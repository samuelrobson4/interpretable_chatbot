# 🤖 Interpretable Chatbot with Confidence Tooltips

A Streamlit web application that provides an interpretable chatbot interface with token-level confidence analysis and interactive tooltips.

## ✨ Features

- **Interactive Chat Interface**: Simple and intuitive chatbot UI
- **Token-Level Confidence Analysis**: See confidence scores for each token in the response
- **Hover Tooltips**: Hover over any token to see its individual confidence percentage
- **Overall Confidence Display**: Color-coded confidence labels at the top of each response
- **Chat History**: View all previous conversations with confidence analysis
- **Real-time Analysis**: Uses OpenAI's `gpt-3.5-turbo-instruct` model with `logprobs` parameter

## 🎨 Confidence Color Coding

- 🟢 **Green (≥90%)**: High confidence
- 🟡 **Yellow (75-89%)**: Good confidence  
- 🟠 **Orange (60-74%)**: Moderate confidence
- 🔴 **Red (<60%)**: Low confidence

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up OpenAI API Key

Create a `.env` file in the project root:

```bash
cp env_example.txt .env
```

Then edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=your_actual_api_key_here
```

**Get your API key from:** [OpenAI Platform](https://platform.openai.com/api-keys)

### 3. Run the Application

```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

## 🚀 Deployment

For secure deployment options, see [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions on:

- **Streamlit Cloud** (Recommended - easiest)
- **Heroku**
- **Docker**
- **Railway**

All deployment methods keep your API keys secure using environment variables or secrets management.

## 📖 How to Use

1. **Enter your OpenAI API key** in the sidebar
2. **Type a question** in the input field
3. **Click Send** to get a response with confidence analysis
4. **Hover over tokens** in the response to see individual confidence scores
5. **View overall confidence** with the colored label at the top

## 🔧 Technical Details

### Confidence Calculation

The app calculates confidence using the following process:

1. **Token Analysis**: Uses OpenAI's `logprobs` parameter to get probability distributions for each token
2. **Confidence Score**: `confidence = exp(logprob) * 100`
3. **Overall Confidence**: Average of all token confidences
4. **Display**: Rounded to one decimal place as percentage

### Token Tooltips

Each token is rendered with:
- **Hover tooltip**: Shows individual confidence percentage
- **Visual indicator**: Dotted underline to suggest interactivity
- **Cursor change**: Help cursor on hover

### API Configuration

- **Model**: `gpt-3.5-turbo-instruct`
- **Logprobs**: 5 (returns top 5 probability distributions per token)
- **Max Tokens**: 150
- **Temperature**: 0.7

## 📁 Project Structure

```
Interp/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── env_example.txt     # Example environment configuration
└── README.md          # This file
```

## 🛠️ Dependencies

- **Streamlit**: Web application framework
- **OpenAI**: API client for GPT models (v1.0.0+)
- **python-dotenv**: Environment variable management

## 🔒 Security Notes

- API keys are stored securely in environment variables
- HTML content is properly escaped to prevent XSS attacks
- No sensitive data is logged or stored

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is open source and available under the MIT License. 

## 👤 Made by

**Samuel Robson**  
Product-minded strategist and AI prototyper  
🎓 MIMS @ UC Berkeley  
🛠️ Interpretability · Tangible Interfaces · Human-Centered AI

[GitHub](https://github.com/samuelrobson4) · [LinkedIn](https://www.linkedin.com/in/samuelrobson1/)
