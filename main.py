#!/usr/bin/env python3
"""
Hukuk RAG Chatbot - Ana Çalıştırma Dosyası
"""
import argparse
from rag_chatbot import RAGChatbot


def main():
    parser = argparse.ArgumentParser(description='Hukuk RAG Chatbot')
    parser.add_argument('--reload', action='store_true', 
                       help='PDF\'leri yeniden yükle')
    parser.add_argument('--query', type=str, 
                       help='Tek bir soru sor ve çık')
    
    args = parser.parse_args()
    
    # Chatbot'u başlat
    chatbot = RAGChatbot()
    
    if not chatbot.initialize(force_reload=args.reload):
        return
    
    # Tek soru modu
    if args.query:
        result = chatbot.ask(args.query)
        print(f"\n🤖 Cevap: {result['answer']}")
        print(f"\n📚 Kaynaklar: {', '.join(result['sources'])}")
        return
    
    # İnteraktif mod
    chatbot.chat_loop()


if __name__ == "__main__":
    main()
