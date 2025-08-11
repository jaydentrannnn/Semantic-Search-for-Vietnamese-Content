import numpy as np
from sentence_transformers import SentenceTransformer
from config import EMBEDDING_LLM, CHUNK_SIZE, OVERLAP  # fixed import
from src.utils import normalize  # fixed import
from pyvi import ViTokenizer

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = OVERLAP):
    words = text.split()
    if len(words) <= chunk_size:
        return [text]
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunks.append(" ".join(words[i:i + chunk_size]))
    return chunks

def embedding(header_to_contents_map: dict[str, list[str]]):
    model = SentenceTransformer(EMBEDDING_LLM, trust_remote_code=True)
    processed_data = []

    for header, contents in header_to_contents_map.items():
        print(f"Running embedding for {header}")
        embedded_header = model.encode(header)
        vectorized_contents = []
        for content in contents:
            normalized_content = normalize(content)
            tokenized = ViTokenizer.tokenize(normalized_content)
            chunk_embeddings = model.encode(chunk_text(tokenized))
            vectorized_contents.append(np.mean(chunk_embeddings, axis=0))
        for vectorized_content in vectorized_contents:
            processed_data.append({
                "header": header,
                "embedded_header": embedded_header,
                "contents": contents,
                "vectorized_contents": vectorized_content
            })
    return processed_data

def embedding_query(model: SentenceTransformer, query: str):
    return model.encode(query)
