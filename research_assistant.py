from langchain_openai import ChatOpenAI
from langchain.agents import Tool, AgentExecutor, create_openai_tools_agent
from langchain import hub
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from memory_manager import AdvancedConversationMemory
from research_tools import ResearchTools
from document_processor import DocumentProcessor
from config import Config

class AdvancedResearchAssistant:
    def __init__(self):
        Config.validate_config()
        
        self.memory = AdvancedConversationMemory()
        self.research_tools = ResearchTools()
        self.document_processor = DocumentProcessor()
        self.llm = ChatOpenAI(
            temperature=Config.TEMPERATURE,
            model=Config.MODEL_NAME,
            streaming=True,
            callbacks=[StreamingStdOutCallbackHandler()]
        )
        
        self.agent = self._create_agent()
    
    def _create_agent(self):
        tools = self._create_tools()
        
        prompt = hub.pull("hwchase17/openai-tools-agent")
        
        agent = create_openai_tools_agent(self.llm, tools, prompt)
        
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            handle_parsing_errors=True,
            return_intermediate_steps=False
        )
        
        return agent_executor
    
    def _create_tools(self):
        return [
            Tool(
                name="web_search",
                func=self.research_tools.web_search,
                description="Useful for searching the web for current information, news, and recent developments"
            ),
            Tool(
                name="load_webpage",
                func=self.research_tools.load_and_process_url,
                description="Useful for loading and processing webpage content for detailed analysis. Input should be a URL."
            ),
            Tool(
                name="query_web_documents",
                func=self.research_tools.query_documents,
                description="Useful for querying previously loaded web documents for specific information"
            ),
            Tool(
                name="process_file",
                func=self.document_processor.process_file,
                description="Useful for processing local files (PDF, TXT) for analysis. Input should be a file path."
            ),
            Tool(
                name="query_local_documents",
                func=self.document_processor.query_documents,
                description="Useful for querying processed local documents for specific information"
            )
        ]
    
    def process_query(self, user_input):
        self.memory.add_message("human", user_input)
        
        memory_vars = self.memory.get_memory()
        entities = self.memory.extract_entities(user_input)
        self.memory.update_entity_memory(entities)
        
        enhanced_prompt = f"""
        Conversation Context: {memory_vars['chat_history']}
        Extracted Entities: {self.memory.entity_memory}
        
        Current Query: {user_input}
        
        Please provide a comprehensive response using available tools when needed.
        Be concise but informative.
        """
        
        try:
            response = self.agent.invoke({
                "input": enhanced_prompt,
                "chat_history": memory_vars['chat_history']
            })
            
            self.memory.add_message("ai", response['output'])
            return response['output']
            
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            self.memory.add_message("ai", error_msg)
            return error_msg
    
    def chat_interface(self):
        print("🤖 Advanced Research Assistant Initialized!")
        print("🔍 I can help with web searches, document analysis, and research")
        print("💡 Try commands like: 'search for AI news', 'load https://example.com', 'process document.txt'")
        print("Type 'clear' to clear memory, 'quit' to exit")
        print("-" * 60)
        
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("👋 Goodbye!")
                    break
                elif user_input.lower() == 'clear':
                    self.memory.clear_memory()
                    print("🧹 Memory cleared!")
                    continue
                elif not user_input:
                    continue
                
                print("\n🤖 Assistant: ", end="")
                response = self.process_query(user_input)
                print()  # New line after streaming
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
    
    def get_stats(self):
        return {
            "web_documents": self.research_tools.get_document_count(),
            "local_documents": self.document_processor.get_document_count(),
            "memory_entries": len(self.memory.memory.chat_memory.messages)
        }