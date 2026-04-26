import streamlit as st

st.set_page_config(
    page_title="Hakkında - Hukuk Danışmanı",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .main { background: #0a0e27; }
    .block-container { padding-top: 2rem; max-width: 1100px; }
    
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
    
    .content-card {
        background: #1e293b;
        padding: 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .content-card h2 {
        color: #4f46e5;
        font-size: 1.5rem;
        margin-bottom: 1.5rem;
        font-weight: 700;
        border-bottom: 2px solid rgba(79, 70, 229, 0.3);
        padding-bottom: 0.8rem;
    }
    
    .content-card p, .content-card li {
        color: #94a3b8;
        line-height: 1.8;
        font-size: 1.05rem;
    }
    
    .content-card ul { padding-left: 1.5rem; }
    .content-card li { margin-bottom: 0.5rem; }
    
    .highlight {
        color: #6366f1;
        font-weight: 600;
    }
    
    .tech-badge {
        display: inline-block;
        background: rgba(79, 70, 229, 0.2);
        color: #6366f1;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        margin: 0.3rem;
        font-size: 0.9rem;
        font-weight: 600;
        border: 1px solid rgba(79, 70, 229, 0.3);
    }
    
    .area-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .area-item {
        background: rgba(79, 70, 229, 0.1);
        padding: 1rem;
        border-radius: 10px;
        color: #e2e8f0;
        text-align: center;
        border: 1px solid rgba(79, 70, 229, 0.2);
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <h1>📖 Sistem Hakkında</h1>
    <p>Hukuk Destek Danışmanı nasıl çalışır?</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="content-card">
    <h2>🤖 Sistem Nedir?</h2>
    <p>
        <span class="highlight">Hukuk Destek Danışmanı</span>, hukukçular ve hukuki danışmanlık ihtiyacı duyan 
        bireyler için özel olarak geliştirilmiş yapay zeka destekli bir asistan sistemidir.
    </p>
    <p>
        Sistem, <span class="highlight">RAG (Retrieval-Augmented Generation)</span> mimarisi üzerine inşa edilmiştir. 
        Bu mimari sayesinde yapay zeka, yalnızca genel bilgisine değil, sisteme yüklenen hukuki belgelere 
        dayanarak yanıt üretir. Bu da yanıtların çok daha doğru ve güvenilir olmasını sağlar.
    </p>
</div>

<div class="content-card">
    <h2>⚙️ Nasıl Çalışır?</h2>
    <p>Sistem 4 temel adımda çalışır:</p>
    <ul>
        <li><strong style="color:#e2e8f0;">1. Belge Yükleme:</strong> Hukuki PDF belgeler sisteme yüklenir ve işlenir.</li>
        <li><strong style="color:#e2e8f0;">2. Vektör Dönüşümü:</strong> Belgeler yapay zeka tarafından anlamlı vektörlere dönüştürülür.</li>
        <li><strong style="color:#e2e8f0;">3. Akıllı Arama:</strong> Soru sorulduğunda ilgili belgeler bulunur.</li>
        <li><strong style="color:#e2e8f0;">4. Yanıt Üretimi:</strong> Bulunan belgeler bağlamında AI yanıt oluşturur.</li>
    </ul>
</div>

<div class="content-card">
    <h2>📚 Kapsanan Hukuk Alanları</h2>
    <div class="area-grid">
        <div class="area-item">⚖️ Kira Hukuku</div>
        <div class="area-item">🏛️ Miras Hukuku</div>
        <div class="area-item">👨‍👩‍👧 Aile Hukuku</div>
        <div class="area-item">💼 İş Hukuku</div>
        <div class="area-item">🏦 İcra & İflas</div>
        <div class="area-item">🛒 Tüketici Hukuku</div>
        <div class="area-item">📜 Borçlar Hukuku</div>
        <div class="area-item">🏠 Eşya Hukuku</div>
        <div class="area-item">⚖️ Ceza Hukuku</div>
        <div class="area-item">🏢 Ticaret Hukuku</div>
        <div class="area-item">🔒 KVKK</div>
        <div class="area-item">🌿 Çevre Hukuku</div>
    </div>
</div>

<div class="content-card">
    <h2>🛠️ Kullanılan Teknolojiler</h2>
    <p>
        <span class="tech-badge">Python</span>
        <span class="tech-badge">Streamlit</span>
        <span class="tech-badge">LangChain</span>
        <span class="tech-badge">ChromaDB</span>
        <span class="tech-badge">Sentence Transformers</span>
        <span class="tech-badge">Groq API</span>
        <span class="tech-badge">Llama 3.3 70B</span>
        <span class="tech-badge">RAG Mimarisi</span>
    </p>
</div>

<div class="content-card">
    <h2>🎯 Özelleştirme ve Büyütme</h2>
    <p>
        Sistem tamamen <span class="highlight">özelleştirilebilir</span> ve <span class="highlight">büyütülebilir</span> 
        bir yapıya sahiptir:
    </p>
    <ul>
        <li>Kendi hukuki belgelerinizi sisteme ekleyebilirsiniz</li>
        <li>Belirli hukuk alanlarına odaklanacak şekilde eğitebilirsiniz</li>
        <li>Firma logonuz ve renk şemanızla özelleştirebilirsiniz</li>
        <li>Farklı dillerde hizmet verecek şekilde yapılandırabilirsiniz</li>
        <li>API entegrasyonu ile mevcut sistemlerinize bağlayabilirsiniz</li>
    </ul>
</div>
""", unsafe_allow_html=True)
