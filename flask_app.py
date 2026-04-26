from flask import Flask, render_template, request, jsonify
from functools import lru_cache
import os

app = Flask(__name__)

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
        return jsonify({'error': str(e)}), 500

@app.route('/api/contact', methods=['POST'])
def api_contact():
    data = request.get_json()
    # Burada e-posta gönderimi veya DB kaydı yapılabilir
    return jsonify({'success': True, 'message': 'Mesajınız alındı!'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
