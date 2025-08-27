AI Assistant with Web Search & Document Processing
A Streamlit-based AI assistant that combines conversational AI with web search capabilities and document processing. This application allows users to interact with an AI model, perform web searches, and analyze uploaded documents through a simple chat interface.

https://img.shields.io/badge/Streamlit-AI%2520Assistant-red
https://img.shields.io/badge/Python-3.8%252B-blue
https://img.shields.io/badge/OpenAI-GPT--3.5%252B-green

Features
Chat Interface: Interactive conversation with an AI assistant

Web Search: Access to current information via DuckDuckGo search

Document Processing: Upload and analyze PDF and text files

URL Loading: Extract and process content from web pages

Conversation Memory: Maintains context across conversations

Usage Statistics: Track token usage and costs in the sidebar

Installation
Clone the repository:

bash
git clone <your-repo-url>
cd ai-assistant
Install required dependencies:

bash
pip install -r requirements.txt
Set up environment variables:

Create a .env file in the root directory

Add your OpenAI API key:

text
OPENAI_API_KEY=your_api_key_here
Requirements
Create a requirements.txt file with the following content:

text
streamlit
openai
langchain
duckduckgo-search
faiss-cpu
pypdf
python-dotenv
tiktoken
Usage
Start the application:

bash
streamlit run app.py
Open your browser and navigate to the provided URL (typically http://localhost:8501)

Interact with the assistant:

Type messages in the chat input

Use the sidebar to upload documents

Ask questions that require web search

Request to load specific URLs