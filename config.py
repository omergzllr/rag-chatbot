import os

# Dizin yapılandırması
PDF_DIRECTORY = "pdfs"
VECTOR_DB_PATH = "vector_db"

# Model yapılandırması
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # Daha küçük ve hızlı model
LLM_MODEL = "llama3"  # Ollama ile kullanılacak model (llama2 veya llama3)

# Chunk yapılandırması
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Retrieval yapılandırması
TOP_K_RESULTS = 3
