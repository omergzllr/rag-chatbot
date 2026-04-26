# 🚀 Hızlı Başlangıç - Streamlit Cloud

## 📋 Ön Hazırlık (5 dakika)

### 1. OpenAI API Key Al
1. https://platform.openai.com/api-keys adresine git
2. "Create new secret key" tıkla
3. Key'i kopyala (sk-...)
4. Güvenli bir yere kaydet

### 2. GitHub Repo Oluştur
```bash
# Projeyi GitHub'a yükle
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/KULLANICI_ADINIZ/hukuk-rag-chatbot.git
git push -u origin main
```

---

## 🌐 Streamlit Cloud'a Deploy (2 dakika)

### Adım 1: Streamlit Cloud'a Git
https://share.streamlit.io

### Adım 2: GitHub ile Giriş Yap

### Adım 3: New App
1. "New app" butonuna tıkla
2. Ayarlar:
   - **Repository:** hukuk-rag-chatbot
   - **Branch:** main
   - **Main file path:** app.py

### Adım 4: Secrets Ekle
"Advanced settings" → "Secrets" sekmesi

Şunu yapıştır:
```toml
OPENAI_API_KEY = "sk-your-actual-key-here"
```

### Adım 5: Deploy!
"Deploy!" butonuna tıkla

✅ 2-3 dakika içinde canlıya alınır!

---

## 🧪 Yerel Test (Opsiyonel)

### OpenAI API ile test:
```bash
# .streamlit/secrets.toml oluştur
mkdir .streamlit
echo 'OPENAI_API_KEY = "sk-..."' > .streamlit/secrets.toml

# Çalıştır
streamlit run app.py
```

### Ollama ile test (yerel):
```bash
# Ollama'yı başlat
ollama serve

# Başka terminalde
streamlit run app.py
```

---

## 💰 Maliyet

**OpenAI API (gpt-3.5-turbo):**
- ~$0.0015 per 1K tokens
- Ortalama soru: ~500 tokens
- **~$0.0007 per soru**
- 1000 soru ≈ $0.70

**Ücretsiz Alternatif:**
- Hugging Face Inference API (ücretsiz ama yavaş)
- Groq API (ücretsiz, hızlı)

---

## 🔧 Sorun Giderme

**Hata: "OPENAI_API_KEY not found"**
- Secrets'i doğru eklediniz mi?
- Streamlit Cloud'da app'i yeniden başlatın

**Hata: "Rate limit exceeded"**
- OpenAI API limitiniz dolmuş
- Biraz bekleyin veya ücretli plana geçin

**Hata: "Module not found"**
- requirements.txt'i kontrol edin
- Streamlit Cloud'da rebuild yapın

---

## 📊 Sonraki Adımlar

1. ✅ Deploy tamamlandı
2. 📱 Mobil uyumlu test et
3. 📚 Daha fazla PDF ekle
4. 🎨 Arayüzü özelleştir
5. 📈 Kullanım istatistiklerini izle

---

## 🆘 Yardım

Sorun mu yaşıyorsunuz?
- Streamlit Docs: https://docs.streamlit.io
- OpenAI Docs: https://platform.openai.com/docs
- GitHub Issues: Repo'nuzda issue açın
