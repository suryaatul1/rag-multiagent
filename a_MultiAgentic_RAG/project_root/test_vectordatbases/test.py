import os

import certifi
import weaviate

from a_MultiAgentic_RAG.project_root.my_configs.Setting import settings

# ensure Python/urllib uses certifi's CA bundle for SSL verification
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

CUSTOM_DATA_PATH = settings.WEAVIATE_DB_PATH # Your custom persistence path
GITHUB_ENDPOINT = "https://models.github.ai/inference/embeddings"
MODEL_NAME = "openai/text-embedding-3-large"
GITHUB_TOKEN = os.environ["GH_OPENAI_TOKEN"]

client = None
try:

    client = weaviate.connect_to_embedded(
        persistence_data_path=CUSTOM_DATA_PATH,
        #additional_config=AdditionalConfig(trust_env=True),
        port=9034,  # Use a different HTTP port
        grpc_port=50063,  # Use a
        environment_variables={
            "ENABLE_API_BASED_MODULES": "true", # Enable API based modules
            "ENABLE_MODULES": 'text2vec-transformers', # We will be using a transformer model
            "TRANSFORMERS_INFERENCE_API":"http://127.0.0.1:5000/", # The endpoint the weaviate API will be using to vectorize
            #"RERANKER_INFERENCE_API":"http://127.0.0.1:5000/" # The endpoint the weaviate API will be using to rerank
        }
    )



    # vectorizer_config = [Configure.NamedVectors.text2vec_transformers(
    #             name="vector", # This is the name you will need to access the vectors of the objects in your collection
    #             source_properties=['place', 'state', 'description', 'best_season_to_visit', 'attractions', 'budget'], # which properties should be used to generate a vector, they will be appended to each other when vectorizing
    #             vectorize_collection_name = False, # This tells the client to not vectorize the collection name.
    #                                                # If True, it will be appended at the beginning of the text to be vectorized
    #             inference_url="http://127.0.0.1:5000", # Since we are using an API based vectorizer, you need to pass the URL used to make the calls
    #                                                    # This was setup in our Flask application
    #         )]

# Delete the collection in case it exists
    if client.collections.exists("example_collection"):
        client.collections.delete("example_collection")

    print(f"✅ Embedded Weaviate @ {CUSTOM_DATA_PATH}")
    #
    # if not client.collections.exists('example_collection'): # Creates only if the collection does not exist
    #     collection = client.collections.create(
    #         name='example_collection',
    #         vectorizer_config=vectorizer_config, # The config we defined before,
    #         reranker_config=Configure.Reranker.transformers(), # The reranker config
    #
    #         properties=[  # Define properties
    #         Property(name="place",vectorize_property_name=True,data_type= DataType.TEXT),
    #         Property(name="state",vectorize_property_name=True, data_type=DataType.TEXT),
    #         Property(name="description",vectorize_property_name=True, data_type=DataType.TEXT),
    #         Property(name="best_season_to_visit",vectorize_property_name=True, data_type=DataType.TEXT),
    #         Property(name="attractions",vectorize_property_name=True, data_type=DataType.TEXT),
    #         Property(name="budget",vectorize_property_name=True, data_type=DataType.TEXT),
    #         Property(name="user_ratings", data_type=DataType.NUMBER),
    #         Property(name="last_updated", data_type=DataType.DATE),
    #
    #     ]
    #     )
    # else:
    #     collection = client.collections.get("example_collection")
    #     print(collection)
    #     client.collections.list_all().keys()

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if client is not None:
        client.close()

client.collections.list_all().keys()