from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from config import Config

class ResearchTools:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.search_tool = DuckDuckGoSearchResults(max_results=Config.SEARCH_MAX_RESULTS)
        self.vector_store = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP
        )
    
    def web_search(self, query):
        """Perform web search and return results"""
        try:
            results = self.search_tool.run(query)
            return str(results)[:1000]  # Limit length to avoid token issues
        except Exception as e:
            return f"Search error: {str(e)}"
    
    def load_and_process_url(self, url):
        """Load webpage content and process it"""
        try:
            loader = WebBaseLoader(url)
            documents = loader.load()
            
            if not documents:
                return "No content found at the provided URL"
            
            splits = self.text_splitter.split_documents(documents)
            
            if self.vector_store is None:
                self.vector_store = FAISS.from_documents(splits, self.embeddings)
            else:
                self.vector_store.add_documents(splits)
            
            return f"Successfully loaded and processed {url}. Found {len(splits)} text chunks."
        except Exception as e:
            return f"Error loading URL: {str(e)}"
    
    def query_documents(self, question):
        """Query the stored documents"""
        if self.vector_store is None:
            return "No documents loaded yet. Use load_webpage tool first."
        
        try:
            retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
            qa_chain = RetrievalQA.from_chain_type(
                llm=ChatOpenAI(temperature=0),
                chain_type="stuff",
                retriever=retriever
            )
            
            return qa_chain.run(question)
        except Exception as e:
            return f"Error querying documents: {str(e)}"
    
    def get_document_count(self):
        """Get number of documents processed"""
        if self.vector_store is None:
            return 0
        return self.vector_store.index.ntotal