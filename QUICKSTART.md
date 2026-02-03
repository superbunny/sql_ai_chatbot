# Quick Start Guide - Flask SQL Chatbot

## Get Running in 3 Minutes ⚡

### Step 1: Install Dependencies
```bash
pip install Flask google-generativeai pandas matplotlib seaborn python-dotenv
```

### Step 2: Create .env File
Copy the example file and add your API key:

```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:
```env
GEMINI_API_KEY=your-actual-key-here
GEMINI_MODEL=gemini-2.0-flash-exp
```

Get your key from: https://aistudio.google.com/app/apikey

### Step 3: Run the App
```bash
python app.py
```

### Step 4: Open Your Browser
Navigate to: `http://localhost:5000`

### Step 5: Try It Out
1. Click "Upload Database"
2. Select `sample_ecommerce.db` (included)
3. Start asking questions!

## Example Questions

Try these with the sample database:

✅ **Simple Queries:**
- "Show me all customers"
- "List products in the Electronics category"
- "What orders are pending?"

✅ **Aggregations:**
- "Total revenue by country"
- "Top 5 customers by lifetime value"
- "How many orders in March 2024?"

✅ **Analytics:**
- "Average order value per customer"
- "Monthly revenue trends"
- "Best-selling product category"

## Add Data Dictionary

1. Click the settings icon (⚙️) in the header
2. Paste this example dictionary:

```json
{
  "customers.email": "Customer's login email, unique identifier",
  "customers.lifetime_value": "Total revenue in USD from all orders",
  "orders.status": "Order state: pending/shipped/delivered/cancelled",
  "products.category": "Product type: Electronics, Furniture, Accessories"
}
```

3. Click "Update Data Dictionary"

## Features

- 🤖 AI-powered SQL generation
- 📊 Automatic chart creation
- 💬 Chat history in session
- 🗑️ Clear history button
- ✨ Start new chat button
- ⚙️ Settings for schema and dictionary

## Using Your Own Database

1. Upload your `.db` file
2. Create a data dictionary for your columns
3. Start chatting!

That's it! 🎉

## Keyboard Shortcuts

- **Enter** - Send message
- **Shift + Enter** - New line in message

## Tips

- Be specific in questions
- Use the data dictionary for better results
- Check the settings to see your schema
- Clear history if context gets confusing

## Environment Configuration

Your `.env` file should look like this:

```env
# Required
GEMINI_API_KEY=your-key-here
GEMINI_MODEL=gemini-2.0-flash-exp

# Optional
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_SECRET_KEY=random-secret-key
```

**Change Model:**
Edit `GEMINI_MODEL` in `.env`:
- `gemini-2.0-flash-exp` (fast, recommended)
- `gemini-1.5-pro` (more capable)
- `gemini-1.5-flash` (balanced)

**Change Port:**
Edit `FLASK_PORT` in `.env` to use a different port.
