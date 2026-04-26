#!/usr/bin/env python3
"""
Soru logunu görüntüle
"""
import json
import os
from datetime import datetime


def view_questions():
    log_file = "questions_log.json"
    
    if not os.path.exists(log_file):
        print("❌ Henüz hiç soru sorulmamış.")
        return
    
    with open(log_file, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    if not questions:
        print("❌ Henüz hiç soru sorulmamış.")
        return
    
    print("\n" + "="*80)
    print(f"📊 SORU LOGU - Toplam {len(questions)} soru")
    print("="*80 + "\n")
    
    # Araştırılması gereken soruları say
    needs_research = [q for q in questions if q.get('needs_research', False)]
    
    print(f"✅ Belgede bulunan: {len(questions) - len(needs_research)}")
    print(f"🔍 Araştırılması gereken: {len(needs_research)}\n")
    
    for i, q in enumerate(questions, 1):
        timestamp = datetime.fromisoformat(q['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        status = "🔍 ARAŞTIR" if q.get('needs_research', False) else "✅ BULUNDU"
        
        print(f"--- Soru {i} [{status}] ---")
        print(f"⏰ Zaman: {timestamp}")
        print(f"❓ Soru: {q['question']}")
        print(f"💬 Cevap: {q['answer'][:100]}...")
        if q['sources']:
            print(f"📚 Kaynaklar: {', '.join(q['sources'])}")
        print()
    
    # Araştırılması gereken soruları ayrı göster
    if needs_research:
        print("\n" + "="*80)
        print("🔍 ARAŞTIRILMASI GEREKEN SORULAR")
        print("="*80 + "\n")
        
        for i, q in enumerate(needs_research, 1):
            print(f"{i}. {q['question']}")
        print()


if __name__ == "__main__":
    view_questions()
