"""
Cloud deployment için OpenAI kullanan LLM Handler
"""
import os
from typing import List, Dict
from openai import OpenAI


class LLMHandler:
    """OpenAI API ile LLM etkileşimi"""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable bulunamadı!")
        
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-3.5-turbo"
    
    def generate_response(self, query: str, context_docs: List[Dict]) -> str:
        """Bağlam ve sorguya göre cevap üretir"""
        
        # Bağlamı hazırla
        context = "\n\n".join([
            f"Kaynak: {doc['metadata']['source']}\n{doc['content']}"
            for doc in context_docs
        ])
        
        # Prompt oluştur
        system_prompt = """Sen bir hukuk asistanısın. Aşağıdaki belgelerden yararlanarak soruyu kısa ve net şekilde yanıtla.

ÖNEMLİ: Eğer belgelerde cevap bulamazsan şunu yaz: "Bu konu hakkında belgelerimizde bilgi bulunamadı. Konu araştırılıp sisteme eklenecektir."
"""
        
        user_prompt = f"""BELGELER:
{context}

SORU: {query}

CEVAP:"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"API hatası: {e}\n\nLütfen OPENAI_API_KEY'in doğru ayarlandığından emin olun."
    
    def check_model_availability(self) -> bool:
        """API'nin çalışıp çalışmadığını kontrol eder"""
        try:
            self.client.models.list()
            return True
        except:
            return False
