import streamlit as st
from research_assistant import AdvancedResearchAssistant
import tempfile
import os
import time

st.set_page_config(
    page_title="🤖 Advanced Research Assistant", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'assistant' not in st.session_state:
    try:
        st.session_state.assistant = AdvancedResearchAssistant()
        st.session_state.initialized = True
    except Exception as e:
        st.error(f"Failed to initialize assistant: {str(e)}")
        st.session_state.initialized = False

if 'messages' not in st.session_state:
    st.session_state.messages = []

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .chat-container {
        max-height: 600px;
        overflow-y: auto;
        padding: 1rem;
        border: 1px solid #ddd;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e6f3ff;
        padding: 0.5rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .assistant-message {
        background-color: #f0f0f0;
        padding: 0.5rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for file upload and settings
with st.sidebar:
    st.title("⚙️ Settings & Tools")
    
    st.subheader("📁 Document Processing")
    uploaded_file = st.file_uploader("Upload PDF or TXT document", type=['pdf', 'txt'])
    
    if uploaded_file:
        with st.spinner("Processing document..."):
            try:
                # Save to temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    file_path = tmp_file.name
                
                # Process file
                result = st.session_state.assistant.document_processor.process_file(file_path)
                st.success("✅ " + result)
                os.unlink(file_path)
                time.sleep(2)
                st.rerun()
                
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
    
    st.subheader("🔧 Utilities")
    if st.button("🧹 Clear Chat History"):
        st.session_state.assistant.memory.clear_memory()
        st.session_state.messages = []
        st.success("Chat history cleared!")
        time.sleep(1)
        st.rerun()
    
    if st.button("📊 Show Statistics"):
        stats = st.session_state.assistant.get_stats()
        st.info(f"""
        **Statistics:**
        - Web Documents: {stats['web_documents']}
        - Local Documents: {stats['local_documents']}
        - Memory Entries: {stats['memory_entries']}
        """)
    
    st.subheader("💡 Usage Tips")
    st.info("""
    **Try these commands:**
    - "Search for AI news"
    - "Load https://example.com"
    - "What do you know about quantum computing?"
    - "Process this document" (after upload)
    """)

# Main chat interface
st.markdown('<h1 class="main-header">🤖 Advanced Research Assistant</h1>', unsafe_allow_html=True)
st.markdown("🔍 *I can help with web searches, document analysis, and research questions*")

# Display chat messages
chat_container = st.container()
with chat_container:
    st.markdown("### 💬 Conversation")
    
    if not st.session_state.messages:
        st.info("👋 Hello! I'm your research assistant. Ask me anything or upload a document to get started.")
    
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="user-message">
                <strong>👤 You:</strong><br>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="assistant-message">
                <strong>🤖 Assistant:</strong><br>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)

# Chat input at the bottom
st.markdown("---")
if not st.session_state.get('initialized', False):
    st.error("Assistant not initialized. Please check your OpenAI API key in the .env file.")
else:
    if prompt := st.chat_input("Type your question here..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message immediately
        with chat_container:
            st.markdown(f"""
            <div class="user-message">
                <strong>👤 You:</strong><br>
                {prompt}
            </div>
            """, unsafe_allow_html=True)
        
        # Get assistant response
        with st.spinner("🤖 Thinking..."):
            try:
                response = st.session_state.assistant.process_query(prompt)
                
                # Add assistant response to chat
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Display assistant response
                with chat_container:
                    st.markdown(f"""
                    <div class="assistant-message">
                        <strong>🤖 Assistant:</strong><br>
                        {response}
                    </div>
                    """, unsafe_allow_html=True)
                
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                with chat_container:
                    st.error(error_msg)
        
        # Rerun to update the UI
        st.rerun()