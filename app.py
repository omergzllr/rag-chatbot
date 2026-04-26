import streamlit as st
import json
import os
from datetime import datetime

# Cloud deployment için LLM handler seçimi
if os.getenv("OPENAI_API_KEY"):
    from llm_handler_cloud import LLMHandler
    from rag_chatbot import RAGChatbot
    USE_CLOUD = True
else:
    from rag_chatbot import RAGChatbot
    USE_CLOUD = False

# Sayfa yapılandırması
st.set_page_config(
    page_title="Hukuk RAG Chatbot",
    page_icon="⚖️",
    layout="wide"
)

# CSS ile özelleştirme
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .bot-message {
        background-color: #f5f5f5;
        border-left: 4px solid #4caf50;
    }
    .source-tag {
        display: inline-block;
        background-color: #fff3cd;
        padding: 0.2rem 0.5rem;
        border-radius: 0.3rem;
        margin: 0.2rem;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# Session state başlatma
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = None
    st.session_state.initialized = False
    st.session_state.chat_history = []

# Başlık
if USE_CLOUD:
    st.markdown('<h1 class="main-header">⚖️ Hukuk RAG Chatbot (Cloud)</h1>', unsafe_allow_html=True)
    st.info("☁️ OpenAI API kullanılıyor")
else:
    st.markdown('<h1 class="main-header">⚖️ Hukuk RAG Chatbot</h1>', unsafe_allow_html=True)
    st.info("🏠 Ollama (Yerel) kullanılıyor")

# Sidebar
with st.sidebar:
    st.header("📊 İstatistikler")
    
    # Soru logunu oku
    if os.path.exists("questions_log.json"):
        with open("questions_log.json", 'r', encoding='utf-8') as f:
            questions_log = json.load(f)
        
        total_questions = len(questions_log)
        needs_research = sum(1 for q in questions_log if q.get('needs_research', False))
        found_in_docs = total_questions - needs_research
        
        st.metric("Toplam Soru", total_questions)
        st.metric("Belgede Bulunan", found_in_docs)
        st.metric("Araştırılacak", needs_research)
        
        if st.button("🔄 Soru Logunu Temizle"):
            os.remove("questions_log.json")
            st.success("Log temizlendi!")
            st.rerun()
    else:
        st.info("Henüz soru sorulmadı")
    
    st.divider()
    
    st.header("⚙️ Ayarlar")
    if st.button("🔄 Sistemi Yeniden Başlat"):
        st.session_state.chatbot = None
        st.session_state.initialized = False
        st.session_state.chat_history = []
        st.success("Sistem yeniden başlatıldı!")
        st.rerun()
    
    if st.button("📚 PDF'leri Yeniden Yükle"):
        if st.session_state.chatbot:
            with st.spinner("PDF'ler yeniden yükleniyor..."):
                st.session_state.chatbot.initialize(force_reload=True)
            st.success("PDF'ler yeniden yüklendi!")

# Ana içerik
col1, col2 = st.columns([2, 1])

with col1:
    st.header("💬 Sohbet")
    
    # Chatbot'u başlat
    if not st.session_state.initialized:
        with st.spinner("🚀 Sistem başlatılıyor..."):
            try:
                st.session_state.chatbot = RAGChatbot()
                success = st.session_state.chatbot.initialize()
                if success:
                    st.session_state.initialized = True
                    st.success("✅ Sistem hazır!")
                else:
                    st.error("❌ PDF bulunamadı. Lütfen 'pdfs' klasörüne PDF ekleyin.")
            except Exception as e:
                st.error(f"❌ Hata: {e}")
    
    # Chat geçmişini göster
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            st.markdown(f'<div class="chat-message user-message">👤 <b>Siz:</b> {message["content"]}</div>', 
                       unsafe_allow_html=True)
        else:
            sources_html = ""
            if message.get('sources'):
                sources_html = "<br>📚 " + " ".join([f'<span class="source-tag">{s}</span>' 
                                                      for s in message['sources']])
            
            st.markdown(f'<div class="chat-message bot-message">🤖 <b>Chatbot:</b> {message["content"]}{sources_html}</div>', 
                       unsafe_allow_html=True)
    
    # Soru girişi
    if st.session_state.initialized:
        with st.form(key='question_form', clear_on_submit=True):
            user_input = st.text_input("Sorunuzu yazın:", placeholder="Örn: Kira artış oranı nasıl belirlenir?")
            submit_button = st.form_submit_button("📤 Gönder")
            
            if submit_button and user_input:
                # Kullanıcı mesajını ekle
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': user_input
                })
                
                # Cevap al
                with st.spinner("💭 Cevap oluşturuluyor..."):
                    try:
                        result = st.session_state.chatbot.ask(user_input)
                        
                        # Bot cevabını ekle
                        st.session_state.chat_history.append({
                            'role': 'bot',
                            'content': result['answer'],
                            'sources': result.get('sources', [])
                        })
                        
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Hata: {e}")

with col2:
    st.header("📋 Örnek Sorular")
    
    example_questions = [
        "Kira artış oranı nasıl belirlenir?",
        "Kiracı hangi durumlarda tahliye edilebilir?",
        "Saklı pay nedir?",
        "Tenkis davası ne zaman açılır?",
        "Depozito en fazla kaç aylık kira olabilir?",
        "Eşin miras payı ne kadardır?",
        "10 yıllık kira süresinin sonunda ne olur?",
        "Vasiyetname türleri nelerdir?"
    ]
    
    for question in example_questions:
        if st.button(question, key=question):
            st.session_state.chat_history.append({
                'role': 'user',
                'content': question
            })
            
            with st.spinner("💭 Cevap oluşturuluyor..."):
                try:
                    result = st.session_state.chatbot.ask(question)
                    
                    st.session_state.chat_history.append({
                        'role': 'bot',
                        'content': result['answer'],
                        'sources': result.get('sources', [])
                    })
                    
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Hata: {e}")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>⚖️ Hukuk RAG Chatbot | Yapay Zeka Destekli Hukuki Danışman</p>
    <p style='font-size: 0.85rem;'>Bu sistem eğitim amaçlıdır. Profesyonel hukuki danışmanlık yerine geçmez.</p>
</div>
""", unsafe_allow_html=True)
