# Vietnamese Wikipedia Semantic Search

This project builds a **semantic + keyword search engine** for Vietnamese Wikipedia articles using **Elasticsearch** and **SentenceTransformers embeddings**.  
It automatically scrapes Wikipedia content, splits it into chunks, embeds the text into vector representations, and stores them in Elasticsearch for **fast and accurate search**.

---

## 🚀 Features
- **Web Scraping**: Extracts content under `<h3>` headings from Vietnamese Wikipedia.
- **Text Cleaning & Normalization**: Removes noise, standardizes text, and prepares it for indexing.
- **Text Embedding**: Uses [`dangvantuan/vietnamese-document-embedding`](https://huggingface.co/dangvantuan/vietnamese-document-embedding) for semantic vector representation.
- **Semantic Search**: Retrieves results by meaning, not just exact keyword match.
- **Keyword Search**: Uses Vietnamese analyzer with stopword removal and fuzzy matching.
- **Dual-Search Strategy**: Combines semantic and traditional text search for best accuracy.

## 📂 Project Structure
```markdown
ElasticSearch/
├── README.md
├── requirements.txt
├── config.py                 # Global settings (URL, model, ES index)
├── src/                      # Core modules
│   ├── utils.py              # Scraping & text processing utilities
│   ├── embedding.py          # Text chunking & embedding functions
│   ├── elastic_search.py     # Elasticsearch setup, indexing, and search
├── scripts/                  # Executable scripts
│   ├── upload_data.py        # Scrapes + indexes Wikipedia content
│   ├── search.py             # Interactive search CLI
└── data/                     # (Optional) Store raw HTML or sample results
```


***

## ⚙️ Setup \& Installation


***

## ⚙️ Setup \& Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/wikivn-search.git
cd wikivn-search
```


### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```


### 3️⃣ Set environment variables

Create a .env file or export variables:

```bash
export ELASTIC_API_KEY="your_api_key_here"
```


***

## 📊 Usage

### Upload Data to Elasticsearch

```bash
python scripts/upload_data.py
```


### Search Interactively

```bash
python scripts/search.py
```

Example search:

```text
Enter query: lịch sử triều Nguyễn
--- Top Search Results ---
Similarity Score: 12.4532
Header: Triều Nguyễn
Matching Content: Triều Nguyễn là triều đại phong kiến cuối cùng...
-------------------------
```


***

## 🧠 How It Works

- Scraping: Gets Wikipedia HTML, extracts text from specific tags, and maps headings to their content.
- Embedding: Converts text into 768-dimensional vectors using SentenceTransformers.
- Indexing: Stores both text and vectors in Elasticsearch with a Vietnamese analyzer.
- Searching:
    - KNN Vector Search for semantic meaning.
    - Multi-Match Query for keyword relevance.
    - Merged results for balanced accuracy.

***

## 📌 Requirements

- Python 3.9+
- Elasticsearch 8+
- Dependencies (see requirements.txt):
    - beautifulsoup4
    - requests
    - elasticsearch
    - sentence-transformers
    - pyvi
    - numpy
