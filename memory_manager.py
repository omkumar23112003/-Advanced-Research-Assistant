from langchain.memory import ConversationBufferWindowMemory
from langchain.schema import HumanMessage, AIMessage
from config import Config

class AdvancedConversationMemory:
    def __init__(self, k=Config.MEMORY_WINDOW_SIZE):
        self.memory = ConversationBufferWindowMemory(
            k=k,
            memory_key="chat_history",
            return_messages=True
        )
        self.entity_memory = {}
    
    def add_message(self, role, content):
        if role == "human":
            message = HumanMessage(content=content)
        else:
            message = AIMessage(content=content)
        self.memory.chat_memory.add_message(message)
    
    def get_memory(self):
        return self.memory.load_memory_variables({})
    
    def extract_entities(self, text):
        entities = {
            "topics": [],
            "questions": [],
            "actions": []
        }
        
        # Simple entity extraction
        if "?" in text:
            entities["questions"].append(text.split("?")[0] + "?")
        
        # Extract potential topics (simplified)
        words = text.lower().split()
        topics = ["ai", "machine learning", "quantum", "research", "news", "technology"]
        for word in words:
            if word in topics and word not in entities["topics"]:
                entities["topics"].append(word)
        
        return entities
    
    def update_entity_memory(self, entities):
        for key, values in entities.items():
            if key not in self.entity_memory:
                self.entity_memory[key] = []
            # Add only new values
            for value in values:
                if value not in self.entity_memory[key]:
                    self.entity_memory[key].append(value)
    
    def clear_memory(self):
        self.memory.clear()
        self.entity_memory = {}