import streamlit as st

st.set_page_config(
    page_title="İletişim - Hukuk Danışmanı",
    page_icon="📞",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .main { background: #0a0e27; }
    .block-container { padding-top: 2rem; max-width: 900px; }
    
    .page-header {
        background: linear-gradient(135deg, #1a1f3a 0%, #2d3561 100%);
        padding: 2.5rem;
        border-radius: 16px;
        margin-bottom: 3rem;
        border: 1px solid rgba(79, 70, 229, 0.3);
        text-align: center;
    }
    
    .page-header h1 { color: #ffffff; font-size: 2.2rem; font-weight: 700; margin: 0; }
    .page-header p { color: #94a3b8; margin: 0.5rem 0 0 0; }
    
    .contact-card {
        background: #1e293b;
        padding: 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.3s ease;
    }
    
    .contact-card:hover {
        border-color: #4f46e5;
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(79, 70, 229, 0.2);
    }
    
    .contact-card h2 {
        color: #4f46e5;
        font-size: 1.4rem;
        margin-bottom: 1.5rem;
        font-weight: 700;
    }
    
    .contact-card p {
        color: #94a3b8;
        line-height: 1.8;
        font-size: 1.05rem;
    }
    
    .contact-info {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1rem;
        background: rgba(79, 70, 229, 0.1);
        border-radius: 10px;
        margin-bottom: 1rem;
        border: 1px solid rgba(79, 70, 229, 0.2);
    }
    
    .contact-icon { font-size: 1.5rem; }
    
    .contact-text { color: #e2e8f0; font-size: 1rem; }
    .contact-label { color: #64748b; font-size: 0.85rem; }
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: #0f172a;
        color: #e2e8f0;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 0.8rem 1rem;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #4f46e5;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
    }
    
    .stTextInput label, .stTextArea label {
        color: #94a3b8 !important;
        font-weight: 500;
    }
    
    .stButton > button {
        background: #4f46e5;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.9rem 2.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: #6366f1;
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(79, 70, 229, 0.3);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <h1>📞 İletişim</h1>
    <p>Bizimle iletişime geçin, size yardımcı olalım</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("""
    <div class="contact-card">
        <h2>📬 İletişim Bilgileri</h2>
        
        <div class="contact-info">
            <div class="contact-icon">📧</div>
            <div>
                <div class="contact-label">E-posta</div>
                <div class="contact-text">info@hukukdestek.ai</div>
            </div>
        </div>
        
        <div class="contact-info">
            <div class="contact-icon">🌐</div>
            <div>
                <div class="contact-label">Web Sitesi</div>
                <div class="contact-text">www.hukukdestek.ai</div>
            </div>
        </div>
        
        <div class="contact-info">
            <div class="contact-icon">📍</div>
            <div>
                <div class="contact-label">Konum</div>
                <div class="contact-text">İstanbul, Türkiye</div>
            </div>
        </div>
        
        <div class="contact-info">
            <div class="contact-icon">⏰</div>
            <div>
                <div class="contact-label">Çalışma Saatleri</div>
                <div class="contact-text">7/24 AI Desteği</div>
            </div>
        </div>
    </div>
    
    <div class="contact-card">
        <h2>🚀 Özel Çözümler</h2>
        <p>
            Hukuk firmanız veya kurumunuz için özelleştirilmiş AI çözümleri sunuyoruz:
        </p>
        <p>• Kendi belgelerinizle eğitilmiş özel model</p>
        <p>• Firma markanıza uygun tasarım</p>
        <p>• API entegrasyonu</p>
        <p>• Teknik destek ve bakım</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="contact-card">
        <h2>✉️ Mesaj Gönderin</h2>
    </div>
    """, unsafe_allow_html=True)

    with st.form("contact_form"):
        name = st.text_input("Ad Soyad", placeholder="Adınız ve soyadınız")
        email = st.text_input("E-posta", placeholder="ornek@email.com")
        subject = st.selectbox("Konu", [
            "Genel Bilgi",
            "Özel Çözüm Talebi",
            "Teknik Destek",
            "İş Birliği",
            "Diğer"
        ])
        message = st.text_area("Mesajınız", placeholder="Mesajınızı buraya yazın...", height=150)

        submitted = st.form_submit_button("📤 Gönder", use_container_width=True)

        if submitted:
            if name and email and message:
                st.success("✅ Mesajınız alındı! En kısa sürede size dönüş yapacağız.")
            else:
                st.error("❌ Lütfen tüm alanları doldurun.")
