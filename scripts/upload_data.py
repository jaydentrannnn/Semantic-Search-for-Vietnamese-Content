from src.utils import clean_soup, get_soup, get_h3_and_content
from config import PAGE_URL, API_KEY
from src.elastic_search import index_data, setup_client
from src.embedding import embedding
from elasticsearch import Elasticsearch

def main_index():
    client = Elasticsearch(
        "https://my-elasticsearch-project-ec8520.es.us-east-1.aws.elastic.cloud:443",
        api_key=API_KEY
    )
    setup_client(client)
    soup = clean_soup(get_soup(PAGE_URL))
    h3_map = get_h3_and_content(soup)
    embedded_map = embedding(h3_map)
    index_data(client, embedded_map)

if __name__ == '__main__':
    main_index()
