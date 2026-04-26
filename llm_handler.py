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
            # Ollama ayakta degilse kullaniciya teknik hata yerine
            # bulunan kaynaklardan kisa bir ozet don.
            snippets = []
            for doc in context_docs[:3]:
                src = doc.get("metadata", {}).get("source", "Bilinmeyen kaynak")
                text = str(doc.get("content", "")).replace("\n", " ").strip()
                if text:
                    snippets.append(f"- {src}: {text[:280]}...")

            if snippets:
                return (
                    "Otomatik model servisine su an baglanilamiyor. "
                    "Asagida ilgili kaynaklardan ozet bolumler yer aliyor:\n\n"
                    + "\n".join(snippets)
                )

            return (
                f"LLM hatasi: {e}\n\n"
                f"Lutfen Ollama'nin calistigindan ve '{self.model_name}' modelinin yuklu oldugundan emin olun."
            )
    
    def check_model_availability(self) -> bool:
        """Model'in mevcut olup olmadığını kontrol eder"""
        try:
            models = ollama.list()
            available_models = [m['name'] for m in models.get('models', [])]
            return self.model_name in available_models
        except:
            return False
