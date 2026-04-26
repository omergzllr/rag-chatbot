import streamlit as st

# Sayfa yapılandırması
st.set_page_config(
    page_title="Hukuk Destek Danışmanı",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Profesyonel Landing Page CSS
st.markdown("""
<style>
    .main {
        background: #0a0e27;
        padding: 0;
    }
    
    .block-container {
        padding-top: 0;
        max-width: 100%;
    }
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #1a1f3a 0%, #2d3561 100%);
        padding: 6rem 2rem;
        text-align: center;
        border-bottom: 2px solid rgba(79, 70, 229, 0.3);
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 1rem;
        letter-spacing: -2px;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        color: #94a3b8;
        margin-bottom: 3rem;
        font-weight: 400;
    }
    
    .cta-button {
        display: inline-block;
        background: #4f46e5;
        color: white;
        padding: 1.2rem 3rem;
        border-radius: 12px;
        text-decoration: none;
        font-weight: 600;
        font-size: 1.2rem;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
    }
    
    .cta-button:hover {
        background: #6366f1;
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(79, 70, 229, 0.4);
    }
    
    /* Features Section */
    .features-section {
        padding: 5rem 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .section-title {
        text-align: center;
        font-size: 2.5rem;
        color: #ffffff;
        margin-bottom: 3rem;
        font-weight: 700;
    }
    
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin-top: 3rem;
    }
    
    .feature-card {
        background: #1e293b;
        padding: 2.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        border-color: #4f46e5;
        box-shadow: 0 20px 40px rgba(79, 70, 229, 0.2);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1.5rem;
    }
    
    .feature-title {
        font-size: 1.5rem;
        color: #ffffff;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .feature-description {
        color: #94a3b8;
        line-height: 1.7;
        font-size: 1rem;
    }
    
    /* Stats Section */
    .stats-section {
        background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
        padding: 4rem 2rem;
        text-align: center;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 3rem;
        max-width: 1000px;
        margin: 0 auto;
    }
    
    .stat-item {
        color: white;
    }
    
    .stat-number {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Footer */
    .footer {
        background: #1e293b;
        padding: 3rem 2rem;
        text-align: center;
        color: #94a3b8;
        border-top: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        
        .hero-subtitle {
            font-size: 1.2rem;
        }
        
        .features-grid {
            grid-template-columns: 1fr;
        }
        
        .stat-number {
            font-size: 2.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">⚖️ Hukuk Destek Danışmanı</h1>
    <p class="hero-subtitle">Hukukçular için özel olarak tasarlanmış yapay zeka destekli asistan</p>
    <p style="color: #64748b; font-size: 1.1rem; margin-bottom: 2rem;">
        İstenildiği şekilde eğitilebilir • Özelleştirilebilir • Büyütülebilir AI teknolojisi
    </p>
</div>
""", unsafe_allow_html=True)

# CTA Button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🚀 Hemen Başla", use_container_width=True, type="primary"):
        st.switch_page("pages/1_💬_Chatbot.py")

# Features Section
st.markdown("""
<div class="features-section">
    <h2 class="section-title">Neden Hukuk Destek Danışmanı?</h2>
    <div class="features-grid">
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <h3 class="feature-title">Yapay Zeka Destekli</h3>
            <p class="feature-description">
                En gelişmiş AI teknolojisi ile hukuki sorularınıza anında yanıt alın. 
                Sürekli öğrenen ve gelişen sistem.
            </p>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">📚</div>
            <h3 class="feature-title">Geniş Hukuk Bilgisi</h3>
            <p class="feature-description">
                20+ hukuk alanında uzmanlaşmış bilgi tabanı. Kira, miras, iş, aile hukuku ve daha fazlası.
            </p>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <h3 class="feature-title">Hızlı ve Güvenilir</h3>
            <p class="feature-description">
                Saniyeler içinde doğru ve güvenilir yanıtlar. 7/24 kesintisiz hizmet.
            </p>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <h3 class="feature-title">Özelleştirilebilir</h3>
            <p class="feature-description">
                Kendi belgelerinizle eğitin. Firmanıza özel hukuki bilgi tabanı oluşturun.
            </p>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">🔒</div>
            <h3 class="feature-title">Güvenli ve Gizli</h3>
            <p class="feature-description">
                Tüm verileriniz şifreli ve güvende. Gizlilik politikalarına tam uyum.
            </p>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <h3 class="feature-title">Sürekli Gelişim</h3>
            <p class="feature-description">
                Kullanım verilerine göre sürekli öğrenen ve gelişen yapay zeka modeli.
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Stats Section
st.markdown("""
<div class="stats-section">
    <div class="stats-grid">
        <div class="stat-item">
            <div class="stat-number">20+</div>
            <div class="stat-label">Hukuk Alanı</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">80+</div>
            <div class="stat-label">Soru-Cevap</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">7/24</div>
            <div class="stat-label">Kesintisiz Hizmet</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">%100</div>
            <div class="stat-label">Ücretsiz</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p style="font-size: 1.2rem; font-weight: 600; color: #ffffff; margin-bottom: 1rem;">
        ⚖️ Hukuk Destek Danışmanı
    </p>
    <p>Hukukçular için özel olarak tasarlanmış yapay zeka destekli asistan</p>
    <p style="margin-top: 1.5rem; font-size: 0.9rem; opacity: 0.7;">
        © 2026 Hukuk Destek Danışmanı. Tüm hakları saklıdır.
    </p>
</div>
""", unsafe_allow_html=True)
