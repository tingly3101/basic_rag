from lib.utils import load_config_yaml
from lib.chain import ConversationChain
import argparse
from lib.ai_search import AzureAISearch

if __name__ == '__main__':
    #Cycle
    """
    1. Input Prompt (rephrase is optional)
    2. query search from prompt (semantic/ vector or hybrid is optional)
    3. combine prompt with query result (need to text prompt)
    4. send completion to openai
    5. response"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', required=True, type=str, help="YAML config file")      # option that takes a value

    args = parser.parse_args()
    config = load_config_yaml(args.config)
    user_prompt = "momo"

    azure_search_client = AzureAISearch(config)
    search_result = azure_search_client.semantic_search(user_prompt)
    # search_result = azure_search_client.vector_search(user_prompt)
    # search_result = azure_search_client.hybrid_search(user_prompt)
    print("search: ", search_result)


    # conversation_chain = ConversationChain(config)
    # while user_prompt != "exit":

    #     user_prompt = str(input("Question:"))
    #     answer = conversation_chain.rag_chain(user_prompt)
    #     print("-------------------------------------------")
    #     print(f"Question: {answer}")
    #     print('==========================================')

        
    
