# Sonraki Çalışma Oturumu

## Hedef

İki Windows sanal makinesinden oluşan yalıtılmış laboratuvarın tasarımını kesinleştirmek ve ilk benign Sysmon kaydını manifestle birlikte üretmek.

## Kullanıcıdan gerekecek bilgiler

- Kullanılacak sanallaştırma yazılımı: VMware, VirtualBox veya Hyper-V
- Bilgisayarın yaklaşık RAM ve boş disk kapasitesi
- Hazır Windows sanal makinesi olup olmadığı
- Windows sürümü

## Yapılacak işler

1. Donanıma göre VM kaynaklarını belirleme
2. İç sanal ağ oluşturma
3. `base-clean` anlık görüntülerini alma
4. Sysmon sürüm ve yapılandırma stratejisini seçme
5. Zararsız süreçlerle telemetri kontrolü
6. Gerçek yapılandırma özetiyle benign manifest oluşturma
7. Olay dışa aktarma biçimini kesinleştirme

## Bu aşamada yapılmayacaklar

- Atomic test çalıştırma
- CALDERA kurma
- Model eğitme
- Canlı zararlı yazılım kullanma

