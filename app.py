import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')

# Streamlit UI
st.set_page_config(page_title="whitecode.ai", page_icon="🤖")
st.title("whitecode.ai - Coding Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "ai", "content": "Hello! I'm whitecode.ai. Ask me coding questions."}]

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"], unsafe_allow_html=True)

# Process user input
if prompt := st.chat_input("Ask a coding question..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("ai"):
        with st.spinner("Thinking..."):
            try:
                response = model.generate_content(f"""
                    As whitecode.ai coding assistant, provide:
                    1. Well-formatted code with proper indentation
                    2. Markdown code blocks with language specification
                    3. Clear explanations when needed

                    Question: {prompt}
                    """)
                st.markdown(response.text, unsafe_allow_html=True)
                st.session_state.messages.append({"role": "ai", "content": response.text})
            except Exception as e:
                st.error(f"Error: {str(e)}")