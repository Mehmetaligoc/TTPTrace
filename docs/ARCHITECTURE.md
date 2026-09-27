# Sistem Mimarisi

## Güven bölgeleri

TTPTrace üç güven bölgesine ayrılır:

1. **Yönetim bölgesi:** Deney manifestlerinin ve araştırma kodunun bulunduğu makine.
2. **Yalıtılmış emülasyon bölgesi:** Anlık görüntülerden döndürülebilen Windows sanal makineleri.
3. **Analiz bölgesi:** Anonimleştirilmiş telemetrinin işlendiği ve modellerin eğitildiği ortam.

Ham telemetri, anonimleştirme ve kalite kontrol tamamlanmadan analiz/veri paylaşım bölgesine geçmez.

```text
Deney manifesti
      |
      v
İzin listeli emülasyon testi ----> Yalıtılmış Windows VM
                                      |
                                      v
                                Sysmon / Event Log
                                      |
                                      v
                              Ham oturum paketi
                                      |
                         doğrulama + anonimleştirme
                                      |
                                      v
                        olaylar / diziler / süreç grafı
                                      |
                     +----------------+----------------+
                     |                |                |
               Random Forest       LSTM/GRU       Transformer
                     |                |                |
                     +----------------+----------------+
                                      |
                                      v
                       genelleme ve kapsama raporu
```

## Veri hattı

1. Deney başlamadan manifest oluşturulur.
2. Manifest güvenlik ve şema kurallarından geçer.
3. Yalnızca izin listesindeki emülasyon testi çalıştırılır.
4. Başlangıç ve bitiş işaretleri ile olay günlüğü dışa aktarılır.
5. Kayıtlar ortak olay biçimine dönüştürülür.
6. Ortama özgü alanlar takma değerlere çevrilir.
7. Oturum bütünlüğü ve etiket tutarlılığı kontrol edilir.
8. Veri üç görünümde üretilir: tekil olay, zaman penceresi ve süreç ilişkili dizi.
9. Veri bölme işlemi oturum/test/makine grupları korunarak yapılır.
10. Modeller ve açıklamalar aynı sabit değerlendirme kümelerinde karşılaştırılır.

## Temel tasarım kararı

Bir oturumun olayları farklı veri bölümlerine dağıtılamaz. Aynı Atomic test varyantının tekrarları görülmeyen-varyant değerlendirmesinde eğitim ve test arasında karıştırılamaz. Bu kural veri sızıntısını önleyen ana ilkedir.

## İlk bileşenler

- `ttptrace.manifest`: deney sözleşmesi doğrulaması
- `configs/techniques.json`: sürümlenmiş teknik kataloğu
- `schemas/`: makinece okunabilir veri sözleşmeleri
- `examples/`: saldırı ve normal oturum örnekleri
- `data/raw/`: sürüm kontrolü dışında ham veri
- `data/processed/`: sürüm kontrolü dışında işlenmiş veri
- `reports/`: değerlendirme çıktıları

