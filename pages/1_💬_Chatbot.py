import streamlit as st
import os

st.set_page_config(
    page_title="Chatbot - Hukuk Danışmanı",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Performans için cache
@st.cache_resource
def load_chatbot():
    from rag_chatbot import RAGChatbot
    chatbot = RAGChatbot()
    chatbot.initialize()
    return chatbot

# CSS
st.markdown("""
<style>
    .main { background: #0a0e27; }
    .block-container { padding-top: 2rem; max-width: 1200px; }
    
    .page-header {
        background: linear-gradient(135deg, #1a1f3a 0%, #2d3561 100%);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        border: 1px solid rgba(79, 70, 229, 0.3);
        text-align: center;
    }
    
    .page-header h1 {
        color: #ffffff;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    
    .page-header p {
        color: #94a3b8;
        margin: 0.5rem 0 0 0;
        font-size: 1rem;
    }
    
    .chat-message {
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        animation: fadeIn 0.4s ease-out;
        border: 1px solid rgba(255,255,255,0.05);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
        color: white;
        margin-left: 15%;
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
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        opacity: 0.7;
    }
    
    .message-content {
        line-height: 1.7;
        font-size: 1rem;
    }
    
    .input-container {
        background: #1e293b;
        border-radius: 16px;
        padding: 2rem;
        border: 1px solid rgba(255,255,255,0.1);
        margin-top: 1.5rem;
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.1);
        background: #0f172a;
        color: #e2e8f0;
        padding: 1.2rem;
        font-size: 1rem;
        resize: none;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #4f46e5;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
    }
    
    .stTextArea > div > div > textarea::placeholder {
        color: #64748b;
    }
    
    .stButton > button {
        border-radius: 10px;
        padding: 0.9rem 2.5rem;
        font-weight: 600;
        border: none;
        background: #4f46e5;
        color: white;
        transition: all 0.3s ease;
        font-size: 1rem;
    }
    
    .stButton > button:hover {
        background: #6366f1;
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(79, 70, 229, 0.3);
    }
    
    .sidebar-card {
        background: #1e293b;
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .sidebar-card h3 {
        color: #ffffff;
        font-size: 1rem;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #0f172a; }
    ::-webkit-scrollbar-thumb { background: #4f46e5; border-radius: 5px; }
    
    @media (max-width: 768px) {
        .user-message, .bot-message { margin-left: 0; margin-right: 0; }
        .chat-message { padding: 1.2rem; }
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="page-header">
    <h1>💬 Hukuk Asistanı</h1>
    <p>Hukuki sorularınızı sorun, anında yanıt alın</p>
</div>
""", unsafe_allow_html=True)

# Session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

col1, col2 = st.columns([2.5, 1], gap="large")

with col1:
    try:
        chatbot = load_chatbot()

        # Mesajları göster
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f"""
                <div class="chat-message user-message">
                    <div class="message-label">👤 Siz</div>
                    <div class="message-content">{message["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message bot-message">
                    <div class="message-label">⚖️ Hukuk Danışmanı</div>
                    <div class="message-content">{message["content"]}</div>
                </div>
                """, unsafe_allow_html=True)

        # Input
        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        with st.form(key='question_form', clear_on_submit=True):
            user_input = st.text_area(
                "Soru",
                placeholder="Hukuki sorunuzu buraya yazın...\nÖrnek: Kira artış oranı nasıl belirlenir?",
                height=120,
                label_visibility="collapsed"
            )
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                submit = st.form_submit_button("📤 Soru Sor", use_container_width=True)

            if submit and user_input:
                st.session_state.chat_history.append({'role': 'user', 'content': user_input})
                with st.spinner("💭 Yanıt hazırlanıyor..."):
                    try:
                        result = chatbot.ask(user_input)
                        st.session_state.chat_history.append({
                            'role': 'bot',
                            'content': result['answer']
                        })
                        st.rerun()
                    except Exception as e:
                        st.error(f"Hata: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Sistem başlatılamadı: {str(e)}")

with col2:
    st.markdown('<div class="sidebar-card"><h3>💡 Örnek Sorular</h3></div>', unsafe_allow_html=True)

    questions = [
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

    for q in questions:
        if st.button(q, key=q, use_container_width=True):
            st.session_state.chat_history.append({'role': 'user', 'content': q})
            with st.spinner("💭 Yanıt hazırlanıyor..."):
                try:
                    chatbot = load_chatbot()
                    result = chatbot.ask(q)
                    st.session_state.chat_history.append({'role': 'bot', 'content': result['answer']})
                    st.rerun()
                except Exception as e:
                    st.error(f"Hata: {str(e)}")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ Sohbeti Temizle", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()
