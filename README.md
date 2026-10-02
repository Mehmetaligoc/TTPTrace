# TTPTrace

**Derin öğrenme ile genellenebilir MITRE ATT&CK teknik tanıma ve adversary emulation analiz platformu.**

TTPTrace, sahibine ait ve yalıtılmış bir Windows laboratuvarında gerçekleştirilen kontrollü güvenlik testlerinden oluşan uç nokta telemetrisini işler. Amaç, modelin belirli komutları ezberlemesi yerine süreç ilişkilerini ve olay dizilerini kullanarak MITRE ATT&CK tekniklerini tanıyıp tanıyamadığını ölçmektir.

## Araştırma hedefi

Ana araştırma sorusu:

> Sysmon olayları süreç ağacı ve zaman ilişkileriyle birlikte modellendiğinde, eğitim sırasında görülmeyen test uygulamaları ve farklı makinelerdeki Red Team faaliyetleri ATT&CK tekniği düzeyinde ne ölçüde doğru sınıflandırılabilir?

Projenin ayırt edici değerlendirmeleri:

- görülmeyen Atomic test varyantı,
- görülmeyen Windows makinesi,
- ortam bilgilerinin anonimleştirilmesi,
- eksik telemetri altında dayanıklılık,
- olay düzeyinde açıklanabilirlik,
- model sonucuna göre ATT&CK kapsama boşluğu analizi.

## İlk sürümün kapsamı

İlk sürüm altı güncel ATT&CK tekniğine odaklanır:

| Kimlik | Teknik | Taktik |
|---|---|---|
| T1059.001 | PowerShell | Execution |
| T1059.003 | Windows Command Shell | Execution |
| T1082 | System Information Discovery | Discovery |
| T1033 | System Owner/User Discovery | Discovery |
| T1083 | File and Directory Discovery | Discovery |
| T1053.005 | Scheduled Task | Execution / Persistence / Privilege Escalation |

Teknik listesi veri toplama başlamadan önce danışmanla kesinleştirilecektir. Kapsam bütün ATT&CK matrisini temsil etme iddiası taşımaz.

## Güvenlik sınırı

Bu depo kamuya açık hedeflere yönelik otomasyon veya izinsiz test için tasarlanmamıştır. Deneylerin yalnızca sahibine ait, yalıtılmış sanal makinelerde ve önceden incelenmiş güvenli emülasyon testleriyle yürütülmesi gerekir. Ayrıntılar [SECURITY.md](SECURITY.md) içindedir.

## Mevcut durum

İlk iskelet aşağıdakileri içerir:

- proje ve araştırma tanımı,
- laboratuvar mimarisi,
- deney manifesti şeması,
- manifest doğrulama modülü ve komut satırı aracı,
- örnek saldırı ve normal oturum manifestleri,
- temel otomatik testler,
- 14 haftalık yol haritası.

## Oturum analizi ve ağ özellikleri

[01_session_analysis.ipynb](01_session_analysis.ipynb) ilk benign oturum için Colab üzerinde geliştirilen analiz akışını içerir:

- JSONL okuma, SHA-256 bütünlük kontrolü ve manifest/olay kimliği doğrulaması,
- ProcessGuid ile süreç ve ebeveyn ilişkilerinin incelenmesi,
- ağ olaylarının oturum içi ve oturum öncesi süreç kayıtlarıyla eşleştirilmesi,
- süreç başına hedef çeşitliliği, TCP/UDP dağılımı ve oturum süresine göre olay sıklığı,
- JSONL çıktılarının kayıt kaybı olmadan yazılıp yeniden okunmasının kontrolü.

İlk oturumda 269 olayın 194'ü ağ olayıdır. Ağ olaylarının 53'ü oturum içi, 139'u oturum öncesi süreç kayıtlarıyla eşleşir; iki olay çözümlenmemiş olarak korunur. Ağ olayı bulunan altı süreç için özellik özeti oluşturulmuştur. Bunlar veri hazırlama kontrolleridir; model başarımı ölçümü değildir. Model eğitimi ve DNS özellikleri henüz uygulanmamıştır.

**Çalıştırma:** Notebook'u Colab'da açın; `events.jsonl`, `analysis-summary.json`, `manifest.json` ve `process-context.jsonl` dosyalarını `/content` altına yükleyip hücreleri sırayla çalıştırın. Bu sürümün hash değerleri ve beklenen sayıları ilk oturuma özgüdür; farklı oturumlara uyarlanmadan genel analiz aracı olarak kullanılamaz. Kamuya açık örnek telemetri henüz sağlanmamaktadır.

Notebook çıktıları ve hesap/çalışma ortamı metaverileri temizlenmiştir. Ham telemetri ve üretilen JSONL dosyaları depoya dahil edilmez. Colab'daki geçici çıktıları indirerek yerel `data/processed/` altında saklayın.

## Hızlı başlangıç

Python 3.12 önerilir. İlk doğrulama aracı yalnızca Python standart kütüphanesini kullanır.

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -e .
.venv\Scripts\python.exe -m ttptrace validate examples\attack_manifest.example.json
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Belgeler

- [Proje tanımı](PROJECT_SPEC.md)
- [Sistem mimarisi](docs/ARCHITECTURE.md)
- [Veri modeli](docs/DATA_MODEL.md)
- [14 haftalık yol haritası](docs/ROADMAP.md)
- [Laboratuvar güvenliği](SECURITY.md)

## Proje aşamaları

1. Deney sözleşmesi ve laboratuvar tasarımı
2. Sysmon telemetri toplama
3. Kontrollü ve etiketli veri üretimi
4. Süreç ağacı ve zaman dizisi oluşturma
5. Temel makine öğrenmesi modeli
6. LSTM/GRU ve Transformer karşılaştırması
7. Genelleme deneyleri
8. Açıklanabilirlik ve ATT&CK kapsama arayüzü

## Lisans durumu

Proje için henüz lisans seçilmemiştir. Kaynak kodu ve veri paylaşım koşulları; Atomic Red Team, MITRE ATT&CK, Sysmon ve kullanılan diğer bileşenlerin koşulları incelendikten sonra belirlenecektir.