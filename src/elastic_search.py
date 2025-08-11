from elasticsearch import Elasticsearch
from config import INDEX_SETTINGS, INDEX_NAME, MAPPING, TOP_K, CANDIDATES
from src.utils import clean_soup, get_soup, get_h3_and_content
from src.embedding import embedding

def setup_client(client: Elasticsearch):
    if not client.indices.exists(index=INDEX_NAME):
        client.indices.create(index=INDEX_NAME, settings=INDEX_SETTINGS, mappings=MAPPING)

def index_data(client: Elasticsearch, data: list):
    for i, item in enumerate(data):
        client.index(index=INDEX_NAME, id=i, document=item)
    client.indices.refresh(index=INDEX_NAME)

def index_data_from_link(client: Elasticsearch, url: str):
    soup = clean_soup(get_soup(url))
    h3_map = get_h3_and_content(soup)
    embedded_map = embedding(h3_map)
    index_data(client, embedded_map)

def semantic_search(client: Elasticsearch, query: str, embedded_query: list):
    knn_query = [
        {
            "field": "embedded_header",
            "query_vector": embedded_query,
            "k": TOP_K,
            "num_candidates": CANDIDATES,
            "boost": 2.0
        },
        {
            "field": "vectorized_contents",
            "query_vector": embedded_query,
            "k": TOP_K,
            "num_candidates": CANDIDATES
        }
    ]
    text_query = {
        "multi_match": {
            "query": query,
            "fields": ["header", "contents"],
            "fuzziness": "AUTO"
        }
    }
    return client.search(index=INDEX_NAME, query=text_query, knn=knn_query, _source=["header", "contents"])
