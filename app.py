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

# Ultra Profesyonel CSS - Animasyonlar ve efektler
st.markdown("""
<style>
    /* Ana tema - Animated gradient arka plan */
    .main {
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        padding: 0;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Başlık kartı - Floating animation */
    .header-card {
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(20px);
        padding: 2.5rem;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 25px 70px rgba(0,0,0,0.3);
        border: 2px solid rgba(255,255,255,0.3);
        animation: floatHeader 3s ease-in-out infinite;
        position: relative;
        overflow: hidden;
    }
    
    .header-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(102, 126, 234, 0.1), transparent);
        animation: shimmer 3s infinite;
    }
    
    @keyframes floatHeader {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .header-card h1 {
        font-size: 3rem;
        margin: 0;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
        position: relative;
        z-index: 1;
    }
    
    .header-card p {
        font-size: 1.2rem;
        margin: 1rem 0 0 0;
        color: #6c757d;
        font-weight: 600;
        position: relative;
        z-index: 1;
    }
    
    /* Mesajlar - Gelişmiş animasyonlar */
    .chat-message {
        padding: 1.8rem;
        border-radius: 20px;
        margin-bottom: 1.5rem;
        animation: messageSlideIn 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .chat-message:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    
    @keyframes messageSlideIn {
        0% {
            opacity: 0;
            transform: translateX(-50px) scale(0.9);
        }
        100% {
            opacity: 1;
            transform: translateX(0) scale(1);
        }
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 10%;
        border-bottom-right-radius: 8px;
        animation: messageSlideInRight 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }
    
    @keyframes messageSlideInRight {
        0% {
            opacity: 0;
            transform: translateX(50px) scale(0.9);
        }
        100% {
            opacity: 1;
            transform: translateX(0) scale(1);
        }
    }
    
    .bot-message {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border: 2px solid #e9ecef;
        margin-right: 10%;
        border-bottom-left-radius: 8px;
    }
    
    .bot-message::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        animation: pulseBar 2s ease-in-out infinite;
    }
    
    @keyframes pulseBar {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .message-label {
        font-weight: 800;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .message-content {
        line-height: 1.9;
        font-size: 1.1rem;
        font-weight: 500;
    }
    
    /* Input container - Glow effect */
    .input-container {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 25px;
        padding: 2rem;
        box-shadow: 0 15px 50px rgba(0,0,0,0.2);
        border: 2px solid rgba(255,255,255,0.3);
        position: relative;
        animation: glowPulse 3s ease-in-out infinite;
    }
    
    @keyframes glowPulse {
        0%, 100% {
            box-shadow: 0 15px 50px rgba(102, 126, 234, 0.2);
        }
        50% {
            box-shadow: 0 15px 60px rgba(102, 126, 234, 0.4);
        }
    }
    
    /* Textarea - Focus animation */
    .stTextArea > div > div > textarea {
        border-radius: 18px;
        border: 3px solid #e9ecef;
        padding: 1.5rem;
        font-size: 1.1rem;
        transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        resize: none;
        font-weight: 500;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 6px rgba(102, 126, 234, 0.15);
        transform: scale(1.02);
    }
    
    .stTextArea > div > div > textarea::placeholder {
        color: #adb5bd;
        font-size: 1rem;
    }
    
    /* Butonlar - 3D effect */
    .stButton > button {
        border-radius: 35px;
        padding: 1.2rem 3.5rem;
        font-weight: 800;
        border: none;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        font-size: 1.15rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255,255,255,0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
    }
    
    .stButton > button:active {
        transform: translateY(-2px) scale(1.02);
    }
    
    /* Sidebar kartları - Hover effects */
    .sidebar-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
        border: 2px solid rgba(255,255,255,0.3);
    }
    
    .sidebar-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
    }
    
    .sidebar-card h3 {
        color: #667eea;
        font-size: 1.4rem;
        margin-bottom: 1rem;
        font-weight: 800;
    }
    
    /* Footer - Fade in */
    .footer {
        text-align: center;
        padding: 2.5rem;
        color: white;
        margin-top: 3rem;
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        animation: fadeInUp 1s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .footer p {
        margin: 0.5rem 0;
        font-weight: 600;
    }
    
    /* Scrollbar - Gradient */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #764ba2 0%, #f093fb 100%);
    }
    
    /* Loading spinner - Custom */
    .stSpinner > div {
        border-top-color: #667eea !important;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Success/Error messages - Slide in */
    .stSuccess, .stError, .stInfo {
        border-radius: 15px;
        padding: 1.2rem 1.8rem;
        animation: slideInLeft 0.5s ease-out;
        font-weight: 600;
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* RESPONSIVE - Mobil uyumluluk */
    @media (max-width: 768px) {
        .header-card h1 {
            font-size: 2rem;
        }
        
        .header-card p {
            font-size: 1rem;
        }
        
        .header-card {
            padding: 1.5rem;
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
        
        .message-content {
            font-size: 1rem;
        }
        
        .stButton > button {
            padding: 1rem 2rem;
            font-size: 1rem;
        }
        
        .sidebar-card {
            padding: 1rem;
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
    <p>Yapay Zeka Destekli Profesyonel Hukuki Danışmanlık Sistemi</p>
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
    <p style='font-size: 0.9rem; margin-top: 0.5rem;'>
        Bu sistem yapay zeka destekli bir bilgilendirme aracıdır.<br>
        Profesyonel hukuki danışmanlık yerine geçmez.
    </p>
</div>
""", unsafe_allow_html=True)
