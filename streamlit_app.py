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
    """Format confidence as a colored label"""
    color = get_confidence_color(confidence_percentage)
    return f"""
    <div style="
        background-color: {color}; 
        color: white; 
        padding: 8px 12px; 
        border-radius: 20px; 
        display: inline-block; 
        font-weight: bold;
        margin-bottom: 10px;
    ">
        Overall Confidence: {confidence_percentage:.1f}%
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
    
    st.title("🤖 Interpretable Chatbot with Confidence Analysis")
    st.markdown("Ask a question and see the model's confidence for each token in its response!")
    
    # Check if API key is configured
    if not client:
        st.error("""
        ⚠️ **OpenAI API Key Not Configured**
        
        For local development, create a `.env` file with:
        ```
        OPENAI_API_KEY=your_api_key_here
        ```
        
        For Streamlit Cloud deployment, add your API key in the app settings.
        """)
        return
    
    # Initialize session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("🔧 Configuration")
        
        if client:
            st.success("✅ API key configured")
        else:
            st.warning("⚠️ API key not found")
        
        st.markdown("---")
        st.markdown("### How it works:")
        st.markdown("""
        1. Enter your question below
        2. The model responds with confidence scores
        3. Click "View Token-Level Confidences" to see individual token confidence
        4. Overall confidence is shown at the top
        """)
    
    # Main chat interface
    st.header("💬 Chat Interface")
    
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
        if st.button("Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
    
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
        st.markdown("---")
        st.header("📝 Chat History")
        
        for i, entry in enumerate(reversed(st.session_state.chat_history)):
            with st.container():
                st.markdown(f"**You:** {entry['question']}")
                
                # Display overall confidence
                confidence_html = format_confidence_label(entry['overall_confidence'])
                st.markdown(confidence_html, unsafe_allow_html=True)
                
                # Display response with token tooltips
                st.markdown("**Bot:**")
                
                # Create a more Streamlit-friendly display with expandable token details
                response_container = st.container()
                
                with response_container:
                    # Display the response text normally
                    st.write(entry['response'])
                    
                    # Add an expander to show token-level confidences
                    with st.expander("🔍 View Token-Level Confidences"):
                        # Create columns for better layout
                        cols = st.columns(3)
                        
                        for j, token in enumerate(entry['tokens']):
                            if j < len(entry['token_confidences']):
                                confidence = entry['token_confidences'][j]
                                col_idx = j % 3
                                
                                with cols[col_idx]:
                                    # Color code based on confidence
                                    color = get_confidence_color(confidence)
                                    st.markdown(f"""
                                    <div style="
                                        background-color: {color}; 
                                        color: white; 
                                        padding: 4px 8px; 
                                        border-radius: 12px; 
                                        display: inline-block; 
                                        margin: 2px;
                                        font-size: 12px;
                                    ">
                                        <strong>{token}</strong>: {confidence:.1f}%
                                    </div>
                                    """, unsafe_allow_html=True)
                
                st.markdown("---")
    
    # Instructions
    if not st.session_state.chat_history:
        st.markdown("---")
        st.markdown("### 💡 Getting Started")
        st.markdown("""
        1. **API key is configured** ✅
        2. **Type a question** in the input field above
        3. **Click Send** to get a response with confidence analysis
        4. **Click "View Token-Level Confidences"** to see individual token confidence scores
        5. **Overall confidence** is shown with a colored label
        """)
        
        st.markdown("### 🎨 Confidence Color Coding")
        st.markdown("""
        - 🟢 **Green (≥90%)**: High confidence
        - 🟡 **Yellow (75-89%)**: Good confidence  
        - 🟠 **Orange (60-74%)**: Moderate confidence
        - 🔴 **Red (<60%)**: Low confidence
        """)

if __name__ == "__main__":
    main() 