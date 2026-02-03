# SQL Database AI Chatbot (Flask + Gemini)

A modern, dark-themed Flask web application that lets you chat with SQLite databases using Google's Gemini AI. Features include natural language querying, automatic visualization, and chat history management.

## Features

- 🗄️ **SQLite Database Support**: Upload and query any SQLite database
- 💬 **Natural Language Interface**: Ask questions in plain English
- 📊 **Auto-Generate Visualizations**: Automatic charts for query results
- 🤖 **Powered by Gemini 2.0 Flash**: Fast and accurate AI responses
- 📖 **Data Dictionary Support**: Add business context to help AI understand your data
- 💾 **Session-Based Chat History**: Maintains conversation context
- 🎨 **Modern Dark UI**: Clean, professional interface inspired by modern AI tools
- 🔄 **Clear History & New Chat**: Manage your conversation sessions

## Screenshots

The interface is designed to match the modern, dark aesthetic of contemporary AI tools with:
- Clean welcome screen with upload functionality
- Chat interface with message bubbles
- SQL query highlighting
- Automatic result tables
- Chart visualizations
- Settings modal for database configuration

## Requirements

- Python 3.13+
- Google Gemini API key

## Installation

### 1. Clone or Download

```bash
cd sql-chatbot-flask
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root directory:

```bash
cp .env.example .env
```

Then edit `.env` and add your API key:

```env
# Google Gemini API Configuration
GEMINI_API_KEY=your-actual-gemini-api-key-here
GEMINI_MODEL=gemini-3-flash-preview

# Flask Configuration
FLASK_SECRET_KEY=your-secret-key-here
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
FLASK_PORT=5002
```

**Get your Gemini API key from:** [Google AI Studio](https://aistudio.google.com/app/apikey)


### 4. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5002`

## Usage

### 1. Upload Your Database

Click the "Upload Database" button on the welcome screen and select your SQLite database file (`.db`, `.sqlite`, or `.sqlite3`).

### 2. Configure Data Dictionary (Optional)

Click the settings icon in the header to open the settings modal. Add a data dictionary in JSON format to help the AI better understand your data:

```json
{
  "customers.email": "Customer's login email address, unique identifier",
  "customers.lifetime_value": "Total revenue from this customer in USD",
  "orders.status": "Order state: 'pending', 'shipped', 'delivered', 'cancelled'",
  "products.category": "Product category: Electronics, Furniture, or Accessories"
}
```

### 3. Start Chatting

Ask questions about your database:
- "Show me all customers from the USA"
- "What are the top 5 best-selling products?"
- "Calculate the average order value by month"
- "Which customers have lifetime value over $1000?"

### 4. View Results

The AI will:
1. Generate appropriate SQL queries
2. Execute them automatically
3. Display results in a table
4. Create visualizations when appropriate

### 5. Manage Your Session

- **Clear Chat History**: Remove all messages but keep the database connection
- **Start New Chat**: Begin fresh (clears history and resets to welcome screen)

## Testing with Sample Database

A sample e-commerce database is included (`sample_ecommerce.db`) with:
- **customers**: Customer information
- **products**: Product catalog
- **orders**: Order records
- **order_items**: Line items for each order

Try these example questions:
1. "How many customers do we have from each country?"
2. "What's the average order value?"
3. "Show me all electronics products under $100"
4. "Which customer has spent the most money?"
5. "What's the total revenue by product category?"

## Project Structure

```
.
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── templates/
│   └── index.html             # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css          # Styling (dark theme)
│   └── js/
│       └── app.js             # Frontend JavaScript
├── uploads/                    # Database upload directory (auto-created)
├── sample_ecommerce.db        # Sample database
└── sample_data_dictionary.json # Example data dictionary
```

## Data Dictionary Best Practices

A good data dictionary includes:

1. **Business Context**: What the column represents in real-world terms
2. **Valid Values**: For categorical columns, list possible values
3. **Relationships**: How columns relate to business processes
4. **Units**: Specify currency, measurements, etc.
5. **Special Cases**: Edge cases or important notes

Example:
```json
{
  "transactions.amount": "Transaction value in USD, negative for refunds",
  "users.role": "Access level: 'admin' (full access), 'manager' (team only), 'employee' (basic)",
  "products.sku": "Stock Keeping Unit in format: CAT-XXXX-YY",
  "orders.created_at": "When order was placed (UTC timezone)"
}
```

## How It Works

1. **Database Upload**: When you upload a database, the app extracts the schema (tables, columns, types, relationships)
2. **System Prompt**: The schema and data dictionary are combined into a system prompt for Gemini
3. **Chat Processing**: User questions are sent to Gemini with full conversation history
4. **SQL Extraction**: The app parses Gemini's response to extract SQL queries
5. **Execution**: Queries are automatically executed against the database
6. **Visualization**: Results are analyzed and visualized when appropriate
7. **Session Management**: Chat history is stored in Flask sessions

 

## Troubleshooting

**"GEMINI_API_KEY not configured"**
- Ensure you've created a `.env` file in the project root
- Check that `GEMINI_API_KEY` is set in your `.env` file
- Verify there are no typos in the variable name
- Make sure the `.env` file is in the same directory as `app.py`

**"WARNING: GEMINI_API_KEY not found in .env file"**
- Create a `.env` file by copying `.env.example`
- Add your actual API key to the `.env` file

**Database upload fails**
- Ensure the file is a valid SQLite database
- Check file permissions

**SQL errors**
- The AI-generated query might need refinement
- Try rephrasing your question
- Add more context in the data dictionary

**Charts not appearing**
- Only certain result types can be visualized
- Results must have numeric data
- Limited to 100 rows for performance

## Security Notes

- **Never commit your `.env` file to version control** - It contains sensitive API keys
- The `.gitignore` file is configured to exclude `.env` automatically
- Use `.env.example` as a template for sharing configuration structure
- This is a development application - don't expose to the internet without proper security
- Database files are stored in the `uploads/` directory
- Sessions use secure random keys from `.env`
- Consider adding authentication for production use

## Contributing

Feel free to customize and extend this application:
- Add support for other database types (PostgreSQL, MySQL)
- Implement user authentication
- Add export functionality (PDF, Excel)
- Enhanced visualization options
- Query history and favorites

## License

MIT License - Free to use and modify

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the data dictionary examples
3. Ensure your Gemini API key is valid and has quota

---

Built with Flask, Google Gemini, and ❤️
