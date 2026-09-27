# İlk Teknik Seçim Kaydı

## Seçim amacı

İlk teknikler; güvenli biçimde emüle edilebilme, Sysmon ile gözlemlenebilme, en az iki farklı uygulama varyantına sahip olma ve birbirinden öğrenilebilir davranışlar üretme ölçütleriyle seçilmiştir.

## Aday teknikler

| Teknik | Neden seçildi? | Araştırma riski |
|---|---|---|
| T1059.001 PowerShell | Zengin süreç ve komut bağlamı; çok sayıda varyant | Model yalnızca `powershell.exe` adını ezberleyebilir |
| T1059.003 Windows Command Shell | PowerShell ile karışabilecek iyi bir karşı sınıf | Komut kabuğu kullanımı tek başına kötü niyetli değildir |
| T1082 System Information Discovery | Zararsız ve tekrar üretilebilir keşif davranışı | Basit tek komutlar kolay ezberlenebilir |
| T1033 System Owner/User Discovery | Normal yönetim davranışıyla anlamlı örtüşme | T1082 ile aynı oturumlarda birlikte görülebilir |
| T1083 File and Directory Discovery | Süreç ve dosya davranışı sağlar | Normal dosya gezintisiyle güçlü sınıf örtüşmesi |
| T1053.005 Scheduled Task | Birden çok olay ve kalıcılık bağlamı üretir | Yönetici yetkisi ve temizleme dikkat ister |

## Ezberlemeyi önleme kuralları

- Dosya yolları, kullanıcı adları ve geçici adlar varyantlar arasında değiştirilir.
- Aynı teknik için en az iki ayrı test kimliği veya uygulama biçimi kullanılır.
- Test kimliği model girdisine verilmez.
- Ham komut satırı hem tam hem anonimleştirilmiş biçimde ayrı deneylerde değerlendirilir.
- Bir varyant bütünüyle test bölümünde tutulur.
- `powershell.exe` gibi tek belirteçlere dayalı başarının görülmesi için özellik çıkarma deneyleri yapılır.

## Teknik kabul ölçütü

Bir teknik veri toplama kapsamına ancak şu koşullarda alınır:

1. Güncel ATT&CK kimliği ve adı doğrulanmıştır.
2. Atomic test içeriği ve temizleme komutu elle incelenmiştir.
3. Test kamuya açık hedef, gerçek kimlik bilgisi veya kalıcı uzaktan erişim gerektirmez.
4. Sysmon yapılandırması ilgili davranışı gözlemleyebilir.
5. En az iki güvenli varyant tanımlanabilir.
6. Pilot oturum temiz anlık görüntüye dönüşle tamamlanabilir.

## Sonraki karar

Bir sonraki oturumda Atomic Red Team kataloğundaki aday testler salt-okunur biçimde incelenecek, komutlar çalıştırılmadan önce güvenli test kimlikleri ve temizleme gereksinimleri kayıt altına alınacaktır.

