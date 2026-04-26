import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict
from config import VECTOR_DB_PATH, EMBEDDING_MODEL, TOP_K_RESULTS


class VectorStore:
    """Vektör veritabanı yönetimi"""
    
    def __init__(self, db_path: str = VECTOR_DB_PATH):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection_name = "hukuk_belgeleri"
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        
        # Collection oluştur veya mevcut olanı al
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "Hukuk belgeleri vektör deposu"}
        )
    
    def add_documents(self, documents: List[Dict[str, str]]):
        """Belgeleri vektör veritabanına ekler"""
        from pdf_processor import PDFProcessor
        processor = PDFProcessor()
        
        all_chunks = []
        all_metadatas = []
        all_ids = []
        
        for doc_idx, doc in enumerate(documents):
            chunks = processor.chunk_text(doc['content'])
            
            for chunk_idx, chunk in enumerate(chunks):
                all_chunks.append(chunk)
                all_metadatas.append({
                    'source': doc['source'],
                    'type': doc['type'],
                    'chunk_id': chunk_idx
                })
                all_ids.append(f"{doc['source']}_{chunk_idx}")
        
        # Embedding'leri oluştur
        embeddings = self.embedding_model.encode(all_chunks).tolist()
        
        # Veritabanına ekle
        self.collection.add(
            embeddings=embeddings,
            documents=all_chunks,
            metadatas=all_metadatas,
            ids=all_ids
        )
        
        print(f"✓ {len(all_chunks)} chunk vektör veritabanına eklendi")
    
    def search(self, query: str, top_k: int = TOP_K_RESULTS) -> List[Dict]:
        """Sorguya en yakın belgeleri bulur"""
        query_embedding = self.embedding_model.encode([query]).tolist()
        
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k
        )
        
        retrieved_docs = []
        for i in range(len(results['documents'][0])):
            retrieved_docs.append({
                'content': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i]
            })
        
        return retrieved_docs
    
    def clear_database(self):
        """Veritabanını temizler"""
        self.client.delete_collection(self.collection_name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name
        )
        print("✓ Veritabanı temizlendi")
