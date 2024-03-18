from lib.llm import LLM
from lib.ai_search import AzureAISearch

class ConversationChain():

    def __init__(self, config) -> None:
        self.config = config
        self.system_prompt = config["system-prompt"]
        self.search_type = config["ai-search"]["search-type"]

    def rag_chain(self, text: str=""):
        # print("search-type:", self.search_type)
        azure_search_client = AzureAISearch(self.config)
        llm = LLM(self.config)
        search_result = ""
        if self.search_type == "semantic_search": 
            # print("run semantic search...")
            search_result = azure_search_client.semantic_search(text)
        elif self.search_type == "vector_search":
            # print("run vector search...")
            search_result = azure_search_client.vector_search(text)
        elif self.search_type == "hybrid_search":
            # print("run hybrid search...")
            search_result = azure_search_client.hybrid_search(text)
        else:
            print("Invalid search type, Please check your search type is in ['semantic_search', 'vector_searc', 'hybrid_search']")
        # print(f"Search Result: {search_result}")
        #search
        
        response = llm.chat_completion(input_text= text, system_prompt=self.system_prompt.format(context=search_result))
        #response.choices[0].message.content
        return response
    
    def rag_chain_include_history(self, sess_id, session, text: str="" ):
        # print("search-type:", self.search_type)
        azure_search_client = AzureAISearch(self.config)
        llm = LLM(self.config)
        search_result = ""
        if self.search_type == "semantic_search": 
            # print("run semantic search...")
            search_result = azure_search_client.semantic_search(text)
        elif self.search_type == "vector_search":
            # print("run vector search...")
            search_result = azure_search_client.vector_search(text)
        elif self.search_type == "hybrid_search":
            # print("run hybrid search...")
            search_result = azure_search_client.hybrid_search(text)
        else:
            print("Invalid search type, Please check your search type is in ['semantic_search', 'vector_searc', 'hybrid_search']")
        # print(f"Search Result: {search_result}")
        #search
        if search_result == "":
            response = llm.chat_completion_return_history(sess_id, session, text, self.system_prompt)
        else:
            response = llm.chat_completion_return_history(sess_id, session, text, self.system_prompt.format(context=search_result))
        #response.choices[0].message.content
        return response


        


        
    