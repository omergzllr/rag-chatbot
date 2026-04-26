#!/usr/bin/env python3
"""
Basit Arama - LLM olmadan sadece PDF'lerden arama yapar
"""
from pdf_processor import PDFProcessor
from vector_store import VectorStore


def main():
    print("🚀 Basit Arama Sistemi Başlatılıyor...")
    
    # PDF'leri işle
    processor = PDFProcessor()
    documents = processor.process_all_pdfs()
    
    if not documents:
        print("⚠️  Hiç PDF bulunamadı. Lütfen 'pdfs' klasörüne PDF dosyaları ekleyin.")
        return
    
    # Vektör veritabanına ekle
    print("🔄 Belgeler vektör veritabanına ekleniyor...")
    vector_store = VectorStore()
    vector_store.add_documents(documents)
    
    print("✅ Sistem hazır!")
    print("\n" + "="*60)
    print("🔍 Basit Arama Sistemi")
    print("="*60)
    print("Komutlar:")
    print("  - Arama yapmak için yazın")
    print("  - 'çıkış' veya 'exit' yazarak çıkabilirsiniz")
    print("="*60 + "\n")
    
    while True:
        try:
            query = input("\n👤 Arama: ").strip()
            
            if query.lower() in ['çıkış', 'exit', 'quit', 'q']:
                print("👋 Görüşmek üzere!")
                break
            
            if not query:
                continue
            
            # İlgili belgeleri bul
            print("🔍 Aranıyor...")
            results = vector_store.search(query, top_k=5)
            
            if not results:
                print("❌ Sonuç bulunamadı.")
                continue
            
            print(f"\n📚 {len(results)} sonuç bulundu:\n")
            
            for i, doc in enumerate(results, 1):
                print(f"--- Sonuç {i} ---")
                print(f"📄 Kaynak: {doc['metadata']['source']}")
                print(f"📊 Benzerlik: {1 - doc['distance']:.2%}")
                print(f"📝 İçerik: {doc['content'][:300]}...")
                print()
            
        except KeyboardInterrupt:
            print("\n\n👋 Görüşmek üzere!")
            break
        except Exception as e:
            print(f"\n❌ Hata: {e}")


if __name__ == "__main__":
    main()
