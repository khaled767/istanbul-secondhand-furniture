# Medine Mobilya — Google Business Profile (GBP) veri paketi

Hazır kopyala-yapıştır metinler. Site tarafındaki bilgilerle birebir aynı tutulmalıdır
(NAP tutarlılığı): aynı işletme adı, aynı adres, aynı telefon.

Site kaynağı: `index.html` içindeki JSON-LD (FurnitureStore) ve `.html` sayfalarının
footer'ı. Bir değeri burada değiştirirseniz **sitede de değiştirin**.

---

## 1) Temel bilgiler

| Alan | Değer |
| --- | --- |
| İşletme adı | `Medine Mobilya` |
| Telefon | `+90 538 646 79 71` |
| WhatsApp | `05386467971` |
| Web sitesi | `https://spotcuistanbul.com` |
| Adres | `Mehterçeşme, Cumhuriyet Cd No:28, 34515 Esenyurt/İstanbul` |
| Çalışma saatleri | Her gün `08:00 – 22:00` (sitedeki `openingHoursSpecification` ile aynı) |
| Fiyat aralığı | `₺₺` |

> Adres doğrulaması: dükkân fiziksel olarak mevcut olduğu için posta kartı veya video
> doğrulaması istenebilir. Doğrulama tamamlanmadan profil haritada görünmez.

---

## 2) الموقف التجاري — نقرأ منه كل شيء

**نحن نشتري ولا نبيع.** لا نتعامل مع من يبحث عن شراء أثاث مستعمل؛ عميلنا هو من يريد
البيع. كل نص، وكل كلمة مفتاحية، وكل بيان في الملف يجب أن يخدم هذا الاتجاه. لا
تشغّل حملات تسوّق (Shopping/Performance Max) ولا تغذية منتجات: تلك تجلب مشترين.

## 3) Kategoriler

Google'ın kategori listesi kendi elinde; aşağıdakilerden **Google'ın sunduğu en yakın**
olanı seçin. İşletme **ikinci el eşya satın alıyor**, bu yüzden:

- Birincil kategori: `İkinci el mağazası` — Google'ın "eşya alan" işletmeler için sunduğu
  en yakın kategori budur. Google'da "satın alıyor" diye bir kategori yok; bu yüzden
  yönü kategoriyle değil **açıklama ve hizmetlerle** anlatmak gerekir (aşağıda öyle).
- İkinci kategori olarak `Mobilya mağazası` **sadece** dükkândan müşteriye satış da
  yapıyorsanız eklenir. Şu an sadece satın alıyorsanız eklemeyin — o kategori "mobilya
  satan yer" arayanları getirir ve telefonu boşa meşgul eder.

---

## 3) İşletme açıklaması (750 karakter sınırı — bu metin 704 karakter)

```
Medine Mobilya, İstanbul genelinde ikinci el eşya alım satımı yapan bir aile
işletmesidir. Esenyurt'taki merkez mağazamızdan koltuk takımı, yatak odası takımı,
yemek masası, gardırop, buzdolabı, çamaşır ve bulaşık makinesi, televizyon ve ofis
mobilyası alıp satıyoruz. Eşyalarınızın fotoğrafını WhatsApp'tan gönderin, dakikalar
içinde ücretsiz fiyat teklifi alın. Kendi nakliye araçlarımızla aynı gün adresinize
geliriz; ödemeyi eşyalarınız aracımıza yüklenmeden önce nakit veya banka havalesi ile
kapıda yaparız. Avcılar, Beylikdüzü, Başakşehir, Büyükçekmece, Küçükçekmece, Çatalca,
Bahçelievler, Bakırköy, Bağcılar, Kadıköy, Üsküdar, Ümraniye, Kartal, Pendik ve
İstanbul'un tüm ilçelerine aynı gün hizmet veriyoruz.
```

---

## 4) Hizmetler (GBP → Hizmetler bölümü)

- İkinci el mobilya alımı
- Koltuk takımı ve L koltuk alımı
- Yatak odası takımı ve gardırop alımı
- Beyaz eşya alımı (buzdolabı, çamaşır, bulaşık makinesi)
- Televizyon ve elektronik eşya alımı
- Yemek masası ve sandalye takımı alımı
- Ofis ve büro mobilyası alımı
- Ücretsiz yerinde fiyat teklifi
- Aynı gün adresten alma ve nakliye

---

## 5) Hizmet bölgesi

GBP en fazla **20** bölge kabul eder; site 40 bölgeyi kapsıyor (tamamı sayfalarda ve
`areaServed` alanında var). Öncelik sırası (merkeze en yakın ve ticari olarak en güçlü):

```
Esenyurt, Avcılar, Beylikdüzü, Başakşehir, Küçükçekmece, Büyükçekmece, Bahçelievler,
Bağcılar, Bakırköy, Güngören, Esenler, Bayrampaşa, Gaziosmanpaşa, Sultangazi, Çatalca,
Silivri, Arnavutköy, Zeytinburnu, Şişli, Fatih
```

Kalan 20 ilçe (Kadıköy, Üsküdar, Ataşehir, Maltepe, Kartal, Pendik, Ümraniye, Beykoz,
Çekmeköy, Sancaktepe, Sultanbeyli, Tuzla, Şile, Adalar, Kağıthane, Beşiktaş, Beyoğlu,
Eyüpsultan, Sarıyer, Florya) sitedeki sayfalar üzerinden organik aramadan gelir;
GBP'de açıklama metninde "İstanbul'un tüm ilçeleri" ifadesiyle kapsanır.

---

## 6) Öznitelikler

Güvenle seçilebilecekler: `Nakit kabul edilir`, `Yerinde hizmet` / `Adrese teslim`,
`Ücretsiz tahmini fiyat`. Var olan ve doğru olan diğer öznitelikleri de işaretleyin
(ör. `Otopark`). **Yanlış öznitelik seçmeyin** — doğrulanamayan öznitelik güveni düşürür.

---

## 7) İlk 5 gönderi (GBP → Gönderiler; haftada 1 tane yeterli)

1. **Teklif** — "Eşyalarınızı yeniliyor musunuz? Koltuk takımı, yatak odası ve beyaz
   eşyanız için WhatsApp'tan fotoğraf gönderin, dakikalar içinde fiyat verelim."
   (CTA: WhatsApp / Ara)
2. **Hizmet bölgesi** — "Bahçelievler ve Bakırköy'de bugün alım yapıyoruz. Kendi
   aracımızla geliyor, ödemeyi kapıda nakit yapıyoruz."
3. **Nasıl çalışır** — "1) Fotoğraf gönderin 2) Fiyatı öğrenin 3) Aynı gün gelip
   alalım. Taşıma ve yükleme bizden."
4. **Beyaz eşya** — "Buzdolabı, çamaşır makinesi ve bulaşık makineniz için çalışır
   durumda olması yeterli; ikinci el beyaz eşya alımı yapıyoruz."
5. **Ofis taşınması** — "Ofis mobilyalarınızı komple alıyoruz; kurumsal tahliye ve
   taşınma dönemlerinde aynı gün ekip yönlendiriyoruz."

---

## 8) Soru-Cevap (GBP → Sorular; kendiniz ekleyip yanıtlayabilirsiniz)

1. *İkinci el eşyamı nasıl satabilirim?* — WhatsApp'tan eşyalarınızın fotoğrafını
   gönderin, dakikalar içinde ücretsiz fiyat teklifi alın.
2. *Aynı gün alım yapıyor musunuz?* — Evet, İstanbul genelinde aynı gün adresinize
   gelerek alım yapıyoruz.
3. *Ödeme nasıl ve ne zaman yapılıyor?* — Ödeme, eşyalarınız yüklenmeden önce
   adresinizde anında nakit veya banka havalesi ile yapılır.
4. *Hangi eşyaları alıyorsunuz?* — Koltuk takımı, yatak odası, yemek masası, gardırop,
   beyaz eşya, televizyon ve ofis mobilyaları.
5. *Taşıma ücreti alıyor musunuz?* — Alım yaptığımız eşyalar için nakliye bize aittir.

---

## 9) Yorum isteme mesajı (WhatsApp/SMS şablonu)

```
Merhaba [isim], Medine Mobilya'yı tercih ettiğiniz için teşekkür ederiz.
Hizmetimizi birkaç kelimeyle değerlendirir misiniz? Aşağıdaki bağlantıdan
30 saniyede yorum bırakabilirsiniz:
[GBP yorum bağlantısı]
```

Hedef: ilk 3 ayda 20+ yorum ve 4.5+ ortalama. Her yorumu yanıtlayın (olumluya kısa
teşekkür, olumsuza çözüm önerisi).

---

## 10) Fotoğraf planı (10 kare yeterli, hepsi gerçek olmalı)

1. Dükkân dış cephe (tabela okunur şekilde) 2. İç mekân / teşhir 3. Ekip ve araç
4. Koltuk takımı yükleme anı 5. Yatak odası alımı 6. Beyaz eşya taşıma 7. Ofis
mobilyası tahliyesi 8. Kapıda ödeme anı (eller, nakit) 9. Mağaza vitrini
10. Ekip + müşteri (izin alarak)

> Google, fotoğraflı profillerin tıklanma oranının belirgin şekilde yüksek olduğunu
> bildiriyor; fotoğrafları ayda birkaç kez yenilemek profili canlı tutar.

---

## Kontrol listesi

- [ ] Profil doğrulandı (posta kartı / video)
- [ ] Kategori: birincil + 2 ek kategori
- [ ] Açıklama yapıştırıldı (704 karakter)
- [ ] 9 hizmet eklendi
- [ ] 20 hizmet bölgesi seçildi
- [ ] Çalışma saatleri 08:00–22:00
- [ ] Telefon ve web sitesi siteyle birebir aynı
- [ ] 10 fotoğraf yüklendi
- [ ] İlk gönderi yayınlandı
- [ ] 5 soru-cevap eklendi
