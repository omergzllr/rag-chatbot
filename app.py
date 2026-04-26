import streamlit as st
import json
import os
from datetime import datetime

# Performans için session state cache
@st.cache_resource
def load_chatbot():
    """Chatbot'u cache'le - sadece bir kez yükle"""
    if os.getenv("GROQ_API_KEY"):
        from llm_handler_cloud import LLMHandler
        from rag_chatbot import RAGChatbot
        USE_CLOUD = True
    else:
        from rag_chatbot import RAGChatbot
        USE_CLOUD = False
    
    chatbot = RAGChatbot()
    chatbot.initialize()
    return chatbot, USE_CLOUD

# Sayfa yapılandırması
st.set_page_config(
    page_title="Hukuk Destek Danışmanı",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ultra Profesyonel Hukuk Asistanı Tasarımı - Koyu Tema
st.markdown("""
<style>
    /* Ana tema - Koyu profesyonel arka plan */
    .main {
        background: #0a0e27;
        padding: 0;
    }
    
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }
    
    /* Başlık - Minimal ve profesyonel */
    .header-card {
        background: linear-gradient(135deg, #1a1f3a 0%, #2d3561 100%);
        padding: 3rem 2rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 3rem;
        border: 1px solid rgba(255,255,255,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .header-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #4f46e5, transparent);
    }
    
    .header-card h1 {
        font-size: 2.5rem;
        margin: 0 0 0.5rem 0;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.5px;
    }
    
    .header-card p {
        font-size: 1rem;
        margin: 0;
        color: #94a3b8;
        font-weight: 400;
        line-height: 1.6;
    }
    
    .header-subtitle {
        font-size: 0.9rem;
        color: #64748b;
        margin-top: 1rem;
        font-style: italic;
    }
    
    /* Mesajlar - Minimal ve temiz */
    .chat-message {
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        animation: fadeIn 0.4s ease-out;
        border: 1px solid rgba(255,255,255,0.05);
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .user-message {
        background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
        color: white;
        margin-left: 15%;
        border: none;
    }
    
    .bot-message {
        background: #1e293b;
        color: #e2e8f0;
        margin-right: 15%;
        border-left: 3px solid #4f46e5;
    }
    
    .message-label {
        font-weight: 600;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        opacity: 0.8;
    }
    
    .message-content {
        line-height: 1.7;
        font-size: 1rem;
        font-weight: 400;
    }
    
    /* Input container - Profesyonel */
    .input-container {
        background: #1e293b;
        border-radius: 16px;
        padding: 2rem;
        border: 1px solid rgba(255,255,255,0.1);
        margin-top: 2rem;
    }
    
    /* Textarea - Koyu tema */
    .stTextArea > div > div > textarea {
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.1);
        background: #0f172a;
        color: #e2e8f0;
        padding: 1.2rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        resize: none;
        font-weight: 400;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #4f46e5;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
        background: #1e293b;
    }
    
    .stTextArea > div > div > textarea::placeholder {
        color: #64748b;
        font-size: 0.95rem;
    }
    
    /* Butonlar - Minimal ve profesyonel */
    .stButton > button {
        border-radius: 10px;
        padding: 0.9rem 2.5rem;
        font-weight: 600;
        border: none;
        background: #4f46e5;
        color: white;
        transition: all 0.3s ease;
        font-size: 1rem;
        letter-spacing: 0.3px;
    }
    
    .stButton > button:hover {
        background: #6366f1;
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(79, 70, 229, 0.3);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Sidebar - Koyu tema */
    .sidebar-card {
        background: #1e293b;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .sidebar-card h3 {
        color: #ffffff;
        font-size: 1.1rem;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    /* Örnek soru butonları */
    div[data-testid="column"] .stButton > button {
        background: #1e293b;
        color: #e2e8f0;
        border: 1px solid rgba(255,255,255,0.1);
        text-align: left;
        padding: 0.9rem 1.2rem;
        font-size: 0.9rem;
        font-weight: 500;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    div[data-testid="column"] .stButton > button:hover {
        background: #2d3561;
        border-color: #4f46e5;
        transform: translateX(5px);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #64748b;
        margin-top: 3rem;
        border-top: 1px solid rgba(255,255,255,0.1);
    }
    
    .footer p {
        margin: 0.3rem 0;
        font-size: 0.9rem;
    }
    
    .footer strong {
        color: #94a3b8;
    }
    
    /* Scrollbar - Koyu tema */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0f172a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #4f46e5;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #6366f1;
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-top-color: #4f46e5 !important;
    }
    
    /* Success/Error messages - Koyu tema */
    .stSuccess {
        background: #1e293b;
        color: #10b981;
        border: 1px solid #10b981;
        border-radius: 10px;
        padding: 1rem;
    }
    
    .stError {
        background: #1e293b;
        color: #ef4444;
        border: 1px solid #ef4444;
        border-radius: 10px;
        padding: 1rem;
    }
    
    .stInfo {
        background: #1e293b;
        color: #3b82f6;
        border: 1px solid #3b82f6;
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* RESPONSIVE */
    @media (max-width: 768px) {
        .header-card h1 {
            font-size: 1.8rem;
        }
        
        .header-card p {
            font-size: 0.9rem;
        }
        
        .header-card {
            padding: 2rem 1.5rem;
        }
        
        .input-container {
            padding: 1.5rem;
        }
        
        .user-message, .bot-message {
            margin-left: 0;
            margin-right: 0;
        }
        
        .chat-message {
            padding: 1.2rem;
        }
        
        .stButton > button {
            padding: 0.8rem 2rem;
            font-size: 0.95rem;
        }
        
        .sidebar-card {
            padding: 1.2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Session state başlatma
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Başlık
st.markdown("""
<div class="header-card">
    <h1>⚖️ Hukuk Destek Danışmanı</h1>
    <p>Hukukçular için özel olarak tasarlanmış yapay zeka destekli asistan</p>
    <p class="header-subtitle">İstenildiği şekilde eğitilebilir, özelleştirilebilir ve büyütülebilir AI teknolojisi</p>
</div>
""", unsafe_allow_html=True)

# Ana layout - Responsive
col1, col2 = st.columns([2.5, 1], gap="large")

with col1:
    # Chatbot'u yükle (cache'den)
    try:
        chatbot, USE_CLOUD = load_chatbot()
        
        # Chat geçmişini göster (container olmadan)
        if st.session_state.chat_history:
            for message in st.session_state.chat_history:
                if message['role'] == 'user':
                    st.markdown(f"""
                    <div class="chat-message user-message">
                        <div class="message-label">👤 SİZ</div>
                        <div class="message-content">{message["content"]}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message bot-message">
                        <div class="message-label">⚖️ HUKUK DANIŞMANI</div>
                        <div class="message-content">{message["content"]}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Soru girişi
        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        with st.form(key='question_form', clear_on_submit=True):
            user_input = st.text_area(
                "Sorunuz",
                placeholder="Hukuki sorunuzu buraya yazın...\n\nÖrnek: Kira artış oranı nasıl belirlenir?",
                height=120,
                label_visibility="collapsed"
            )
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                submit_button = st.form_submit_button("📤 Soru Sor", use_container_width=True)
            
            if submit_button and user_input:
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': user_input
                })
                
                with st.spinner("💭 Yanıt hazırlanıyor..."):
                    try:
                        result = chatbot.ask(user_input)
                        
                        st.session_state.chat_history.append({
                            'role': 'bot',
                            'content': result['answer'],
                            'sources': result.get('sources', [])
                        })
                        
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Hata: {str(e)}", icon="❌")
        st.markdown('</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"❌ Sistem başlatılamadı: {str(e)}", icon="❌")

with col2:
    # Örnek sorular
    st.markdown('<div class="sidebar-card"><h3>💡 Örnek Sorular</h3></div>', unsafe_allow_html=True)
    
    example_questions = [
        "Kira artış oranı nasıl belirlenir?",
        "Kiracı hangi durumlarda tahliye edilebilir?",
        "Saklı pay nedir?",
        "Tenkis davası ne zaman açılır?",
        "Depozito en fazla kaç aylık kira olabilir?",
        "Eşin miras payı ne kadardır?",
        "10 yıllık kira süresinin sonunda ne olur?",
        "Vasiyetname türleri nelerdir?",
        "Yıllık izin hakkı nasıl hesaplanır?",
        "Kıdem tazminatı ne zaman ödenir?"
    ]
    
    for question in example_questions:
        if st.button(question, key=question, use_container_width=True):
            st.session_state.chat_history.append({
                'role': 'user',
                'content': question
            })
            
            with st.spinner("💭 Yanıt hazırlanıyor..."):
                try:
                    chatbot, _ = load_chatbot()
                    result = chatbot.ask(question)
                    
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
    <p>Hukukçular için özel olarak tasarlanmış yapay zeka destekli asistan</p>
    <p style='font-size: 0.85rem; margin-top: 1rem; opacity: 0.7;'>
        İstenildiği şekilde eğitilebilir • Özelleştirilebilir • Büyütülebilir AI teknolojisi
    </p>
</div>
""", unsafe_allow_html=True)
