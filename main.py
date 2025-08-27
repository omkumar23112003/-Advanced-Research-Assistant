from research_assistant import AdvancedResearchAssistant
import argparse

def main():
    parser = argparse.ArgumentParser(description="Advanced Research Assistant")
    parser.add_argument('--chat', action='store_true', help='Start interactive chat')
    parser.add_argument('--query', type=str, help='Single query to process')
    
    args = parser.parse_args()
    
    assistant = AdvancedResearchAssistant()
    
    if args.query:
        print(f"Processing query: {args.query}")
        print("Response:", end=" ")
        response = assistant.process_query(args.query)
        print()
        
        # Show stats
        stats = assistant.get_stats()
        print(f"\n📊 Stats: {stats}")
        
    elif args.chat:
        assistant.chat_interface()
    else:
        # Default to interactive mode
        assistant.chat_interface()

if __name__ == "__main__":
    main()