import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
import markdown
import re

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')


def format_code_blocks(text):
    # Convert markdown code blocks to HTML with proper formatting
    text = markdown.markdown(text)
    # Add additional styling for code blocks
    text = text.replace('<code>',
                        '<code style="display: block; white-space: pre-wrap; background: #f4f4f4; padding: 10px; border-radius: 5px; margin: 10px 0;">')
    return text


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.form['question']

    try:
        # Add context to make sure Gemini provides well-formatted code responses
        prompt = f"""You are whitecode.ai, an AI coding assistant. 
        1st give code 
        When providing code solutions, always format them properly with correct indentation.
        Use markdown code blocks with language specification for syntax highlighting.

        Question: {user_question}

        Answer:"""

        response = model.generate_content(prompt)
        formatted_response = format_code_blocks(response.text)

        return jsonify({'response': formatted_response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)