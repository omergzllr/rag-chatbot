import streamlit as st
import json
import os
from datetime import datetime

# Cloud deployment için LLM handler seçimi
if os.getenv("GROQ_API_KEY"):
    from llm_handler_cloud import LLMHandler
    from rag_chatbot import RAGChatbot
    USE_CLOUD = True
else:
    from rag_chatbot import RAGChatbot
    USE_CLOUD = False

# Sayfa yapılandırması
st.set_page_config(
    page_title="Hukuk Destek Danışmanı",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Profesyonel CSS
st.markdown("""
<style>
    /* Ana tema */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Başlık */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        margin: 0;
        font-weight: 700;
    }
    
    .main-header p {
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Chat container */
    .chat-container {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        min-height: 500px;
        max-height: 600px;
        overflow-y: auto;
    }
    
    /* Mesajlar */
    .chat-message {
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        animation: fadeIn 0.3s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 20%;
        box-shadow: 0 3px 10px rgba(102, 126, 234, 0.3);
    }
    
    .bot-message {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        margin-right: 20%;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
    }
    
    .message-label {
        font-weight: 600;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .message-content {
        line-height: 1.6;
    }
    
    /* Kaynaklar */
    .sources-container {
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid #dee2e6;
    }
    
    .source-tag {
        display: inline-block;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin: 0.3rem;
        font-size: 0.85rem;
        font-weight: 500;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    /* Input alanı */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #e9ecef;
        padding: 0.8rem 1.5rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Butonlar */
    .stButton > button {
        border-radius: 25px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        border: none;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: white;
    }
    
    /* Metrikler */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label {
        color: #6c757d;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Örnek sorular */
    .example-question {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.8rem;
        border: 2px solid #e9ecef;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .example-question:hover {
        border-color: #667eea;
        transform: translateX(5px);
        box-shadow: 0 3px 10px rgba(102, 126, 234, 0.2);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #6c757d;
        margin-top: 3rem;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Session state başlatma
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = None
    st.session_state.initialized = False
    st.session_state.chat_history = []

# Başlık
st.markdown("""
<div class="main-header">
    <h1>⚖️ Hukuk Destek Danışmanı</h1>
    <p>Yapay Zeka Destekli Profesyonel Hukuki Danışmanlık Sistemi</p>
</div>
""", unsafe_allow_html=True)

# Ana layout
col1, col2 = st.columns([2, 1])

with col1:
    # Chatbot'u başlat
    if not st.session_state.initialized:
        with st.spinner("🔄 Sistem başlatılıyor..."):
            try:
                st.session_state.chatbot = RAGChatbot()
                success = st.session_state.chatbot.initialize()
                if success:
                    st.session_state.initialized = True
                    st.success("✅ Sistem hazır! Sorularınızı sorabilirsiniz.", icon="✅")
                else:
                    st.error("❌ Sistem başlatılamadı. Lütfen yönetici ile iletişime geçin.", icon="❌")
            except Exception as e:
                st.error(f"❌ Hata: {str(e)}", icon="❌")
    
    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    if not st.session_state.chat_history:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; color: #6c757d;">
            <h3>👋 Hoş Geldiniz!</h3>
            <p>Hukuki sorularınızı sormak için aşağıdaki alana yazabilir veya sağdaki örnek sorulardan birini seçebilirsiniz.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Chat geçmişini göster
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            st.markdown(f"""
            <div class="chat-message user-message">
                <div class="message-label">👤 Siz</div>
                <div class="message-content">{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            sources_html = ""
            if message.get('sources'):
                sources_html = '<div class="sources-container">📚 Kaynaklar: ' + \
                              ''.join([f'<span class="source-tag">{s}</span>' for s in message['sources']]) + \
                              '</div>'
            
            st.markdown(f"""
            <div class="chat-message bot-message">
                <div class="message-label">⚖️ Hukuk Danışmanı</div>
                <div class="message-content">{message["content"]}</div>
                {sources_html}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Soru girişi
    if st.session_state.initialized:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.form(key='question_form', clear_on_submit=True):
            col_input, col_button = st.columns([4, 1])
            with col_input:
                user_input = st.text_input(
                    "Sorunuz",
                    placeholder="Hukuki sorunuzu buraya yazın...",
                    label_visibility="collapsed"
                )
            with col_button:
                submit_button = st.form_submit_button("📤 Gönder", use_container_width=True)
            
            if submit_button and user_input:
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': user_input
                })
                
                with st.spinner("💭 Yanıt hazırlanıyor..."):
                    try:
                        result = st.session_state.chatbot.ask(user_input)
                        
                        st.session_state.chat_history.append({
                            'role': 'bot',
                            'content': result['answer'],
                            'sources': result.get('sources', [])
                        })
                        
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Hata: {str(e)}", icon="❌")

with col2:
    # İstatistikler
    st.markdown("### 📊 İstatistikler")
    
    if os.path.exists("questions_log.json"):
        with open("questions_log.json", 'r', encoding='utf-8') as f:
            questions_log = json.load(f)
        
        total_questions = len(questions_log)
        needs_research = sum(1 for q in questions_log if q.get('needs_research', False))
        found_in_docs = total_questions - needs_research
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_questions}</div>
            <div class="metric-label">Toplam Soru</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{found_in_docs}</div>
            <div class="metric-label">Yanıtlanan</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Henüz soru sorulmadı", icon="ℹ️")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Örnek sorular
    st.markdown("### 💡 Örnek Sorular")
    
    example_questions = [
        "Kira artış oranı nasıl belirlenir?",
        "Kiracı hangi durumlarda tahliye edilebilir?",
        "Saklı pay nedir?",
        "Tenkis davası ne zaman açılır?",
        "Depozito en fazla kaç aylık kira olabilir?",
        "Eşin miras payı ne kadardır?"
    ]
    
    for question in example_questions:
        if st.button(question, key=question, use_container_width=True):
            st.session_state.chat_history.append({
                'role': 'user',
                'content': question
            })
            
            with st.spinner("💭 Yanıt hazırlanıyor..."):
                try:
                    result = st.session_state.chatbot.ask(question)
                    
                    st.session_state.chat_history.append({
                        'role': 'bot',
                        'content': result['answer'],
                        'sources': result.get('sources', [])
                    })
                    
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Hata: {str(e)}", icon="❌")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Sohbeti temizle butonu
    if st.button("🗑️ Sohbeti Temizle", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# Footer
st.markdown("""
<div class="footer">
    <p><strong>⚖️ Hukuk Destek Danışmanı</strong></p>
    <p style='font-size: 0.9rem; margin-top: 0.5rem;'>
        Bu sistem yapay zeka destekli bir bilgilendirme aracıdır.<br>
        Profesyonel hukuki danışmanlık yerine geçmez.
    </p>
</div>
""", unsafe_allow_html=True)
