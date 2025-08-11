from elasticsearch import Elasticsearch
from config import API_KEY, EMBEDDING_LLM
from src.embedding import embedding_query
from src.utils import normalize
from src.elastic_search import semantic_search
from sentence_transformers import SentenceTransformer

def main_search():
    client = Elasticsearch(
        "https://my-elasticsearch-project-ec8520.es.us-east-1.aws.elastic.cloud:443",
        api_key=API_KEY
    )
    model = SentenceTransformer(EMBEDDING_LLM, trust_remote_code=True)

    query = ""
    while query != "quit":
        query = input("Enter query: ")
        if query.strip().lower() == "quit":
            break
        embedded_normalized_query = embedding_query(model, normalize(query))
        result = semantic_search(client, query, embedded_normalized_query)

        print("\n--- Top Search Results ---")
        if not result['hits']['hits']:
            print("No results found.")
        for hit in result['hits']['hits']:
            print(f"Similarity Score: {hit['_score']:.4f}")
            print(f"Header: {hit['_source']['header']}")
            print(f"Matching Content: {hit['_source']['contents']}")
            print("-" * 25)

if __name__ == "__main__":
    main_search()
