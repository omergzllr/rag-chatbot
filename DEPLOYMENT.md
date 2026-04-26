# 🚀 Deployment Rehberi

## Yerel Test

```bash
pip install streamlit
streamlit run app.py
```

Tarayıcıda otomatik açılacak: http://localhost:8501

---

## 🌐 Render'a Deploy (ÖNERİLEN)

### 1. GitHub'a Yükle

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/KULLANICI_ADINIZ/hukuk-rag-chatbot.git
git push -u origin main
```

### 2. Render'da Proje Oluştur

1. https://render.com adresine git
2. "New +" → "Web Service" seç
3. GitHub repo'nuzu bağla
4. Ayarlar:
   - **Name:** hukuk-rag-chatbot
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
   - **Instance Type:** Free

5. "Create Web Service" tıkla

### 3. Ortam Değişkenleri (Opsiyonel)

Render dashboard'da Environment sekmesinden:
- `PYTHON_VERSION`: 3.11.7

---

## ⚠️ ÖNEMLİ NOTLAR

### Ollama Sorunu
Render ücretsiz planında Ollama çalıştıramazsınız. İki seçenek:

#### Seçenek A: OpenAI API Kullan (Önerilen)
`llm_handler.py` dosyasını düzenle:

```python
import openai

class LLMHandler:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def generate_response(self, query: str, context_docs: List[Dict]) -> str:
        context = "\n\n".join([
            f"Kaynak: {doc['metadata']['source']}\n{doc['content']}"
            for doc in context_docs
        ])
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sen bir hukuk asistanısın."},
                {"role": "user", "content": f"BELGELER:\n{context}\n\nSORU: {query}"}
            ]
        )
        return response.choices[0].message.content
```

Render'da Environment Variable ekle:
- `OPENAI_API_KEY`: sk-...

#### Seçenek B: Hugging Face API (Ücretsiz)
```python
from huggingface_hub import InferenceClient

class LLMHandler:
    def __init__(self):
        self.client = InferenceClient(token=os.getenv("HF_TOKEN"))
    
    def generate_response(self, query: str, context_docs: List[Dict]) -> str:
        # ... context hazırla
        response = self.client.text_generation(
            prompt=f"BELGELER:\n{context}\n\nSORU: {query}",
            model="mistralai/Mistral-7B-Instruct-v0.2"
        )
        return response
```

---

## 🎯 Alternatif: Streamlit Cloud (En Kolay)

1. https://streamlit.io/cloud
2. GitHub repo'nuzu bağla
3. Deploy!

**Avantajlar:**
- Çok kolay
- Ücretsiz
- Otomatik güncelleme

**Dezavantajlar:**
- Ollama çalıştıramaz
- API gerekir

---

## 📊 Performans İpuçları

1. **Vektör DB'yi Cache'le:**
   - İlk yüklemede oluştur
   - Sonraki çalıştırmalarda kullan

2. **PDF'leri Önceden İşle:**
   - Build sırasında işle
   - Runtime'da tekrar işleme

3. **Model Boyutunu Küçült:**
   - Daha küçük embedding modeli kullan
   - `all-MiniLM-L6-v2` gibi

---

## 🆘 Sorun Giderme

**Hata: "Port already in use"**
```bash
streamlit run app.py --server.port=8502
```

**Hata: "Module not found"**
```bash
pip install -r requirements.txt
```

**Hata: "Out of memory"**
- Daha küçük model kullan
- Chunk size'ı küçült
