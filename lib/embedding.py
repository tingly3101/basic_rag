from openai import AzureOpenAI
import os

class Embedding():

    def __init__(self, config):
        self.open_ai_endpoint = config["llm"]["azure-open-ai"]["endpoint"]
        self.open_ai_key = config["llm"]["azure-open-ai"]["api-key"]
        self.open_ai_api_version = config["llm"]["azure-open-ai"]["api-version"]
    def get_credential(self):
        return {'endpoint': self.open_ai_endpoint, 
                'api-key': self.open_ai_key,
                }

    def get_embeddings(self, text: str):
        # There are a few ways to get embeddings. This is just one example.
        client = AzureOpenAI(
            azure_endpoint = self.open_ai_endpoint,
            api_key = self.open_ai_key,
            api_version = self.open_ai_api_version,
        )
        embedding = client.embeddings.create(input=text, model = "deploy-text-embedding-ada-002")

        return embedding.data[0].embedding