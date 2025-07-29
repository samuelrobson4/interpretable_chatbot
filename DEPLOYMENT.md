# 🚀 Deployment Guide

This guide shows you how to deploy your Interpretable Chatbot securely without exposing your API keys.

## 🔐 **Option 1: Streamlit Cloud (Recommended)**

### **Step 1: Prepare Your Repository**

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git push -u origin main
   ```

2. **Ensure your repository has:**
   - `streamlit_app.py` (main app file)
   - `requirements.txt` (dependencies)
   - `README.md` (documentation)

### **Step 2: Deploy to Streamlit Cloud**

1. **Go to [share.streamlit.io](https://share.streamlit.io)**
2. **Sign in with GitHub**
3. **Click "New app"**
4. **Configure your app:**
   - **Repository**: Select your GitHub repo
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
5. **Click "Deploy"**

### **Step 3: Add Your API Key**

1. **In your deployed app, go to Settings (⚙️)**
2. **Click "Secrets"**
3. **Add your API key:**
   ```toml
   OPENAI_API_KEY = "sk-your-api-key-here"
   ```
4. **Click "Save"**

### **Step 4: Your App is Live!**

Your app will be available at: `https://your-app-name.streamlit.app`

---

## ☁️ **Option 2: Heroku**

### **Step 1: Create Heroku App**

```bash
# Install Heroku CLI
brew install heroku/brew/heroku  # macOS
# or download from https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login

# Create app
heroku create your-app-name
```

### **Step 2: Add Configuration**

```bash
# Set environment variables
heroku config:set OPENAI_API_KEY="sk-your-api-key-here"
```

### **Step 3: Deploy**

```bash
# Add Heroku buildpack for Python
heroku buildpacks:set heroku/python

# Deploy
git push heroku main
```

---

## 🐳 **Option 3: Docker**

### **Step 1: Create Dockerfile**

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### **Step 2: Build and Run**

```bash
# Build image
docker build -t interpretable-chatbot .

# Run with environment variable
docker run -p 8501:8501 -e OPENAI_API_KEY="sk-your-api-key-here" interpretable-chatbot
```

---

## 🌐 **Option 4: Railway**

### **Step 1: Connect Repository**

1. **Go to [railway.app](https://railway.app)**
2. **Connect your GitHub repository**
3. **Select your repository**

### **Step 2: Configure Environment**

1. **Go to Variables tab**
2. **Add environment variable:**
   - **Name**: `OPENAI_API_KEY`
   - **Value**: `sk-your-api-key-here`

### **Step 3: Deploy**

Railway will automatically deploy your app when you push to GitHub.

---

## 🔒 **Security Best Practices**

### **Never Do This:**
- ❌ Hardcode API keys in your code
- ❌ Commit `.env` files to Git
- ❌ Share API keys in public repositories
- ❌ Use API keys in client-side code

### **Always Do This:**
- ✅ Use environment variables or secrets management
- ✅ Add `.env` to your `.gitignore`
- ✅ Use different API keys for development and production
- ✅ Regularly rotate your API keys
- ✅ Monitor API usage and costs

### **Add to .gitignore:**

```gitignore
# Environment variables
.env
.env.local
.env.production

# API keys
*.key
secrets.json

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

---

## 📊 **Cost Management**

### **Monitor Usage:**
- Set up billing alerts in OpenAI dashboard
- Use usage tracking in your app
- Consider rate limiting for public deployments

### **Optimize Costs:**
- Use appropriate model sizes
- Implement caching for repeated queries
- Set reasonable token limits

---

## 🚨 **Troubleshooting**

### **Common Issues:**

1. **"API key not found"**
   - Check environment variable name
   - Verify secrets configuration
   - Restart the app after adding secrets

2. **"Model not found"**
   - Ensure you're using `gpt-3.5-turbo-instruct`
   - Check OpenAI API status

3. **"Rate limit exceeded"**
   - Implement rate limiting
   - Use API key with higher limits
   - Add retry logic

### **Get Help:**
- [Streamlit Documentation](https://docs.streamlit.io)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [GitHub Issues](https://github.com/your-repo/issues)

---

## 🎉 **You're Ready to Deploy!**

Choose the deployment option that best fits your needs:

- **Streamlit Cloud**: Easiest, best for demos and prototypes
- **Heroku**: Good for production apps with custom domains
- **Docker**: Most flexible, works anywhere
- **Railway**: Modern, developer-friendly

Your app will be secure and ready to share with the world! 🌍 