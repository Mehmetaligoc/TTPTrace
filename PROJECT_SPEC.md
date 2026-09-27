# TTPTrace Proje Tanımı

## Amaç

TTPTrace, kontrollü adversary emulation oturumlarında oluşan Windows uç nokta telemetrisini MITRE ATT&CK teknikleriyle ilişkilendiren bir araştırma ve analiz platformudur. Sistem, belirli komutları veya dosya yollarını ezberlemek yerine süreç ilişkileri ile olay sırasını öğrenmeyi hedefler.

## Araştırma soruları

1. `ProcessGuid` ve ebeveyn-çocuk süreç ilişkileri, sabit zaman pencerelerine göre teknik sınıflandırmasını iyileştirir mi?
2. LSTM/GRU ve küçük Transformer modelleri klasik modellerden daha iyi genelleme sağlar mı?
3. Model, eğitimde görmediği bir test varyantını aynı ATT&CK tekniğiyle eşleştirebilir mi?
4. Bir makinede eğitilen model başka bir Windows makinesinde çalışabilir mi?
5. Ortama özgü alanların anonimleştirilmesi ezberlemeyi azaltır mı?
6. Model kararları analiste olay düzeyinde açıklanabilir mi?

## Hipotezler

- Süreç ilişkili diziler, bağımsız olaylardan daha yüksek Macro F1 sağlayacaktır.
- Rastgele ayrım sonucu, görülmeyen varyant ve görülmeyen makine sonuçlarından daha yüksek olacaktır.
- Ortama özgü belirteçlerin anonimleştirilmesi rastgele ayrım başarısını düşürebilir ancak dış ortam genellemesini iyileştirebilir.
- Derin modeller özellikle birden fazla olaya yayılan tekniklerde klasik modellere göre avantaj gösterecektir.

## Minimum çalışan ürün

- 6 ATT&CK tekniği ve normal sınıf
- 2 Windows sanal makinesi
- Teknik başına en az 2 güvenli test varyantı
- Sysmon olaylarının JSON/CSV biçiminde dışa aktarılması
- Deney manifestiyle güvenilir etiketleme
- Bağımsız olay ve süreç ilişkili dizi veri kümeleri
- Random Forest temel modeli
- LSTM veya GRU modeli
- Dosyadan analiz yapan arayüz
- Rastgele, görülmeyen varyant ve görülmeyen makine değerlendirmeleri

## Genişletilmiş hedefler

- Küçük Transformer Encoder
- Canlı olay akışı
- CALDERA entegrasyonu
- ATT&CK Navigator katmanı
- Temporal Graph Neural Network
- Model destekli kapsama testi önerileri

## Başarı ölçütleri

Ana ölçüt Macro F1 olacaktır. Ek olarak teknik başına precision/recall, Weighted F1, Top-3 doğruluk, yanlış pozitif oranı, kalibrasyon hatası ve tahmin süresi raporlanacaktır.

Model başarısı yalnızca rastgele ayrımda raporlanmayacaktır. Projenin ana sonucu görülmeyen varyant ve görülmeyen makine deneyleridir.

## Çıktılar

- anonimleştirilmiş ve sürümlenmiş veri kümesi,
- deney üretim ve doğrulama araçları,
- eğitilmiş modeller ve model kartları,
- analiz arayüzü,
- tekrar üretilebilir deney raporu,
- bitirme tezi, sunum ve demo videosu.

