"""
Cloud deployment için Groq API kullanan LLM Handler (Ücretsiz ve Hızlı)
"""
import os
from typing import List, Dict
import requests


class LLMHandler:
    """Groq API ile LLM etkileşimi"""
    
    def __init__(self):
        # Groq API key - ücretsiz: https://console.groq.com/keys
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable bulunamadı!")
        
        self.api_key = api_key
        self.model = "llama-3.1-70b-versatile"  # Ücretsiz ve güçlü model
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
    
    def generate_response(self, query: str, context_docs: List[Dict]) -> str:
        """Bağlam ve sorguya göre cevap üretir"""
        
        # Bağlamı hazırla
        context = "\n\n".join([
            f"Kaynak: {doc['metadata']['source']}\n{doc['content']}"
            for doc in context_docs
        ])
        
        # Prompt oluştur
        system_prompt = """Sen bir hukuk asistanısın. Aşağıdaki belgelerden yararlanarak soruyu Türkçe olarak kısa ve net şekilde yanıtla.

ÖNEMLİ: Eğer belgelerde cevap bulamazsan şunu yaz: "Bu konu hakkında belgelerimizde bilgi bulunamadı. Konu araştırılıp sisteme eklenecektir."
"""
        
        user_prompt = f"""BELGELER:
{context}

SORU: {query}

CEVAP (Türkçe):"""
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 500,
                "top_p": 1,
                "stream": False
            }
            
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=30)
            
            # Hata detaylarını göster
            if response.status_code != 200:
                error_detail = response.text
                return f"API Hatası ({response.status_code}): {error_detail}"
            
            result = response.json()
            return result['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException as e:
            return f"İstek hatası: {str(e)}"
        except Exception as e:
            return f"Beklenmeyen hata: {str(e)}"
    
    def check_model_availability(self) -> bool:
        """API'nin çalışıp çalışmadığını kontrol eder"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            response = requests.get("https://api.groq.com/openai/v1/models", headers=headers, timeout=10)
            return response.status_code == 200
        except:
            return False
