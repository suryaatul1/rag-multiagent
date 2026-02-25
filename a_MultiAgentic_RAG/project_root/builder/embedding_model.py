import os

from azure.core.credentials import AzureKeyCredential
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel
from langchain_azure_ai.embeddings import AzureAIEmbeddingsModel


class EmbeddingModel:
    def __init__(self, embedding_model_name="openai/text-embedding-3-large"):
        self._embedding_model_name = embedding_model_name
        self._embedding_model = self.load_embedding_model()


    def load_embedding_model(self):

        endpoint = "https://models.github.ai/inference"
        token = os.environ["GH_OPENAI_TOKEN"]

    # Create LangChain embeddings model (wraps your original EmbeddingsClient)
        embeddings = AzureAIEmbeddingsModel(
            endpoint=endpoint,
            credential=AzureKeyCredential(token),
            model=self._embedding_model_name
        )
        return embeddings

    def get_embedding(self):
        # Generate embeddings for the given text using the loaded model
        # This is a placeholder implementation. You can replace it with actual embedding generation code.
        return self._embedding_model


