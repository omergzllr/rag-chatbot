import os
from PyPDF2 import PdfReader
from typing import List, Dict
from config import PDF_DIRECTORY, CHUNK_SIZE, CHUNK_OVERLAP


class PDFProcessor:
    """PDF dosyalarını işleyen sınıf"""
    
    def __init__(self, pdf_directory: str = PDF_DIRECTORY):
        self.pdf_directory = pdf_directory
        os.makedirs(pdf_directory, exist_ok=True)
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Tek bir PDF'den metin çıkarır"""
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"PDF okuma hatası ({pdf_path}): {e}")
            return ""
    
    def process_all_pdfs(self) -> List[Dict[str, str]]:
        """Tüm PDF'leri işler ve metadata ile birlikte döner"""
        documents = []
        
        if not os.path.exists(self.pdf_directory):
            print(f"Uyarı: {self.pdf_directory} dizini bulunamadı")
            return documents
        
        pdf_files = [f for f in os.listdir(self.pdf_directory) if f.endswith('.pdf')]
        
        for pdf_file in pdf_files:
            pdf_path = os.path.join(self.pdf_directory, pdf_file)
            text = self.extract_text_from_pdf(pdf_path)
            
            if text:
                documents.append({
                    'content': text,
                    'source': pdf_file,
                    'type': 'hukuk_belgesi'
                })
                print(f"✓ İşlendi: {pdf_file}")
        
        return documents
    
    def chunk_text(self, text: str, chunk_size: int = CHUNK_SIZE, 
                   overlap: int = CHUNK_OVERLAP) -> List[str]:
        """Metni parçalara ayırır"""
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += chunk_size - overlap
        
        return chunks
