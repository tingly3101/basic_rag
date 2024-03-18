from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from lib.embedding import Embedding



class AzureAISearch():

    def __init__(self, config) -> None:
        self.endpoint = config["ai-search"]["endpoint"]
        self.index_name = config["ai-search"]["index-name"]
        self.credential = AzureKeyCredential(config["ai-search"]["api-key"])
        self.search_client = SearchClient(self.endpoint, self.index_name, self.credential)
        self.embedding = Embedding(config)

    def semantic_search(self, query: str):

        results = list(self.search_client.search(search_text=query,
                                                select=["restaurant_name", "restaurant_desc", "keyword", "location", "promotion_desc"],
                                                logging_enable=True))
        if len(results) > 0:
            most_relevence = results[0]
            return f"ร้านอาหาร: {most_relevence['restaurant_name']}\nLocation: {most_relevence['location']}\n{most_relevence['restaurant_desc']}\nโปรโมชั่น: {most_relevence['promotion_desc']}"
        else:
            return ""
    
    def vector_search(self, query: str):
        vector_query = VectorizedQuery(
            vector = self.embedding.get_embeddings(query),
            k_nearest_neighbors=3,
            fields="restaurant_desc_embedding"
        )

        results = list(self.search_client.search(
            search_text = "",
            vector_queries = [vector_query],
            select = ["restaurant_name", "restaurant_desc", "keyword", "location", "promotion_desc"],))

        if len(results) > 0:
            most_relevence = results[0]
            return f"ร้านอาหาร: {most_relevence['restaurant_name']}\nLocation: {most_relevence['location']}\n{most_relevence['restaurant_desc']}\nโปรโมชั่น: {most_relevence['promotion_desc']}"
        else:
            return ""
        
    def hybrid_search(self, query):

        vector_query = VectorizedQuery(
            vector = self.embedding.get_embeddings(query),
            k_nearest_neighbors=3,
            fields="restaurant_desc_embedding"
        )

        results = list(self.search_client.search(
            search_text=query,
            vector_queries=[vector_query],
            select = ["restaurant_name", "restaurant_desc", "keyword", "location", "promotion_desc"],
        ))

        if len(results) > 0:
            most_relevence = results[0]
            return f"ร้านอาหาร: {most_relevence['restaurant_name']}\nLocation: {most_relevence['location']}\n{most_relevence['restaurant_desc']}\nโปรโมชั่น: {most_relevence['promotion_desc']}"
        else:
            return ""
    


