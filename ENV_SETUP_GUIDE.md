# Environment Configuration Guide

This application uses a `.env` file to manage all configuration settings including API keys and Flask settings.

## Initial Setup

### 1. Copy the Example File

```bash
cp .env.example .env
```

### 2. Edit the .env File

Open `.env` in your text editor and configure the following:

```env
# ============================================
# Google Gemini API Configuration (Required)
# ============================================

# Your Gemini API key from https://aistudio.google.com/app/apikey
GEMINI_API_KEY=your-actual-gemini-api-key-here

# Gemini model version to use
# Options: gemini-2.0-flash-exp (recommended), gemini-1.5-pro, gemini-1.5-flash
GEMINI_MODEL=gemini-2.0-flash-exp

# ============================================
# Flask Configuration (Optional)
# ============================================

# Secret key for Flask sessions (generate a random string)
FLASK_SECRET_KEY=your-random-secret-key-here

# Enable/disable debug mode (use False in production)
FLASK_DEBUG=True

# Host to bind to (0.0.0.0 = all interfaces, 127.0.0.1 = localhost only)
FLASK_HOST=0.0.0.0

# Port to run on
FLASK_PORT=5000
```

## Getting Your Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and paste it into your `.env` file

## Gemini Model Options

Choose the model that best fits your needs:

| Model | Speed | Capability | Best For |
|-------|-------|------------|----------|
| `gemini-2.0-flash-exp` | ⚡ Fast | Good | Most queries (recommended) |
| `gemini-1.5-flash` | ⚡ Fast | Good | General use |
| `gemini-1.5-pro` | 🐌 Slower | ⭐ Best | Complex queries |

## Generating a Secret Key

The `FLASK_SECRET_KEY` is used to encrypt session data. Generate a secure random key:

**Python:**
```python
import secrets
print(secrets.token_hex(32))
```

**Command Line (Linux/Mac):**
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

**Command Line (Windows):**
```cmd
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and use it as your `FLASK_SECRET_KEY`.

## Example .env File

Here's a complete example with all settings:

```env
# Google Gemini API
GEMINI_API_KEY=AIzaSyD1234567890abcdefghijklmnopqrstuv
GEMINI_MODEL=gemini-2.0-flash-exp

# Flask Configuration
FLASK_SECRET_KEY=a3f8d9c2b1e4f7a8c5d2e9f1b4a7c8d2e5f9a1b4c7d8e2f5a9b1c4d7e8f2a5b9
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
```

## Development vs Production

### Development Settings
```env
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
```

### Production Settings
```env
FLASK_DEBUG=False
FLASK_HOST=127.0.0.1
```

**Important:** Never expose your application to the internet without proper security measures!

## Security Best Practices

1. ✅ **Never commit `.env` to version control**
   - The `.gitignore` file excludes it automatically
   
2. ✅ **Use different API keys for development and production**
   - Keep production keys separate and more restricted

3. ✅ **Rotate your secret key periodically**
   - Generate a new `FLASK_SECRET_KEY` every few months

4. ✅ **Restrict API key permissions**
   - In Google Cloud Console, limit your API key to only Gemini API

5. ✅ **Use environment-specific .env files**
   - `.env.development`
   - `.env.production`

## Troubleshooting

### Error: "GEMINI_API_KEY not configured"

**Solution:**
- Verify `.env` file exists in the project root
- Check that `GEMINI_API_KEY` is set (no quotes needed)
- Ensure no extra spaces around the `=` sign

### Error: "WARNING: GEMINI_API_KEY not found in .env file"

**Solution:**
- Make sure you've created `.env` (not `.env.example`)
- Verify the file is named exactly `.env` (no `.txt` extension)
- Check that the key is on a line starting with `GEMINI_API_KEY=`

### Application not starting

**Solution:**
- Check all required variables are set
- Verify `FLASK_PORT` is not in use by another application
- Make sure `python-dotenv` is installed: `pip install python-dotenv`

### "Invalid API key" error

**Solution:**
- Verify your API key is correct
- Check the key hasn't been revoked in Google AI Studio
- Ensure there are no extra characters or spaces in the key

## Changing Settings

After changing any setting in `.env`, you must restart the Flask application:

1. Stop the app (Ctrl+C)
2. Edit `.env`
3. Start the app again: `python app.py`

The changes will take effect immediately upon restart.

## Environment Variables Priority

The application loads settings in this order:

1. `.env` file (highest priority)
2. System environment variables
3. Default values in code (lowest priority)

This means `.env` file values override system environment variables.

## Backup Your Configuration

Save a copy of your `.env` file (with the API key removed) as a template:

```bash
cp .env .env.backup
```

Edit `.env.backup` and replace sensitive values with placeholders.
