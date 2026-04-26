from typing import Dict
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from pdf_processor import PDFProcessor
from vector_store import VectorStore

load_dotenv()  # .env dosyasını yükle

# Cloud deployment için LLM handler seçimi - lazy import
LLMHandler = None


class RAGChatbot:
    """RAG mimarisi ile çalışan hukuk chatbotu"""
    
    def __init__(self):
        self.pdf_processor = PDFProcessor()
        self.vector_store = VectorStore()
        
        # LLM handler'ı lazy load et
        global LLMHandler
        if LLMHandler is None:
            if os.getenv("GROQ_API_KEY"):
                from llm_handler_cloud import LLMHandler as CloudHandler
                LLMHandler = CloudHandler
            else:
                from llm_handler import LLMHandler as LocalHandler
                LLMHandler = LocalHandler
        
        self.llm_handler = LLMHandler()
        self.questions_log_file = "questions_log.json"
        self._load_questions_log()
    
    def _load_questions_log(self):
        """Soru logunu yükle veya oluştur"""
        if os.path.exists(self.questions_log_file):
            with open(self.questions_log_file, 'r', encoding='utf-8') as f:
                self.questions_log = json.load(f)
        else:
            self.questions_log = []
    
    def _save_question(self, question: str, answer: str, sources: list, found_in_docs: bool):
        """Soruyu JSON'a kaydet"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'question': question,
            'answer': answer,
            'sources': sources,
            'found_in_docs': found_in_docs,
            'needs_research': not found_in_docs
        }
        
        self.questions_log.append(log_entry)
        
        with open(self.questions_log_file, 'w', encoding='utf-8') as f:
            json.dump(self.questions_log, f, ensure_ascii=False, indent=2)
    
    def initialize(self, force_reload: bool = False):
        """Sistemi başlatır ve PDF'leri yükler"""
        print("[INIT] RAG Chatbot baslatiliyor...")
        
        if force_reload:
            print("[INIT] PDF'ler yeniden yukleniyor...")
            self.vector_store.clear_database()
        
        # PDF'leri işle
        documents = self.pdf_processor.process_all_pdfs()
        
        if not documents:
            print("[WARN] Hic PDF bulunamadi. Lutfen 'pdfs' klasorune PDF dosyalari ekleyin.")
            return False
        
        # Vektör veritabanına ekle
        print("[INIT] Belgeler vektor veritabanina ekleniyor...")
        self.vector_store.add_documents(documents)
        
        print("[OK] Sistem hazir!")
        return True
    
    def ask(self, question: str) -> Dict:
        """Soru sorar ve cevap alır"""
        print(f"\n[Q] Soru: {question}")
        
        # İlgili belgeleri bul
        print("[SEARCH] Ilgili belgeler araniyor...")
        relevant_docs = self.vector_store.search(question)
        
        if not relevant_docs:
            answer = 'Bu konu hakkında belgelerimizde bilgi bulunamadı. Konu araştırılıp sisteme eklenecektir.'
            sources = []
            found_in_docs = False
        else:
            # Cevap üret
            print("[LLM] Cevap olusturuluyor...")
            answer = self.llm_handler.generate_response(question, relevant_docs)
            
            # Kaynakları topla
            sources = list(set([doc['metadata']['source'] for doc in relevant_docs]))
            
            # Cevabın belgede bulunup bulunmadığını kontrol et
            found_in_docs = "bulunamadı" not in answer.lower() and "araştırılıp" not in answer.lower()
        
        # Soruyu kaydet
        self._save_question(question, answer, sources, found_in_docs)
        
        return {
            'answer': answer,
            'sources': sources,
            'relevant_chunks': len(relevant_docs),
            'found_in_docs': found_in_docs
        }
    
    def chat_loop(self):
        """Interaktif sohbet döngüsü"""
        print("\n" + "="*60)
        print("[BOT] Hukuk Chatbot'a Hos Geldiniz!")
        print("="*60)
        print("Komutlar:")
        print("  - Soru sormak için yazın")
        print("  - 'çıkış' veya 'exit' yazarak çıkabilirsiniz")
        print("="*60 + "\n")
        
        while True:
            try:
                question = input("\n[SIZ] ").strip()
                
                if question.lower() in ['çıkış', 'exit', 'quit', 'q']:
                    print("[EXIT] Gorusmek uzere!")
                    break
                
                if not question:
                    continue
                
                result = self.ask(question)
                
                print(f"\n[BOT] {result['answer']}")
                print(f"\n[SRC] {', '.join(result['sources'])}")
                
            except KeyboardInterrupt:
                print("\n\n[EXIT] Gorusmek uzere!")
                break
            except Exception as e:
                print(f"\n[ERR] Hata: {e}")
