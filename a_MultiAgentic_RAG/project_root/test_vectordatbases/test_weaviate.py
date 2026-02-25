import os

import weaviate
from weaviate.classes.config import Configure
from weaviate.collections.classes.config import Property, DataType
from weaviate.config import AdditionalConfig

from a_MultiAgentic_RAG.project_root.my_configs.Setting import settings

CUSTOM_DATA_PATH = settings.WEAVIATE_DB_PATH # Your custom persistence path
GITHUB_ENDPOINT = "https://models.github.ai/inference/embeddings"
MODEL_NAME = "openai/text-embedding-3-large"
GITHUB_TOKEN = os.environ["GH_OPENAI_TOKEN"]

additional_config=AdditionalConfig(trust_env=False)

client = weaviate.connect_to_embedded(
        persistence_data_path=CUSTOM_DATA_PATH,
         additional_config,

        environment_variables={

            "ENABLE_API_BASED_MODULES": "true", # Enable API based modules
            "ENABLE_MODULES": 'text2vec-transformers, reranker-transformers ', # We will be using a transformer model
            #"TRANSFORMERS_INFERENCE_API":"http://127.0.0.1:5000/", # The endpoint the weaviate API will be using to vectorize
            #"RERANKER_INFERENCE_API":"http://127.0.0.1:5000/" # The endpoint the weaviate API will be using to rerank

        }
    )

vectorizer_config = [Configure.NamedVectors.text2vec_transformers(
                name="vector", # This is the name you will need to access the vectors of the objects in your collection
                source_properties=['chunk_id', 'chunk_data'], # which properties should be used to generate a vector, they will be appended to each other when vectorizing
                vectorize_collection_name = False # This tells the client to not vectorize the collection name.
                                                   # If True, it will be appended at the beginning of the text to be vectorized
            )]


if not client.collections.exists('example_collection'): # Creates only if the collection does not exist
    collection = client.collections.create(
            name='example_collection',
            vectorizer_config=vectorizer_config, # The config we defined before,
            reranker_config=Configure.Reranker.transformers(), # The reranker config

            properties=[  # Define properties
            Property(name="chunk_id",vectorize_property_name=True,data_type= DataType.TEXT),
            Property(name="chunk_data",vectorize_property_name=True, data_type=DataType.TEXT),
                       ]
        )
else:
    collection = client.collections.get("example_collection")

print(collection)