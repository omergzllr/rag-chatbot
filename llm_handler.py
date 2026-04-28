from typing import List, Dict
from config import LLM_MODEL


class LLMHandler:
    """Yerel LLM ile etkileşim"""
    
    def __init__(self, model_name: str = LLM_MODEL):
        self.model_name = model_name
        self._ollama_client = None
        self._ollama_import_error = ""
        self._hf_pipeline = None
        self._hf_import_error = ""
        try:
            import ollama  # type: ignore

            self._ollama_client = ollama
        except Exception as exc:  # noqa: BLE001
            self._ollama_import_error = str(exc)
        try:
            from transformers import pipeline  # type: ignore

            self._hf_pipeline = pipeline(
                "text2text-generation",
                model="google/flan-t5-small",
                max_new_tokens=192,
                do_sample=False,
            )
        except Exception as exc:  # noqa: BLE001
            self._hf_import_error = str(exc)
    
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
            if self._ollama_client is None:
                raise RuntimeError("ollama kullanima uygun degil")

            response = self._ollama_client.generate(
                model=self.model_name,
                prompt=prompt
            )
            return response['response']
        except Exception as e:
            if self._hf_pipeline is not None:
                try:
                    # Flan promptu daha kisa tuttugumuzda CPU'da daha stabil calisir.
                    hf_prompt = (
                        "Sen bir hukuk asistanisin. Belgelerden cikarak kisa ve acik bir cevap ver.\n"
                        "Soru: " + query + "\n"
                        "Belgelerden ozet:\n" + context[:2400]
                    )
                    out = self._hf_pipeline(hf_prompt)
                    generated = str(out[0].get("generated_text", "")).strip() if out else ""
                    if generated and self._is_usable_generated_text(generated):
                        return generated
                except Exception:
                    pass

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
                f"Lutfen Ollama'nin calistigindan ve '{self.model_name}' modelinin yuklu oldugundan emin olun. "
                f"Eger Ollama kurulu degilse Hugging Face fallback modeli de kullanilamadi: {self._hf_import_error}"
            )

    @staticmethod
    def _is_usable_generated_text(text: str) -> bool:
        cleaned = " ".join(text.split())
        if len(cleaned) < 20:
            return False
        # Ayni token tekrarina dayali bozuk uretimleri ele.
        tokens = cleaned.lower().split()
        if len(tokens) >= 8:
            unique_ratio = len(set(tokens)) / len(tokens)
            if unique_ratio < 0.35:
                return False
        return True
    
    def check_model_availability(self) -> bool:
        """Model'in mevcut olup olmadığını kontrol eder"""
        try:
            if self._ollama_client is None:
                return False
            models = self._ollama_client.list()
            available_models = [m['name'] for m in models.get('models', [])]
            return self.model_name in available_models
        except:
            return False
