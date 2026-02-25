
import os
from langchain_azure_ai.embeddings import AzureAIEmbeddingsModel
from azure.core.credentials import AzureKeyCredential

endpoint = "https://models.github.ai/inference"
model_name = "openai/text-embedding-3-large"
token = os.environ["GH_OPENAI_TOKEN"]

# Create LangChain embeddings model (wraps your original EmbeddingsClient)
embeddings = AzureAIEmbeddingsModel(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
    model=model_name  # Equivalent to your client.embed(model=...)
)


# Embed documents (same input/output behavior as your original code)
texts = ["first phrase", "second phrase", "third phrase"]
embedded_docs = embeddings.embed_documents(texts)

# Print embedding details (matches your original output format)
for i, embedding in enumerate(embedded_docs):
    length = len(embedding)
    print(
        f"data[{i}]: length={length}, "
        f"[{embedding[0]}, {embedding[1]}, "
        f"..., {embedding[length-2]}, {embedding[length-1]}]"
    )


# Usage info (via LangChain's prompt_tokens, completion_tokens, total_tokens)
# print(f"Usage: prompt_tokens={embeddings.prompt_tokens}, "
#       f"completion_tokens={embeddings.completion_tokens}, "
#       f"total_tokens={embeddings.total_tokens}")