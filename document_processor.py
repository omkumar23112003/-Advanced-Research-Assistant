from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from config import Config
import os

class DocumentProcessor:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP
        )
    
    def process_file(self, file_path):
        """Process a single file"""
        if not os.path.exists(file_path):
            return f"File not found: {file_path}"
        
        try:
            if file_path.endswith('.pdf'):
                loader = PyPDFLoader(file_path)
            elif file_path.endswith('.txt'):
                loader = TextLoader(file_path)
            else:
                return f"Unsupported file format: {file_path}"
            
            documents = loader.load()
            splits = self.text_splitter.split_documents(documents)
            
            if self.vector_store is None:
                self.vector_store = FAISS.from_documents(splits, self.embeddings)
            else:
                self.vector_store.add_documents(splits)
            
            return f"Successfully processed {file_path}. Created {len(splits)} chunks."
            
        except Exception as e:
            return f"Error processing file: {str(e)}"
    
    def query_documents(self, question):
        """Query processed documents"""
        if self.vector_store is None:
            return "No documents processed yet."
        
        try:
            retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
            docs = retriever.get_relevant_documents(question)
            
            if not docs:
                return "No relevant information found in documents."
            
            result = "Relevant information from documents:\n\n"
            for i, doc in enumerate(docs, 1):
                result += f"{i}. {doc.page_content[:200]}...\n\n"
            
            return result
            
        except Exception as e:
            return f"Error querying documents: {str(e)}"
    
    def get_document_count(self):
        """Get number of documents processed"""
        if self.vector_store is None:
            return 0
        return self.vector_store.index.ntotal