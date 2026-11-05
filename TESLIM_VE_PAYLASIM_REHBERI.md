# SE PRIMER: ÖDEV TESLİM, VİDEO KAYIT VE LINKEDIN PAYLAŞIM REHBERİ

Bu rehber, **Samsun Üniversitesi Yazılım Mühendisliği YZM301 Yazılım Testi** dersi (Prof. Dr. Nurettin Şenyer) için hazırlanan **SE Primer AI Tutor** projesinin GitHub'a yüklenmesi, video kaydının çekilmesi ve LinkedIn'de paylaşılması için adım adım hazırlanmıştır.

---

## 1. GITHUB'A YÜKLEME ADIMLARI

Proje yerel olarak Git ile başlatılmış (`git init`), `.gitignore` ve `README.md` dahil tüm dosyalar `main` dalına ilk commit ile kaydedilmiştir.

### GitHub'a Göndermek İçin:
1. Tarayıcınızda [github.com/new](https://github.com/new) adresine gidin.
2. **Repository name** olarak `se-primer-ai-tutor` yazın.
3. Gizliliği **Public (Genel)** seçin.
4. *"Initialize this repository with a README"* veya *.gitignore* kutucuklarını **işaretlemeyin** (çünkü yerelde zaten hazırlandı).
5. **Create repository** butonuna tıklayın.
6. Bilgisayarınızda terminali (PowerShell) açıp şu iki komutu sırasıyla çalıştırın:
   ```bash
   cd "c:\Users\admin\OneDrive\Masaüstü\Grafik Final Proje\SE_Primer_Projesi"
   git remote add origin https://github.com/eceyologlu2003-bot/se-primer-ai-tutor.git
   git push -u origin main
   ```
*(GitHub kullanıcı şifresi yerine GitHub Personal Access Token (PAT) veya tarayıcı onay penceresi açılırsa onaylayınız).*

---

## 2. DEMO VİDEO KAYIT SENARYOSU (1.5 - 2 DAKİKA)

> [!TIP]
> **Video Kayıt Aracı:** Windows'ta `Win + Alt + R` tuşlarına basarak dahili Windows Game Bar ile veya [Loom / OBS Studio] ile ekranınızı ve sesinizi kaydedebilirsiniz.

### 🎬 Dakika Dakika Video Metni & Ekran Hareketleri

#### ⏱️ [00:00 - 00:25] GİRİŞ & KAVRAMSAL ÇERÇEVE
- **Ekranda Ne Olacak:** [`index.html`](index.html) sayfasının başlığı, slayt önizleme karuseli ve projenin üst kısmı görünür.
- **Ne Söyleyeceksiniz (Sesli Anlatım):**
  > *"Merhaba, ben Ece Yoloğlu. Samsun Üniversitesi Yazılım Mühendisliği 3. sınıf öğrencisiyim. Bu videoda, YZM301 Yazılım Testi, Doğrulama ve Geçerleme dersimiz kapsamında Prof. Dr. Nurettin Şenyer hocamızın verdiği 'SE Primer: Yazılım Mühendisliği, Oynanan Bir Kitap' projesini sunuyorum.  
  > Projemizin temel felsefesi Neal Stephenson'ın 'The Diamond Age' romanındaki akıllı eğitmen konseptine dayanıyor: 'Her seçim bir durum geçişi. Her son bir kabul kriteri.' Bu ilkeden yola çıkarak Şehir Hastanesi'nin sabah 08:00'deki 50.000 kişilik randevu trafiğini yönettiğimiz etkileşimli bir durum makinesi (FSM) ve AI destekli test simülatörü geliştirdik."*

#### ⏱️ [00:25 - 00:55] 1. SENARYO: 08:00 SİSTEM ÇÖKÜŞÜ (HATA DURUMU)
- **Ekranda Ne Olacak:** Oynanabilir Hikâye Motorunda hatalı seçimlere tıklayın:
  1. Adım 1: "2) Doğrudan veritabanına SQL SELECT ve UPDATE sorgusu at" butonuna basın.
  2. Adım 2: "2) Geliştirici ortamında 1 kullanıcıyla Happy Path testi yap" butonuna basın.
  3. Adım 3: "2) Güvenlik filtrelerini ertele" butonuna basın.
  4. Adım 4: "2) Basit kural tabanlı model kullan" butonuna basın.
  - FSM diyagramındaki `S6: ÇÖKTÜ` düğümünün kırmızı yandığını ve terminalde hata loglarını gösterin.
- **Ne Söyleyeceksiniz:**
  > *"Şimdi simülatörümüzde önce hatalı bir mühendislik senaryosu deneyelim. Eşzamanlılık kilit mekanizması yerine basit SQL sorguları seçtiğimizde ve yük testini atladığımızda, saat 08:00 olduğu an 50.000 eşzamanlı istek sebebiyle sistem 'Race Condition' ve 'Deadlock' yaşayarak çöküyor. Gördüğünüz gibi FSM grafiğimiz kırmızı renkle S6 Çöküş durumuna geçti ve kabul kriterlerimizin tamamı 'KALDI (FAILED)' durumuna düştü."*

#### ⏱️ [00:55 - 01:25] 2. SENARYO: 08:00 RANDEVU BAŞARILI (BAŞARILI DURUM)
- **Ekranda Ne Olacak:** `Yeniden Başlat ↺` butonuna basın ve bu kez doğru mühendislik seçimlerini yapın:
  1. Adım 1: "1) Redis Dağıtık Kilit (Redlock) + DB Connection Pool"
  2. Adım 2: "1) JMeter ile 50.000 sanal kullanıcı yük ve sınır değer testleri"
  3. Adım 3: "1) Token Bucket Rate Limiter ve SQLi sanitizasyonu"
  4. Adım 4: "1) BERT tabanlı poliklinik sınıflandırma modeli"
  - `S5: BAŞARI` düğümünün yeşil parladığını ve tüm Kabul Kriterleri (AC-01..AC-04) kartlarının yeşile dönüp `GEÇTİ (PASSED)` olduğunu gösterin.
- **Ne Söyleyeceksiniz:**
  > *"Şimdi sistemi sıfırlayıp doğru mühendislik kararlarıyla ilerleyelim. Redis Dağıtık Kilit ile transaction bütünlüğünü sağladık, 50.000 sanal kullanıcıyla yük testini koştuk ve güvenlik kalkanını açtık. Saat 08:00:00 olduğunda sistem P99 gecikmeyi 180 milisaniyede tutarak 0 hata ile çalıştı. FSM grafiğimiz S5 Başarılı durumuna ulaştı ve Given-When-Then formatındaki 4 kabul kriterimizin tamamı yeşil olarak doğrulandı."*

#### ⏱️ [01:25 - 01:45] BERT TRİYAJ & CONFUSION MATRIX DEMOSU
- **Ekranda Ne Olacak:** Sayfayı aşağı kaydırıp BERT Semptom Triyaj kutusuna gelin. Metin kutusuna *"Sol kolum uyuşuyor, göğsüm sıkışıyor ve nefes alamıyorum"* yazıp `Modeli Çalıştır (BERT Inference)` butonuna basın (Kardiyoloji %95 çubuğunu gösterin). Ardından Hata Matrisindeki FN değerini gösterin.
- **Ne Söyleyeceksiniz:**
  > *"Projemizin ikinci önemli parçası makine öğrenmesi entegrasyonu. Sunumumuzun 3. slaytındaki BERT Transformer mimarisini hasta triyajı için simüle ettik. Örneğin hastanın girdiği şikayet metnini modelimiz yüzde 95 olasılıkla doğrudan Kardiyoloji polikliniğine yönlendiriyor.  
  > 6. slayttaki Hata Matrisinde ise tıbbi test prensibi gereği Yanlış Negatif (FN) oranını minimize ederek Duyarlılık (Recall) değerimizi yüzde 99.47 seviyesinde doğruladık."*

#### ⏱️ [01:45 - 02:00] KONSOL TESTLERİ & KAPANIŞ
- **Ekranda Ne Olacak:** Terminal ekranına geçin ve `python test_se_primer.py` komutunu çalıştırın. `Ran 5 tests in 0.000s ... OK` çıktısını gösterin.
- **Ne Söyleyeceksiniz:**
  > *"Tüm bu durum geçişleri ve kabul kriterleri Python unittest kütüphanesiyle de yazılmış olup, 5 test senaryomuzun tamamı hatasız geçmektedir. Beni dinlediğiniz için teşekkür ederim."*

---

## 3. LINKEDIN PAYLAŞIM METNİ

Aşağıdaki metni doğrudan kopyalayıp LinkedIn'de bir video veya ekran görüntüsü ekleyerek paylaşabilirsiniz:

```text
🎮 "Her seçim bir durum geçişi. Her son bir kabul kriteri."

Samsun Üniversitesi Yazılım Mühendisliği Bölümü'nde Prof. Dr. Nurettin Şenyer hocamızın rehberliğinde yürüttüğümüz YZM301 Yazılım Testi, Doğrulama ve Geçerleme dersi kapsamında geliştirdiğim "SE Primer: Yazılım Mühendisliği, Oynanan Bir Kitap" projesini tamamlamaktan büyük heyecan duyuyorum! 🚀

📚 Projenin Felsefesi:
Neal Stephenson'ın kült eseri "The Diamond Age"deki akıllı eğitmen (The Primer) vizyonundan ilham alarak; yazılım testi ve mimari kararlarını soyut teorilerden çıkarıp oynanabilir, dallanan bir vaka simülasyonuna (Playable Interactive Case Study) dönüştürdük.

🏥 Vaka: Şehir Hastanesi 08:00 Canlıya Geçişi
Sabah 08:00:00 anında 50.000 vatandaşın aynı anda hekim randevusu almaya çalıştığı pik yük anında Baş Test Mühendisi rolünü üstleniyoruz:
🔹 Dağıtık Kilit (Redis Redlock) vs Naive SQL (Race condition & Deadlock analizi)
🔹 JMeter ile 50k kullanıcı yük testi ve Sınır Değer Analizi (BVA)
🔹 Token Bucket Rate Limiting ile bot ve DDoS koruması
🔹 Doğal Dil İşleme: BERT Transformer mimarisi ile semptom-poliklinik triyajı
🔹 Model Doğrulama: Hata Matrisi (Confusion Matrix) üzerinde hayati önem taşıyan Yanlış Negatiflerin (FN) minimizasyonu ve %99.47 Recall başarımı.

🎯 BDD ve Kabul Kriterleri (Acceptance Criteria):
Gherkin (Given-When-Then) standardıyla kurguladığımız tüm kabul kriterleri otomatik Python unittest paketi ve interaktif web arayüzü ile %100 doğrulandı.

💻 Proje Kodları ve Detaylı Rapor:
GitHub: https://github.com/eceyologlu2003-bot/se-primer-ai-tutor

Değerli vizyonu ve rehberliği için hocam Prof. Dr. Nurettin Şenyer'e çok teşekkür ederim.

#YazılımTesti #SoftwareTesting #QualityAssurance #SDET #BDD #Cucumber #MachineLearning #BERT #Python #SamsunÜniversitesi #SoftwareEngineering #StateMachines
```

---

## 4. FORM VE CLASSROOM TESLİM BİLGİLERİ

Google Classroom ve Samsun Üniversitesi Yazılım Mühendisliği Ödev Teslim Formuna girilecek bilgiler:

- **Adı Soyadı:** Ece Yoloğlu
- **Öğrenci Numarası:** 241478071
- **E-posta:** 241478071@samsun.edu.tr
- **Ders:** YZM301 Yazılım Testi
- **Ödev:** Ödev 6 & Ödev 7 (AI Tutor: SE Primer v2)
- **GitHub Linki:** `https://github.com/eceyologlu2003-bot/se-primer-ai-tutor`
- **LinkedIn Gönderi Linki:** *(LinkedIn'de paylaştıktan sonra gönderinizin bağlantısını buraya ekleyin)*
- **Demo Video Linki:** *(Kaydettiğiniz videoyu Google Drive / YouTube / LinkedIn'e yükledikten sonra linkini ekleyin)*
