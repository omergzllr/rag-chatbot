from dataclasses import dataclass
from enum import Enum
from typing import List


class CitizenDocType(str, Enum):
    EVICTION_NOTICE = "eviction_notice"
    CONSUMER_COMPLAINT = "consumer_complaint"
    CRIMINAL_COMPLAINT = "criminal_complaint"
    VEHICLE_SALE_CONTRACT = "vehicle_sale_contract"
    EMPLOYMENT_TERMINATION = "employment_termination"
    INCIDENT_REPORT = "incident_report"


@dataclass(frozen=True)
class DocumentField:
    key: str
    label: str
    required: bool = True


@dataclass(frozen=True)
class DocumentTypeDefinition:
    doc_type: CitizenDocType
    title: str
    description: str
    fields: List[DocumentField]
    legal_notice: str


DOCUMENT_TYPES = {
    CitizenDocType.EVICTION_NOTICE: DocumentTypeDefinition(
        doc_type=CitizenDocType.EVICTION_NOTICE,
        title="Kiraci Tahliye Ihtarnamesi",
        description="Kiralanan tasinmazin tahliyesine yonelik ihtarname taslagi",
        fields=[
            DocumentField("tenant_full_name", "Kiraci ad soyad"),
            DocumentField("tenant_address", "Kiraci adresi"),
            DocumentField("property_address", "Tasinmaz adresi"),
            DocumentField("contract_date", "Kira sozlesmesi tarihi"),
            DocumentField("eviction_reason", "Tahliye gerekcesi"),
            DocumentField("notice_days", "Verilen sure (gun)"),
        ],
        legal_notice="Bu taslak bilgilendirme amaclidir; noter/avukat kontrolu onerilir.",
    ),
    CitizenDocType.CONSUMER_COMPLAINT: DocumentTypeDefinition(
        doc_type=CitizenDocType.CONSUMER_COMPLAINT,
        title="Tuketici Hakem Heyeti Basvurusu",
        description="Ayipli mal/hizmet iadesi degisim talebi dilekcesi",
        fields=[
            DocumentField("applicant_full_name", "Basvuran ad soyad"),
            DocumentField("seller_name", "Satici/servis unvani"),
            DocumentField("incident_date", "Olay tarihi"),
            DocumentField("purchase_amount", "Urun/hizmet bedeli"),
            DocumentField("request_type", "Talep (iade/degisim/onarim)"),
            DocumentField("incident_summary", "Olay ozeti"),
        ],
        legal_notice="Nihai basvuru oncesi belgeleri ve tutarlari resmi sinirlarla kontrol edin.",
    ),
    CitizenDocType.CRIMINAL_COMPLAINT: DocumentTypeDefinition(
        doc_type=CitizenDocType.CRIMINAL_COMPLAINT,
        title="Suc Duyurusu Dilekcesi",
        description="Savciliga sunulacak suc duyurusu taslagi",
        fields=[
            DocumentField("complainant_full_name", "Sikayetci ad soyad"),
            DocumentField("suspect_info", "Supheli bilgisi"),
            DocumentField("incident_date", "Olay tarihi"),
            DocumentField("incident_location", "Olay yeri"),
            DocumentField("crime_type", "Suc turu"),
            DocumentField("incident_summary", "Olay anlatimi"),
        ],
        legal_notice="Agir ceza veya acil risk durumlarinda dogrudan avukata basvurun.",
    ),
    CitizenDocType.VEHICLE_SALE_CONTRACT: DocumentTypeDefinition(
        doc_type=CitizenDocType.VEHICLE_SALE_CONTRACT,
        title="Arac Satis Sozlesmesi",
        description="Basit arac satisina yonelik sozlesme taslagi",
        fields=[
            DocumentField("seller_full_name", "Satici ad soyad"),
            DocumentField("buyer_full_name", "Alici ad soyad"),
            DocumentField("vehicle_info", "Arac bilgileri"),
            DocumentField("sale_price", "Satis bedeli"),
            DocumentField("sale_date", "Satis tarihi"),
            DocumentField("delivery_terms", "Teslim kosullari"),
        ],
        legal_notice="Noter islemleri ve vergi yukumluluklerini resmi kanallardan dogrulayin.",
    ),
    CitizenDocType.EMPLOYMENT_TERMINATION: DocumentTypeDefinition(
        doc_type=CitizenDocType.EMPLOYMENT_TERMINATION,
        title="Is Hukuku Fesih Dilekcesi",
        description="Hakli nedenle fesih/istifa veya alacak talep metni",
        fields=[
            DocumentField("employee_full_name", "Calisan ad soyad"),
            DocumentField("employer_name", "Isveren unvani"),
            DocumentField("employment_start_date", "Ise giris tarihi"),
            DocumentField("termination_date", "Fesih tarihi"),
            DocumentField("termination_reason", "Fesih gerekcesi"),
            DocumentField("claims", "Talep edilen hak/alacaklar"),
        ],
        legal_notice="Sureli basvurular icin zaman asimi ve arabuluculuk kosullarini kontrol edin.",
    ),
    CitizenDocType.INCIDENT_REPORT: DocumentTypeDefinition(
        doc_type=CitizenDocType.INCIDENT_REPORT,
        title="Olay/Tespit Tutanagi",
        description="Trafik, apartman veya teslim tutanagi taslagi",
        fields=[
            DocumentField("report_type", "Tutanak tipi"),
            DocumentField("incident_date", "Tarih"),
            DocumentField("incident_location", "Yer"),
            DocumentField("parties", "Taraflar"),
            DocumentField("findings", "Tespitler"),
            DocumentField("signatures", "Imza bilgileri"),
        ],
        legal_notice="Resmi tutanaklar ilgili kurum formatina gore ayrica duzenlenmelidir.",
    ),
}


def list_document_catalog() -> list:
    return [
        {
            "doc_type": item.doc_type.value,
            "title": item.title,
            "description": item.description,
        }
        for item in DOCUMENT_TYPES.values()
    ]
