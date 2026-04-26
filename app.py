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

# Profesyonel CSS - Responsive ve modern
st.markdown("""
<style>
    /* Ana tema - Gradient arka plan */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Başlık kartı */
    .header-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .header-card h1 {
        font-size: 3rem;
        margin: 0;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
    }
    
    .header-card p {
        font-size: 1.2rem;
        margin: 1rem 0 0 0;
        color: #6c757d;
        font-weight: 500;
    }
    
    /* Chat container - Beyaz kart */
    .chat-container {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.15);
        min-height: 200px;
        max-height: 400px;
        overflow-y: auto;
        margin-bottom: 1.5rem;
    }
    
    /* Hoş geldin mesajı */
    .welcome-message {
        text-align: center;
        padding: 3rem 2rem;
        color: #6c757d;
    }
    
    .welcome-message h3 {
        color: #667eea;
        font-size: 2rem;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    
    .welcome-message p {
        font-size: 1.1rem;
        line-height: 1.8;
    }
    
    /* Mesajlar - Daha modern */
    .chat-message {
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        animation: slideIn 0.3s ease-out;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 10%;
        border-bottom-right-radius: 5px;
    }
    
    .bot-message {
        background: #f8f9fa;
        border: 2px solid #e9ecef;
        margin-right: 10%;
        border-bottom-left-radius: 5px;
    }
    
    .message-label {
        font-weight: 700;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .message-content {
        line-height: 1.8;
        font-size: 1.05rem;
    }
    
    /* Kaynaklar */
    .sources-container {
        margin-top: 1.5rem;
        padding-top: 1.5rem;
        border-top: 2px solid rgba(0,0,0,0.1);
    }
    
    .source-tag {
        display: inline-block;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 25px;
        margin: 0.3rem;
        font-size: 0.85rem;
        font-weight: 600;
        box-shadow: 0 3px 10px rgba(245, 87, 108, 0.3);
    }
    
    /* Input container - Daha belirgin */
    .input-container {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.15);
    }
    
    /* Textarea - Daha büyük */
    .stTextArea > div > div > textarea {
        border-radius: 15px;
        border: 3px solid #e9ecef;
        padding: 1.2rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        resize: none;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
    }
    
    .stTextArea > div > div > textarea::placeholder {
        color: #adb5bd;
        font-size: 1rem;
    }
    
    /* Butonlar - Daha büyük ve belirgin */
    .stButton > button {
        border-radius: 30px;
        padding: 1rem 3rem;
        font-weight: 700;
        border: none;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        font-size: 1.1rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.5);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    /* Sidebar kartları */
    .sidebar-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    
    .sidebar-card h3 {
        color: #667eea;
        font-size: 1.3rem;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    
    /* Metrikler */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3);
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 800;
        color: white;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        color: rgba(255,255,255,0.9);
        font-size: 1rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: white;
        margin-top: 3rem;
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
    }
    
    .footer p {
        margin: 0.5rem 0;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* Success/Error messages */
    .stSuccess, .stError, .stInfo {
        border-radius: 12px;
        padding: 1rem 1.5rem;
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
        
        .chat-container {
            padding: 1rem;
            min-height: 300px;
            max-height: 400px;
        }
        
        .input-container {
            padding: 1.5rem;
        }
        
        .user-message {
            margin-left: 0;
        }
        
        .bot-message {
            margin-right: 0;
        }
        
        .chat-message {
            padding: 1rem;
        }
        
        .message-content {
            font-size: 1rem;
        }
        
        .stButton > button {
            padding: 0.8rem 2rem;
            font-size: 1rem;
        }
        
        .welcome-message {
            padding: 2rem 1rem;
        }
        
        .welcome-message h3 {
            font-size: 1.5rem;
        }
        
        .welcome-message p {
            font-size: 1rem;
        }
        
        .metric-value {
            font-size: 2rem;
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
                    sources_html = ""
                    if message.get('sources'):
                        sources_html = '<div class="sources-container">📚 Kaynaklar: ' + \
                                      ''.join([f'<span class="source-tag">{s}</span>' for s in message['sources']]) + \
                                      '</div>'
                    
                    st.markdown(f"""
                    <div class="chat-message bot-message">
                        <div class="message-label">⚖️ HUKUK DANIŞMANI</div>
                        <div class="message-content">{message["content"]}</div>
                        {sources_html}
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
