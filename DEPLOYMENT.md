# Deployment Guide for Streamlit Cloud

## 🚀 Deploy to Streamlit Cloud

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin main
```

### Step 2: Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository: `SiddharthShukla48/Multi-Agent-Content-Creator-Assistant`
5. Main file path: `app.py`
6. Click "Advanced settings"

### Step 3: Add Secrets
In the "Secrets" section, add:
```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

### Step 4: Deploy
Click "Deploy!" and wait for your app to start.

---

## 🔧 How API Keys Work

### Local Development
- API key is stored in `.env` file (git-ignored)
- Loaded automatically by `python-dotenv`
- Never committed to GitHub

### Streamlit Cloud Deployment
- API key is stored in Streamlit Cloud secrets dashboard
- Accessed via `st.secrets["GROQ_API_KEY"]`
- Securely encrypted and never exposed in logs
- Can be updated anytime without redeploying

---

## 📋 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | Yes | Your Groq API key for LLM access |
| `LANGCHAIN_TRACING_V2` | No | Auto-set to "false" |
| `CHROMA_DB_IMPL` | No | Auto-set to "duckdb+parquet" |

---

## 🔐 Security Best Practices

✅ **DO:**
- Store API keys in `.env` locally
- Add secrets via Streamlit Cloud dashboard
- Keep `.env` in `.gitignore`
- Use `.env.example` as a template

❌ **DON'T:**
- Commit `.env` to GitHub
- Hardcode API keys in code
- Share API keys in public channels
- Store secrets in README or documentation

---

## 🛠️ Updating Secrets After Deployment

To update your API key on Streamlit Cloud:
1. Go to your app dashboard
2. Click "Settings" (⚙️)
3. Click "Secrets"
4. Update the value
5. Save - app will restart automatically

---

## 🐛 Troubleshooting

### "GROQ_API_KEY not found" error
- **Local**: Check that `.env` file exists and contains the key
- **Cloud**: Verify secrets are set in Streamlit Cloud dashboard

### App won't start on Streamlit Cloud
- Check the logs for errors
- Verify `requirements.txt` includes all dependencies
- Ensure Python version compatibility (3.10+)

### Session data issues
- Session data is stored locally in `session_data/` folder
- On Streamlit Cloud, this resets on each deployment
- This is expected behavior for a stateless deployment
