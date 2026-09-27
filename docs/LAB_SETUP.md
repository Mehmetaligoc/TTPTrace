# Yalıtılmış Laboratuvar Kurulum Planı

Bu belge ikinci çalışma oturumunda uygulanacak laboratuvar tasarımını tanımlar. Henüz herhangi bir emülasyon testi çalıştırılmaz.

## Önerilen ilk topoloji

```text
                    Yönetim bilgisayarı
                           |
                    yalnızca yönetim
                           |
             +-------------+-------------+
             |                           |
        HOST-WIN01                    HOST-WIN02
       eğitim/pilot                 dış test makinesi
             |                           |
             +------ iç sanal ağ --------+
```

İlk sürümde ayrı bir etki alanı denetleyicisi veya CALDERA sunucusu zorunlu değildir. Önce iki Windows uç noktası ve dosya tabanlı telemetri hattı doğrulanır.

## Ağ kuralları

- Bridged ağ kullanılmaz.
- Deney ağı `host-only` veya `internal network` olarak kurulur.
- Güncelleme gerektiğinde geçici NAT açılır ve deneyden önce kapatılır.
- Gelen bağlantı noktaları fiziksel ağa yayımlanmaz.
- Sanal ağ aralığı gerçek ev/okul ağıyla çakışmaz.
- Her deney öncesi ağ modu manifest dışı kontrol listesinde doğrulanır.

## Sanal makineler

Her iki VM için:

- Windows sürümü ve build numarası kaydedilir.
- Yerel, sahte laboratuvar hesabı kullanılır.
- Gerçek Microsoft hesabı veya kişisel dosya kullanılmaz.
- Sysmon kurulmadan önce `base-clean` anlık görüntüsü alınır.
- Sysmon ve günlük ayarlarından sonra `telemetry-ready-v1` görüntüsü alınır.
- Deneylerden sonra aynı görüntüye dönüş denenir.

## Zaman ve kimlik

- İki VM aynı zaman kaynağını kullanır.
- Olaylar analiz sırasında UTC'ye çevrilir.
- Gerçek makine adları veri kümesine yazılmaz; `HOST-WIN01` ve `HOST-WIN02` kullanılır.
- Her oturum benzersiz `TTPT-*` deney kimliği taşır.

## Telemetri kabul kontrolü

Pilot deneyden önce aşağıdakiler doğrulanır:

- Sysmon Operational günlüğü olay üretiyor.
- Process Create olayında `ProcessGuid` bulunuyor.
- Ebeveyn süreç alanları kaydediliyor.
- Ağ bağlantısı ve dosya oluşturma olayları yapılandırmaya göre görülebiliyor.
- Olay zamanları saat dilimiyle dışa aktarılabiliyor.
- Kullanılan Sysmon yapılandırmasının SHA-256 özeti manifestte kayıtlı.

## Deney yaşam döngüsü

1. VM anlık görüntüsü ve ağ modu kontrol edilir.
2. Manifest taslağı oluşturulur ve doğrulanır.
3. Günlük başlangıç işareti kaydedilir.
4. Önceden incelenmiş tek bir emülasyon testi çalıştırılır.
5. Bitiş işareti kaydedilir.
6. Olaylar deney klasörüne dışa aktarılır.
7. Testin temizleme adımı uygulanır.
8. VM temiz anlık görüntüye döndürülür.
9. Manifest ve olay paketi kalite kontrolünden geçer.

## Kurulum günü tamamlanma ölçütü

Laboratuvar, yalnızca aşağıdaki kanıtlar mevcutsa hazır kabul edilir:

- iki VM'nin anlık görüntü listesi,
- ağ yalıtım ekranı veya yapılandırma çıktısı,
- zararsız bir süreç başlatma olayını içeren Sysmon dışa aktarımı,
- gerçek yapılandırma özetiyle doğrulanan bir benign manifest,
- VM geri dönüş testinin başarılı olması.

