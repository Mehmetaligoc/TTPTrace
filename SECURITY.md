# Güvenlik ve Etik Kullanım

TTPTrace yalnızca yetkili güvenlik araştırması ve eğitim için geliştirilir.

## Zorunlu laboratuvar sınırları

- Deneyler yalnızca proje sahibine ait veya açıkça izin verilmiş sanal makinelerde yürütülür.
- Hedef makineler kişisel, okul veya iş ağından yalıtılır.
- Varsayılan laboratuvar ağı dışarıdan erişilebilir servis yayımlamaz.
- Gerçek kullanıcı kimlik bilgileri ve kişisel veriler kullanılmaz.
- Zararlı yazılım, kimlik bilgisi hırsızlığı ve kalıcı uzaktan erişim bileşenleri ilk kapsamın dışındadır.
- Her emülasyon testi çalıştırılmadan önce komutu, ön koşulları ve temizleme adımları elle incelenir.
- Otomatik çalıştırıcı yalnızca açık izin listesindeki test kimliklerini kabul eder.
- Süre sınırı, anlık görüntü ve deney sonrası temizleme uygulanır.
- Ham EVTX/PCAP dosyaları anonimleştirilmeden yayımlanmaz.

## Projenin yapmayacağı işler

- Kamuya açık hedef tarama veya saldırı
- İzinsiz zafiyet istismarı
- Gerçek kimlik bilgisi toplama
- Güvenlik kontrollerini gizlice aşma
- Kendiliğinden hedef seçen veya istismar yapan otonom saldırı

## Veri paylaşımı

Paylaşıma açılacak veri; kullanıcı adı, makine adı, IP adresi, ev dizini, alan adı, dosya yolu ve deney anahtarları açısından anonimleştirilir. Anonimleştirme sonrasında yeniden tanımlama riski ayrıca incelenir.

## Güvenlik açığı bildirimi

Bu araştırma kodunda güvenlik açığı bulunursa herkese açık bir issue içinde gerçek sır veya istismar ayrıntısı paylaşılmamalıdır. Depo yayımlandığında özel bildirim kanalı ayrıca belirtilecektir.

