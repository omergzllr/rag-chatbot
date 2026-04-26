import ollama
from typing import List, Dict
from config import LLM_MODEL


class LLMHandler:
    """Yerel LLM ile etkileşim"""
    
    def __init__(self, model_name: str = LLM_MODEL):
        self.model_name = model_name
    
    def generate_response(self, query: str, context_docs: List[Dict]) -> str:
        """Bağlam ve sorguya göre cevap üretir"""
        
        # Bağlamı hazırla
        context = "\n\n".join([
            f"Kaynak: {doc['metadata']['source']}\n{doc['content']}"
            for doc in context_docs
        ])
        
        # Prompt oluştur
        prompt = f"""Sen bir hukuk asistanısın. Aşağıdaki belgelerden yararlanarak soruyu kısa ve net şekilde yanıtla.

ÖNEMLİ: Eğer belgelerde cevap bulamazsan şunu yaz: "Bu konu hakkında belgelerimizde bilgi bulunamadı. Konu araştırılıp sisteme eklenecektir."

BELGELER:
{context}

SORU: {query}

CEVAP:"""
        
        try:
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt
            )
            return response['response']
        except Exception as e:
            return f"LLM hatası: {e}\n\nLütfen Ollama'nın çalıştığından ve '{self.model_name}' modelinin yüklü olduğundan emin olun."
    
    def check_model_availability(self) -> bool:
        """Model'in mevcut olup olmadığını kontrol eder"""
        try:
            models = ollama.list()
            available_models = [m['name'] for m in models.get('models', [])]
            return self.model_name in available_models
        except:
            return False
