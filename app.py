from flask import Flask, render_template, request, jsonify, session
import sqlite3
import pandas as pd
import json
import os
import google.generativeai as genai
from datetime import datetime
import uuid
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure Flask from environment variables
app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24))

# Configure Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-exp')

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("WARNING: GEMINI_API_KEY not found in .env file")

def get_database_schema(db_path):
    """Extract schema information from SQLite database"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    schema_info = "DATABASE SCHEMA:\n\n"
    
    for table in tables:
        table_name = table[0]
        schema_info += f"Table: {table_name}\n"
        
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        for col in columns:
            col_id, col_name, col_type, not_null, default_val, pk = col
            schema_info += f"  - {col_name} ({col_type})"
            if pk:
                schema_info += " [PRIMARY KEY]"
            if not_null:
                schema_info += " [NOT NULL]"
            schema_info += "\n"
        
        cursor.execute(f"PRAGMA foreign_key_list({table_name});")
        fks = cursor.fetchall()
        if fks:
            schema_info += "  Foreign Keys:\n"
            for fk in fks:
                schema_info += f"    - {fk[3]} -> {fk[2]}.{fk[4]}\n"
        
        schema_info += "\n"
    
    conn.close()
    return schema_info

def format_data_dictionary(data_dict):
    """Format data dictionary for the system prompt"""
    if not data_dict:
        return ""
    
    dict_text = "\n\nDATA DICTIONARY (Business Context):\n\n"
    for key, description in data_dict.items():
        dict_text += f"- {key}: {description}\n"
    
    return dict_text

def execute_sql_query(db_path, query):
    """Execute SQL query and return results as DataFrame"""
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df, None
    except Exception as e:
        return None, str(e)

def create_visualization(df, query_type="table"):
    """Create visualization from dataframe"""
    try:
        plt.clf()
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Simple heuristic for chart type
        if len(df.columns) == 2 and df[df.columns[1]].dtype in ['int64', 'float64']:
            # Bar chart for 2 columns with numeric values
            df.plot(x=df.columns[0], y=df.columns[1], kind='bar', ax=ax, color='#4A90E2')
            ax.set_xlabel(df.columns[0])
            ax.set_ylabel(df.columns[1])
            plt.xticks(rotation=45, ha='right')
        elif len(df.columns) >= 2 and all(df[col].dtype in ['int64', 'float64'] for col in df.columns[1:]):
            # Line chart for time series or multiple numeric columns
            df.plot(x=df.columns[0], y=df.columns[1:], kind='line', ax=ax, marker='o')
            ax.set_xlabel(df.columns[0])
            plt.xticks(rotation=45, ha='right')
        else:
            return None
        
        plt.tight_layout()
        
        # Save to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close()
        
        return image_base64
    except Exception as e:
        print(f"Visualization error: {e}")
        return None

def get_system_prompt(schema_info, data_dictionary):
    """Generate system prompt with schema and data dictionary"""
    prompt = f"""You are a helpful SQL database assistant. You help users query and understand their SQLite database.

{schema_info}
{format_data_dictionary(data_dictionary)}

When users ask questions about their data:
1. Understand what they're asking for
2. Generate the appropriate SQL query
3. Explain what the query does
4. Present the SQL query in a code block using ```sql

Always generate valid SQLite SQL syntax. Be helpful and explain your reasoning.

When showing SQL queries, format them clearly with proper indentation.
If a question is ambiguous, ask for clarification before generating a query.

For visualization requests, suggest appropriate chart types based on the data structure.
"""
    return prompt

def extract_sql_from_response(response_text):
    """Extract SQL query from Gemini's response"""
    if "```sql" in response_text:
        start = response_text.find("```sql") + 6
        end = response_text.find("```", start)
        return response_text[start:end].strip()
    elif "```" in response_text:
        start = response_text.find("```") + 3
        end = response_text.find("```", start)
        sql = response_text[start:end].strip()
        if any(keyword in sql.upper() for keyword in ["SELECT", "INSERT", "UPDATE", "DELETE", "CREATE"]):
            return sql
    return None

@app.route('/')
def index():
    # Initialize session
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    if 'chat_history' not in session:
        session['chat_history'] = []
    if 'db_path' not in session:
        session['db_path'] = None
    if 'data_dictionary' not in session:
        session['data_dictionary'] = {}
    
    return render_template('index.html')

@app.route('/upload_db', methods=['POST'])
def upload_db():
    try:
        if 'database' not in request.files:
            return jsonify({'error': 'No database file provided'}), 400
        
        file = request.files['database']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save database
        db_path = os.path.join('uploads', f"{session['session_id']}_{file.filename}")
        os.makedirs('uploads', exist_ok=True)
        file.save(db_path)
        
        # Get schema
        schema_info = get_database_schema(db_path)
        
        session['db_path'] = db_path
        session['schema_info'] = schema_info
        
        return jsonify({
            'success': True,
            'schema': schema_info,
            'message': 'Database uploaded successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/update_dictionary', methods=['POST'])
def update_dictionary():
    try:
        data = request.json
        dictionary = data.get('dictionary', {})
        
        if isinstance(dictionary, str):
            dictionary = json.loads(dictionary)
        
        session['data_dictionary'] = dictionary
        
        return jsonify({
            'success': True,
            'message': 'Data dictionary updated successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not session.get('db_path'):
            return jsonify({'error': 'Please upload a database first'}), 400
        
        if not GEMINI_API_KEY:
            return jsonify({'error': 'GEMINI_API_KEY not configured'}), 500
        
        # Build conversation history
        chat_history = session.get('chat_history', [])
        
        # Get system prompt
        system_prompt = get_system_prompt(
            session.get('schema_info', ''),
            session.get('data_dictionary', {})
        )
        
        # Create Gemini model
        model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            system_instruction=system_prompt
        )
        
        # Build conversation for Gemini
        gemini_history = []
        for msg in chat_history:
            role = "user" if msg['role'] == 'user' else "model"
            gemini_history.append({
                "role": role,
                "parts": [msg['content']]
            })
        
        # Start chat
        chat_session = model.start_chat(history=gemini_history)
        
        # Send message
        response = chat_session.send_message(user_message)
        assistant_message = response.text
        
        # Extract SQL query
        sql_query = extract_sql_from_response(assistant_message)
        
        # Execute query if SQL found
        query_results = None
        visualization = None
        error = None
        
        if sql_query:
            df, exec_error = execute_sql_query(session['db_path'], sql_query)
            
            if exec_error:
                error = exec_error
            elif df is not None and not df.empty:
                query_results = {
                    'columns': df.columns.tolist(),
                    'data': df.to_dict('records'),
                    'row_count': len(df)
                }
                
                # Try to create visualization
                if len(df) > 0 and len(df) <= 100:
                    viz = create_visualization(df)
                    if viz:
                        visualization = viz
        
        # Update chat history
        chat_history.append({
            'role': 'user',
            'content': user_message,
            'timestamp': datetime.now().isoformat()
        })
        
        chat_history.append({
            'role': 'assistant',
            'content': assistant_message,
            'timestamp': datetime.now().isoformat(),
            'sql_query': sql_query
        })
        
        session['chat_history'] = chat_history
        
        return jsonify({
            'success': True,
            'message': assistant_message,
            'sql_query': sql_query,
            'results': query_results,
            'visualization': visualization,
            'error': error
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clear_history', methods=['POST'])
def clear_history():
    session['chat_history'] = []
    return jsonify({'success': True, 'message': 'Chat history cleared'})

@app.route('/new_chat', methods=['POST'])
def new_chat():
    session['session_id'] = str(uuid.uuid4())
    session['chat_history'] = []
    return jsonify({'success': True, 'message': 'New chat started'})

@app.route('/get_schema', methods=['GET'])
def get_schema():
    schema = session.get('schema_info', '')
    return jsonify({'schema': schema})

if __name__ == '__main__':
    # Get Flask configuration from environment variables
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    
    app.run(debug=debug, host=host, port=port)
