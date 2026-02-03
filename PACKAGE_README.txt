# SQL Database AI Chatbot - Complete Package

This ZIP file contains everything you need to run the Flask-based SQL Database AI Chatbot with Google Gemini.

## 📦 Package Contents

```
sql-database-chatbot/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
│
├── templates/
│   └── index.html                  # Main web interface
│
├── static/
│   ├── css/
│   │   └── style.css              # Dark theme styling
│   └── js/
│       └── app.js                 # Frontend JavaScript
│
├── sample_ecommerce.db            # Sample database for testing
├── sample_data_dictionary.json     # Example data dictionary
├── create_sample_db.py            # Script to regenerate sample DB
│
├── README.md                       # Full documentation
├── QUICKSTART.md                   # Quick start guide
└── ENV_SETUP_GUIDE.md             # Environment setup guide
```

## 🚀 Quick Start (3 Steps)

### 1. Install Dependencies
```bash
cd sql-database-chatbot
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your Gemini API key
# Get your key from: https://aistudio.google.com/app/apikey
```

Your `.env` should look like:
```env
GEMINI_API_KEY=your-actual-api-key-here
GEMINI_MODEL=gemini-2.0-flash-exp
```

### 3. Run the Application
```bash
python app.py
```

Open your browser to: `http://localhost:5000`

## 📖 Documentation

- **README.md** - Complete setup and usage guide
- **QUICKSTART.md** - Get started in 3 minutes
- **ENV_SETUP_GUIDE.md** - Detailed environment configuration

## 🧪 Test with Sample Database

1. Upload `sample_ecommerce.db`
2. Try example questions:
   - "Show me all customers"
   - "What's the total revenue by country?"
   - "Top 5 best-selling products"

## 💡 Key Features

- 🤖 Google Gemini 2.0 Flash integration
- 💬 Natural language to SQL
- 📊 Automatic visualizations
- 🎨 Modern dark UI
- 💾 Session-based chat history
- ⚙️ Data dictionary support

## 🔒 Security Note

⚠️ Never commit your `.env` file with real API keys to version control!
The `.gitignore` file is configured to exclude it automatically.

## 📋 System Requirements

- Python 3.13+ (or 3.10+)
- Google Gemini API key
- Modern web browser

## 🆘 Need Help?

Check the documentation files:
1. Start with **QUICKSTART.md**
2. For detailed setup: **README.md**
3. For .env issues: **ENV_SETUP_GUIDE.md**

## 📝 License

MIT License - Free to use and modify

---

Built with Flask, Google Gemini, and ❤️
