# Deney ve Veri Modeli

## Deney manifesti neden gerekli?

Sysmon olayları tek başına hangi kontrollü testin ne zaman çalıştırıldığını güvenilir biçimde söylemez. Manifest, telemetriye dışarıdan eklenen doğrulanabilir deney bağlamıdır. Her oturum tek bir manifest ve benzersiz deney kimliği taşır.

## Temel varlıklar

### Experiment

- `experiment_id`: `TTPT-YYYYMMDD-IDENTIFIER`
- `session_type`: `attack` veya `benign`
- `technique_id`: saldırı oturumlarında ATT&CK kimliği
- `emulation.test_id`: kullanılan testin değişmez kimliği
- `emulation.variant`: araştırmadaki varyant grubu

### Host

- gerçek bilgisayar adı yerine anonim `host_id`
- işletim sistemi sürümü
- deneyden önceki anlık görüntü kimliği

### Window

- saat dilimli başlangıç ve bitiş zamanı
- bitiş zamanı başlangıçtan sonra olmalıdır

### Authorization

- deney kapsamı sahibine ait yalıtılmış laboratuvar olmalıdır
- onay ve ağ yalıtımı açıkça `true` olmalıdır

### Collection

- en az Sysmon veri kaynağı
- kullanılan Sysmon yapılandırmasının SHA-256 özeti

### Artifacts

- proje köküne göre güvenli göreli yollar
- ham olay dosyası Git deposuna eklenmez

## Planlanan ortak olay biçimi

İkinci aşamada her olay aşağıdaki ortak alanlara dönüştürülecektir:

| Alan | Açıklama |
|---|---|
| experiment_id | Oturum bağlantısı |
| timestamp | UTC olay zamanı |
| host_id | Anonim makine |
| event_id | Sysmon/Windows olay kimliği |
| process_guid | Oturum içi takma süreç kimliği |
| parent_process_guid | Ebeveyn süreç ilişkisi |
| image_token | Anonimleştirilmiş çalıştırılabilir dosya |
| command_tokens | Kontrollü biçimde dönüştürülmüş komut parçaları |
| destination_token | Anonim ağ hedefi |
| technique_id | Oturum etiketi veya null |
| is_benign | Normal oturum göstergesi |

## Veri bölme stratejileri

- **Random baseline:** Oturum grupları korunarak katmanlı ayrım
- **Leave-one-variant-out:** Bir test varyantı yalnızca testte
- **Leave-one-host-out:** Bir makine yalnızca testte
- **Telemetry ablation:** Belirli olay kaynakları çıkarılarak değerlendirme

Satır bazlı rastgele bölme kullanılmayacaktır; aynı oturumdan gelen olayların iki tarafa da düşmesi ciddi veri sızıntısı oluşturur.

