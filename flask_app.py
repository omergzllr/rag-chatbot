from flask import Flask, render_template, request, jsonify
from functools import lru_cache
from dotenv import load_dotenv
import os

load_dotenv()  # .env dosyasından key'leri yükle

app = Flask(__name__)

# Debug modda watchdog'un çok fazla dosya izlemesini engelle
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

EXAMPLE_QUESTIONS = [
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

@lru_cache(maxsize=1)
def get_chatbot():
    from rag_chatbot import RAGChatbot
    chatbot = RAGChatbot()
    chatbot.initialize()
    return chatbot

# ===== PAGES =====
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html', example_questions=EXAMPLE_QUESTIONS)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# ===== API =====
@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.get_json()
    question = data.get('question', '').strip()
    if not question:
        return jsonify({'error': 'Soru boş olamaz'}), 400
    try:
        chatbot = get_chatbot()
        result = chatbot.ask(question)
        return jsonify({'answer': result['answer']})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'answer': f'Sistem hatası: {str(e)}'}), 200

@app.route('/api/contact', methods=['POST'])
def api_contact():
    data = request.get_json()
    # Burada e-posta gönderimi veya DB kaydı yapılabilir
    return jsonify({'success': True, 'message': 'Mesajınız alındı!'})

if __name__ == '__main__':
    app.run(debug=False, port=5000)  # debug=False - watchdog reload sorunu çözülür
