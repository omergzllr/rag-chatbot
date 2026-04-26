# 🚀 Streamlit Cloud Deployment (En Kolay Yöntem)

## Adım 1: GitHub'a Yükle

```bash
git init
git add .
git commit -m "Hukuk RAG Chatbot"
git branch -M main
git remote add origin https://github.com/KULLANICI_ADINIZ/hukuk-rag-chatbot.git
git push -u origin main
```

## Adım 2: Streamlit Cloud'a Deploy

1. **https://share.streamlit.io** adresine git
2. GitHub ile giriş yap
3. "New app" butonuna tıkla
4. Ayarlar:
   - **Repository:** hukuk-rag-chatbot
   - **Branch:** main
   - **Main file path:** app.py
5. "Deploy!" tıkla

✅ 2-3 dakika içinde canlıya alınır!

---

## ⚠️ ÖNEMLİ: Ollama Sorunu

Streamlit Cloud'da Ollama çalışmaz. API kullanmanız gerekir.

### Çözüm: OpenAI API (Önerilen)

1. **OpenAI API Key Al:**
   - https://platform.openai.com/api-keys
   - "Create new secret key" tıkla
   - Key'i kopyala (sk-...)

2. **Streamlit Cloud'da Secret Ekle:**
   - App ayarlarına git
   - "Secrets" sekmesi
   - Şunu ekle:
   ```toml
   OPENAI_API_KEY = "sk-your-key-here"
   ```

3. **Kodu Güncelle:**

Aşağıdaki dosyayı oluştur:

