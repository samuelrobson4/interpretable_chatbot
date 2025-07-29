import streamlit as st
from openai import OpenAI
import os
import math
import html

# For Streamlit Cloud deployment
def get_openai_client():
    """Get OpenAI client with API key from Streamlit secrets or environment"""
    # Try Streamlit secrets first (for cloud deployment)
    if hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets:
        api_key = st.secrets['OPENAI_API_KEY']
    else:
        # Fallback to environment variable (for local development)
        api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        return None
    
    return OpenAI(api_key=api_key)

# Initialize client
client = get_openai_client()

def get_confidence_color(confidence_percentage):
    """Return color based on confidence percentage"""
    if confidence_percentage >= 90:
        return "green"
    elif confidence_percentage >= 75:
        return "orange"
    elif confidence_percentage >= 60:
        return "#FF8C00"  # Dark orange
    else:
        return "red"

def format_confidence_label(confidence_percentage):
    """Format confidence as a colored label with Apple-inspired design"""
    # Define Apple-inspired colors for different confidence levels
    if confidence_percentage >= 90:
        color = "#34c759"  # Apple green
        color_dark = "#28a745"
    elif confidence_percentage >= 75:
        color = "#ff9500"  # Apple orange
        color_dark = "#e67e00"
    elif confidence_percentage >= 60:
        color = "#ff3b30"  # Apple red
        color_dark = "#d70015"
    else:
        color = "#ff2d92"  # Apple pink
        color_dark = "#e6007a"
    
    return f"""
    <div class="confidence-label" style="
        --confidence-color: {color};
        --confidence-color-dark: {color_dark};
    ">
        Confidence: {confidence_percentage:.1f}%
    </div>
    """

def get_chatbot_response(user_question):
    """Get response from OpenAI with logprobs"""
    if not client:
        st.error("OpenAI API key not configured. Please set it in Streamlit secrets or environment variables.")
        return None, None
    
    try:
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=user_question,
            max_tokens=150,
            temperature=0.7,
            logprobs=5,  # Get top 5 logprobs for each token
            echo=False
        )
        
        # Extract the response text and logprobs
        response_text = response.choices[0].text.strip()
        logprobs = response.choices[0].logprobs.top_logprobs
        
        return response_text, logprobs
    except Exception as e:
        st.error(f"Error calling OpenAI API: {str(e)}")
        return None, None

def calculate_token_confidences(response_text, logprobs):
    """Calculate confidence for each token"""
    if not logprobs:
        return [], 0.0
    
    token_confidences = []
    total_confidence = 0.0
    token_count = 0
    
    # Process each token's logprobs
    for i, token_logprobs in enumerate(logprobs):
        if token_logprobs:
            # Get the highest logprob (most likely token)
            max_logprob = max(token_logprobs.values())
            confidence = math.exp(max_logprob) * 100
            token_confidences.append(confidence)
            total_confidence += confidence
            token_count += 1
    
    # Calculate overall confidence
    overall_confidence = total_confidence / token_count if token_count > 0 else 0.0
    
    return token_confidences, overall_confidence

def split_response_into_tokens(response_text):
    """Split response text into tokens (simplified tokenization)"""
    # This is a simplified tokenization - in practice, you'd want to use the actual tokens
    # For now, we'll split by whitespace and punctuation
    import re
    tokens = re.findall(r'\S+|\s+', response_text)
    return [token for token in tokens if token.strip()]

def main():
    st.set_page_config(
        page_title="Interpretable Chatbot",
        page_icon="🤖",
        layout="wide"
    )
    
    # Apply Apple-inspired custom CSS
    st.markdown("""
    <style>
    /* Apple-inspired design system */
    .main {
        background-color: #fafafa;
    }
    
    .stApp {
        background-color: #fafafa;
    }
    
    /* Custom title styling */
    .main-title {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-size: 2.5rem;
        font-weight: 600;
        color: #1d1d1f;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .main-subtitle {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-size: 1.1rem;
        color: #86868b;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Card-like containers */
    .chat-container {
        background: white;
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        border: 1px solid #e5e5e7;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 1px solid #e5e5e7;
        padding: 12px 16px;
        font-size: 16px;
        background: white;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #007aff;
        box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 12px;
        font-weight: 500;
        padding: 8px 20px;
        border: none;
        background: linear-gradient(135deg, #007aff 0%, #0056cc 100%);
        color: white;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 122, 255, 0.3);
    }
    
    /* Confidence label styling */
    .confidence-label {
        background: linear-gradient(135deg, var(--confidence-color) 0%, var(--confidence-color-dark) 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        display: inline-block;
        font-weight: 600;
        font-size: 14px;
        margin: 8px 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Token confidence badges */
    .token-badge {
        background: var(--token-color);
        color: white;
        padding: 6px 12px;
        border-radius: 16px;
        display: inline-block;
        margin: 4px;
        font-size: 12px;
        font-weight: 500;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f5f5f7;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: #1d1d1f;
        font-weight: 600;
    }
    
    /* Text styling */
    p, div {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: white;
        border-radius: 12px;
        border: 1px solid #e5e5e7;
        font-weight: 500;
    }
    
    /* Response text styling */
    .response-text {
        background: #f5f5f7;
        padding: 16px;
        border-radius: 12px;
        border-left: 4px solid #007aff;
        margin: 12px 0;
        font-size: 16px;
        line-height: 1.5;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Apple-inspired title
    st.markdown('<h1 class="main-title">Interpretable Chatbot</h1>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">Ask a question and see the model\'s confidence for each token in its response</p>', unsafe_allow_html=True)
    
    # Check if API key is configured
    if not client:
        st.markdown("""
        <div style="
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
            padding: 16px;
            border-radius: 12px;
            margin: 24px 0;
        ">
            <h4 style="margin: 0 0 12px 0; color: #856404;">⚠️ OpenAI API Key Not Configured</h4>
            <p style="margin: 0 0 8px 0;">For local development, create a <code>.env</code> file with:</p>
            <pre style="
                background: #f8f9fa;
                padding: 12px;
                border-radius: 8px;
                margin: 8px 0;
                font-size: 14px;
            ">OPENAI_API_KEY=your_api_key_here</pre>
            <p style="margin: 8px 0 0 0;">For Streamlit Cloud deployment, add your API key in the app settings.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Initialize session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Sidebar for configuration
    with st.sidebar:
        st.markdown("""
        <div style="
            background: white;
            padding: 20px;
            border-radius: 16px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
            border: 1px solid #e5e5e7;
        ">
            <h3 style="margin-top: 0; color: #1d1d1f;">Configuration</h3>
        """, unsafe_allow_html=True)
        
        if client:
            st.success("✅ API key configured")
        else:
            st.warning("⚠️ API key not found")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style="
            background: white;
            padding: 20px;
            border-radius: 16px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
            border: 1px solid #e5e5e7;
        ">
            <h3 style="margin-top: 0; color: #1d1d1f;">How it works</h3>
            <p style="color: #86868b; line-height: 1.5;">
            1. Enter your question below<br>
            2. The model responds with confidence scores<br>
            3. Click "View Token-Level Confidences" to see individual token confidence<br>
            4. Overall confidence is shown at the top
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main chat interface
    st.markdown('<h2 style="color: #1d1d1f; margin-bottom: 24px;">💬 Chat Interface</h2>', unsafe_allow_html=True)
    
    # Chat input container
    st.markdown("""
    <div style="
        background: white;
        padding: 24px;
        border-radius: 16px;
        margin-bottom: 24px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        border: 1px solid #e5e5e7;
    ">
    """, unsafe_allow_html=True)
    
    # User input
    user_question = st.text_input(
        "Ask me anything:",
        placeholder="e.g., What is the capital of France?",
        key="user_input"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        submit_button = st.button("Send", type="primary")
    
    with col2:
        if st.button("Clear Chat", type="secondary"):
            st.session_state.chat_history = []
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Process user input
    if submit_button and user_question:
        with st.spinner("🤔 Thinking..."):
            response_text, logprobs = get_chatbot_response(user_question)
            
            if response_text and logprobs:
                # Calculate confidences
                token_confidences, overall_confidence = calculate_token_confidences(response_text, logprobs)
                
                # Split response into tokens
                tokens = split_response_into_tokens(response_text)
                
                # Create chat entry
                chat_entry = {
                    'question': user_question,
                    'response': response_text,
                    'tokens': tokens,
                    'token_confidences': token_confidences,
                    'overall_confidence': overall_confidence
                }
                
                st.session_state.chat_history.append(chat_entry)
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown('<h2 style="color: #1d1d1f; margin: 32px 0 24px 0;">📝 Chat History</h2>', unsafe_allow_html=True)
        
        for i, entry in enumerate(reversed(st.session_state.chat_history)):
            st.markdown("""
            <div style="
                background: white;
                padding: 24px;
                border-radius: 16px;
                margin-bottom: 24px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
                border: 1px solid #e5e5e7;
            ">
            """, unsafe_allow_html=True)
            
            # User question
            st.markdown(f"""
            <div style="margin-bottom: 16px;">
                <span style="
                    background: #007aff;
                    color: white;
                    padding: 4px 12px;
                    border-radius: 12px;
                    font-size: 12px;
                    font-weight: 600;
                    margin-right: 8px;
                ">You</span>
                <span style="color: #1d1d1f; font-weight: 500;">{entry['question']}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Display overall confidence
            confidence_html = format_confidence_label(entry['overall_confidence'])
            st.markdown(confidence_html, unsafe_allow_html=True)
            
            # Bot response
            st.markdown("""
            <div style="margin: 16px 0;">
                <span style="
                    background: #34c759;
                    color: white;
                    padding: 4px 12px;
                    border-radius: 12px;
                    font-size: 12px;
                    font-weight: 600;
                    margin-right: 8px;
                ">Bot</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Response text in styled container
            st.markdown(f"""
            <div class="response-text">
                {entry['response']}
            </div>
            """, unsafe_allow_html=True)
            
            # Token confidence expander
            with st.expander("🔍 View Token-Level Confidences", expanded=False):
                # Create columns for better layout
                cols = st.columns(3)
                
                for j, token in enumerate(entry['tokens']):
                    if j < len(entry['token_confidences']):
                        confidence = entry['token_confidences'][j]
                        col_idx = j % 3
                        
                        with cols[col_idx]:
                            # Apple-inspired color coding
                            if confidence >= 90:
                                token_color = "#34c759"  # Apple green
                            elif confidence >= 75:
                                token_color = "#ff9500"  # Apple orange
                            elif confidence >= 60:
                                token_color = "#ff3b30"  # Apple red
                            else:
                                token_color = "#ff2d92"  # Apple pink
                            
                            st.markdown(f"""
                            <div class="token-badge" style="--token-color: {token_color};">
                                <strong>{token}</strong>: {confidence:.1f}%
                            </div>
                            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Instructions
    if not st.session_state.chat_history:
        st.markdown("""
        <div style="
            background: white;
            padding: 32px;
            border-radius: 16px;
            margin: 32px 0;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
            border: 1px solid #e5e5e7;
        ">
            <h3 style="color: #1d1d1f; margin-top: 0;">💡 Getting Started</h3>
            <div style="color: #86868b; line-height: 1.6; margin-bottom: 24px;">
                1. <strong>API key is configured</strong> ✅<br>
                2. <strong>Type a question</strong> in the input field above<br>
                3. <strong>Click Send</strong> to get a response with confidence analysis<br>
                4. <strong>Click "View Token-Level Confidences"</strong> to see individual token confidence scores<br>
                5. <strong>Overall confidence</strong> is shown with a colored label
            </div>
            
            <h3 style="color: #1d1d1f;">🎨 Confidence Color Coding</h3>
            <div style="display: flex; flex-wrap: wrap; gap: 12px; margin-top: 16px;">
                <div style="
                    background: #34c759;
                    color: white;
                    padding: 8px 16px;
                    border-radius: 20px;
                    font-size: 14px;
                    font-weight: 500;
                ">🟢 High (≥90%)</div>
                <div style="
                    background: #ff9500;
                    color: white;
                    padding: 8px 16px;
                    border-radius: 20px;
                    font-size: 14px;
                    font-weight: 500;
                ">🟡 Good (75-89%)</div>
                <div style="
                    background: #ff3b30;
                    color: white;
                    padding: 8px 16px;
                    border-radius: 20px;
                    font-size: 14px;
                    font-weight: 500;
                ">🟠 Moderate (60-74%)</div>
                <div style="
                    background: #ff2d92;
                    color: white;
                    padding: 8px 16px;
                    border-radius: 20px;
                    font-size: 14px;
                    font-weight: 500;
                ">🔴 Low (<60%)</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 