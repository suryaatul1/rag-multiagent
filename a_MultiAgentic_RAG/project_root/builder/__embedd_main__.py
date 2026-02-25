from a_MultiAgentic_RAG.project_root.builder.embedding_model import EmbeddingModel

obj = EmbeddingModel()
model= obj.get_embedding()

texts = ["first phrase", "second phrase", "third phrase"]
embedded_docs = model.embed_documents(texts)

# Print embedding details (matches your original output format)
for i, embedding in enumerate(embedded_docs):
    length = len(embedding)
    print(
        f"data[{i}]: length={length}, "
        f"[{embedding[0]}, {embedding[1]}, "
        f"..., {embedding[length-2]}, {embedding[length-1]}]"
    )
