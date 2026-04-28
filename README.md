# Hukuk RAG Chatbot

Tamamen yerel çalışan veya cloud'da deploy edilebilen RAG (Retrieval-Augmented Generation) mimarisi ile hukuk chatbotu.

## 🚀 Hızlı Başlangıç

### Yerel Kullanım (Ollama)
```bash
pip install -r requirements.txt
ollama pull llama3
streamlit run app.py
```

### Profesyonel Web Stack (Next.js + Python API)
```bash
# 1) Python API
pip install -r requirements.txt
python api_server.py

# 2) Yeni web arayuzu
cd web
npm install
npm run dev
```

### Windows Notu (python komutu calismiyorsa)
Bu depoda backend calismasi icin gercek Python kurulumuna ihtiyac vardir. Eger `python` veya `py` komutu "Sistem dosyaya erisemiyor" benzeri hata verirse:

1. Python 3.11+ kurun (resmi installer)
2. Kurulumda `Add python.exe to PATH` secenegini aktif edin
3. Yeni terminalde dogrulayin:
```bash
python --version
pip --version
```
4. Ardindan:
```bash
pip install -r requirements.txt
python api_server.py
```

LLM secimi:
- Cloud: `GROQ_API_KEY` tanimliysa Groq modeli kullanilir
- Lokal: `GROQ_API_KEY` yoksa Ollama kullanilir (`ollama` paketi + yüklü model gerekir)

### Cloud Deployment (Streamlit Cloud)
1. OpenAI API key al: https://platform.openai.com/api-keys
2. GitHub'a yükle
3. Streamlit Cloud'a deploy et: https://share.streamlit.io
4. Secrets'e API key ekle

Detaylı rehber: [QUICKSTART.md](QUICKSTART.md)

## Özellikler

- ✅ PDF'lerden otomatik bilgi çıkarma
- ✅ Yerel embedding modeli (Türkçe destekli)
- ✅ Vektör veritabanı (ChromaDB)
- ✅ Yerel LLM (Ollama) veya Cloud API (OpenAI)
- ✅ Web arayüzü (Streamlit)
- ✅ Soru loglama ve analiz
- ✅ API gerektirmeyen tam offline çalışma (yerel mod)

## Kurulum

### 1. Python Bağımlılıkları

```bash
pip install -r requirements.txt
```

### 2. Ollama Kurulumu

Ollama'yı indirin ve kurun: https://ollama.ai

Ardından bir model indirin:
```bash
ollama pull llama2
# veya Türkçe için daha iyi:
ollama pull llama3
```

### 3. PDF'leri Ekleyin

`pdfs` klasörüne hukuk belgelerinizi (PDF formatında) ekleyin.

## Kullanım

### İlk Çalıştırma (PDF'leri yükle)

```bash
python main.py --reload
```

### İnteraktif Mod

```bash
python main.py
```

### Tek Soru Modu

```bash
python main.py --query "Kira sözleşmesi feshi için gerekli şartlar nelerdir?"
```

## Yapılandırma

`config.py` dosyasından ayarları değiştirebilirsiniz:

- `EMBEDDING_MODEL`: Embedding modeli (Türkçe destekli)
- `LLM_MODEL`: Ollama model adı
- `CHUNK_SIZE`: Metin parça boyutu
- `TOP_K_RESULTS`: Kaç belge getirilecek

## Mimari

```
PDF Dosyaları
    ↓
PDF İşleme (PyPDF2)
    ↓
Metin Parçalama (Chunking)
    ↓
Embedding (Sentence Transformers)
    ↓
Vektör Veritabanı (ChromaDB)
    ↓
Soru → Benzerlik Arama → İlgili Belgeler
    ↓
LLM (Ollama) → Cevap
```

## Notlar

- İlk çalıştırmada embedding modeli otomatik indirilir (~500MB)
- Ollama modellerini önceden indirmeniz önerilir
- Türkçe için `llama3` veya `mistral` modelleri önerilir
