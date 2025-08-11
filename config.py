import os

PAGE_URL = "https://vi.wikipedia.org/wiki/L%E1%BB%8Bch_s%E1%BB%AD_Vi%E1%BB%87t_Nam"
CONTENT_TAGS = ['p', 'ul', 'ol', 'blockquote', 'dl', 'div']

# Embedding
EMBEDDING_LLM = 'dangvantuan/vietnamese-document-embedding'
CHUNK_SIZE = 1024
OVERLAP = 128

# Elasticsearch
API_KEY = os.getenv("ELASTIC_API_KEY")  # Load from env var
INDEX_NAME = "doc-search"

INDEX_SETTINGS = {
    "analysis": {
        "analyzer": {
            "vietnamese_analyzer": {
                "tokenizer": "icu_tokenizer",
                "filter": [
                    "lowercase",
                    "vietnamese_stop",
                    "icu_folding"
                ]
            }
        },
        "filter": {
            "vietnamese_stop": {
                "type": "stop",
                "stopwords": "_vietnamese_"
            }
        }
    }
}

MAPPING = {
    "properties": {
        "header": {
            "type": "text",
            "fields": {
                "keyword": {
                    "type": "keyword",
                }
            }
        },
        "embedded_header": {
            "type": "dense_vector",
            "dims": 768,
            "index": True,
            "similarity": "cosine"
        },
        "contents": {
            "type": "text",
        },
        "vectorized_contents": {
            "type": "dense_vector",
            "dims": 768,
            "index": True,
            "similarity": "cosine"
        }
    }
}

# Semantic Search
TOP_K = 3
CANDIDATES = 27
