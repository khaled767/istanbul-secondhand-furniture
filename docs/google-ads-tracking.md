# قياس الإعلانات والعملاء — Medine Mobilya

الموقع الآن يرصد ما يهم فعلًا: **المحادثة والاتصال**، لا مجرد الزيارة. هذا الملف يشرح ما
يُرسَل، وما يتبقّى لك في لوحة Google Ads، وكيف تُبنى الحملات لتجلب بائعين لا مشترين.

---

## ١) ما يُرسَل من الموقع الآن (tracking.js)

| الحدث | متى يُرسَل | لماذا |
| --- | --- | --- |
| `whatsapp_click` | أي نقرة على رابط واتساب في أي صفحة | هذا هو التحويل الحقيقي: العميل بدأ محادثة |
| `call_click` | أي نقرة على رابط اتصال (`tel:`) | جزء من العملاء يفضّل الاتصال |
| `engaged` | بقاء 45 ثانية + تمرير 50% | إشارة ناعمة لبناء جمهور إعادة الاستهداف |

وأيضًا يُحفَظ مصدر الزيارة (`gclid` أو `utm_*`) لمدة 90 يومًا (أول لمسة تفوز)، وتُضاف
سطر مرجعي إلى نص رسالة الواتساب، فيصل إليك في المحادثة من أين جاء العميل:

```
Merhaba, Esenyurt bölgesinde ikinci el eşya satmak istiyorum
(Ref: google / cpc / esenyurt-koltuk / ikinci el esya alanlar / gclid:Cj0KCQ...)
```

هذا هو البديل العملي عن نظام CRM: كل محادثة تحمل مصدرها معها.

---

## ٢) ثلاث نقرات في Google Ads لتشغيل التحويلات

1. Ads → **Tools → Conversions → + New conversion action → Website**.
   - الاسم: `WhatsApp Lead` — الفئة: Contact — القيمة: (اتركها «استخدم القيمة نفسها» = 1،
     أو ضع متوسط قيمة الشراء إن أردت حساب ROAS) — العدّ: «Every» لكل تحويل.
   - الطريقة: **Google tag** (لا نستخدم Tag Manager) → سيعطيك سطرًا مثل
     `AW-609406158/AbC-D_efGh`.
2. أعد نفس الخطوة مرتين: `Call Lead` و(اختياري) `Engaged Visitor`.
3. افتح `tracking.js` في المستودع وضع القيم في القسم العلوي:

```js
var CONV = {
  whatsapp_click: "AW-609406158/AbC-D_efGh",  // من خطوة 1
  call_click:     "AW-609406158/XyZ-9_abcd",
  engaged:        ""
};
```

ثم ادفع التغيير (GitHub → Netlify ينشر تلقائيًا). بعد ذلك:
- في كل حملة اختر المزايدة: **Maximize conversions** (يكفي ~15–20 تحويلًا شهريًا لعمل جيد).
- إن كانت التحويلات قليلة: ابدأ بـ **Maximize clicks** مع حدّ سعر نقرة، واجمع بيانات أسبوعين.

> ملاحظة مهمة: لا تُشغّل Maksimize conversions قبل وصول التحويلات فعليًا؛ وإلا سيتعلّم
> النظام من لا شيء.

---

## ٣) بناء الحملات: نية **البائع** لا المشتري

أنت **تشتري** الأثاث المستعمل. إذًا الكلمات التي تبحث عنها عميل جاهز هي عبارات البيع:

مقترح — حملة «İkinci El Eşya Alanlar» (الجهة الأوروبية) ومجموعة مقابلها للآسيوية:

```
ikinci el eşya alanlar
ikinci el eşya alan yerler
ikinci el eşya alım satım
mobilya alanlar
ikinci el koltuk takımı alanlar
beyaz eşya alanlar
ikinci el beyaz eşya alan yerler
eşya alan spotçu
ikinci el eşya satmak istiyorum
koltuk takımımı satmak istiyorum
<منطقة> ikinci el eşya alanlar      ← 40 منطقة، كل واحدة مجموعة أو كلمة منفصلة
```

**كلمات سلبية إلزامية** (وإلا أحرقت ميزانيتك على من يريد الشراء منك أو يبحث عن عمل):

```
satılık   ucuz   bedava   ücretsiz   iş ilanı   işe alım   eleman   mağaza
ikinci el eşya satan yerler   ikinci el koltuk satın al   spot ürün satın al
hurda   çöp   bağış   ikinci el eşya fiyatları nedir      (استعلام معلوماتي)
```

**الإضافات (Assets)** — كلها متاحة ولا تكلف شيئًا:
- إضافة مكالمة + رقم الموقع ⇒ زر اتصال مباشر في الإعلان.
- إضافة الموقع (الفرع في إسن يورت) ⇒ ظهور على الخريطة.
- روابط فرعية: صفحتا منطقة الفرع + «Bölgeler» + «Nasıl çalışır» (عند إنشائها).
- مقتطفات خدمات: `Koltuk takımı`, `Yatak odası`, `Beyaz eşya`, `Ofis mobilyası`.
- ملاحظات: `Aynı gün alım`, `Kapıda nakit ödeme`, `Ücretsiz fiyat teklifi`, `Kendi nakliyemiz`.

**صفحة الهبوط**: لكل مجموعة جغرافية وجّه الإعلان إلى صفحة تلك المنطقة
(مثال: مجموعة Esenyurt → `/esenyurt-ikinci-el-esya-alim-satim`). لديك 40 صفحة جاهزة،
وهذا يرفع نقاط الجودة ويخفض تكلفة النقرة مقابل توجيه الكل للرئيسية.

**الاستهداف الجغرافي**: اختر المناطق التي تخدمها فعليًا (المستودع في إسن يورت)،
وخيار «Presence: people in your targeted locations» — لا «interest» فقط.

---

## ٤) وسم UTM الموحّد

في كل رابط إعلان استخدم:

```
?utm_source=google&utm_medium=cpc&utm_campaign={campaignid}&utm_term={keyword}&utm_content={adgroupid}
```

مع تعبئة القيم الديناميكية من Ads (ValueTrack). سبب ذلك: حتى لو تأخّرت تحويلات Ads،
تصل إليك المحادثة في واتساب وعليها السطر المرجعي، فتعرف الكلمة الفائزة.

---

## ٥) Google Business Profile — العامل المحلي الأول

الملف الجاهز في `docs/google-business-profile.md`. لا تظهر في «İkinci el eşya alanlar
Esenyurt» داخل الخريطة بدونه، والمكالمات من الخريطة أرخص من أي إعلان. اطلب تقييمًا من كل
عميل بعد الاستلام (القالب موجود في الملف) — 20 تقييمًا في 3 أشهر تغيّر ترتيبك.

---

## ٦) روتين أسبوعي (10 دقائق)

- Ads → Campaigns: تكلفة كل تحويل (Cost/conv.) لكل مجموعة — أوقف أي كلمة تكلّف أكثر من
  سعر شرائك المستهدف دون تحويل.
- Ads → Search terms: أضف الكلمات السيئة إلى السلبية (يبدأ النمو من هنا عادة).
- WhatsApp: هل الرسائل تحمل Ref؟ راجع أي حملة تنتج محادثات بلا بيع (اضبط الاستهداف).
- GSC → Pages: راقب نمو المفهرس (9 اليوم) و«Page with redirect» وهي طبيعية.
- GBP → أضف منشورًا جديدًا وصورة جديدة.

---

## الحالة الحالية (قبل التعديل)

- كان الموقع يرصد **صفر أحداث تحويل**، أي أن كل ميزانية الإعلانات حتى اليوم أُنفقت بلا
  قياس. بعد هذا التعديل: 3 أحداث + إسناد كامل للمصدر.
- المتبقي عليك: أخذ معرّفات التحويل من Ads ولصقها في `CONV` (خطوة ٢)، وإنشاء ملف
  Google Business Profile وتوثيقه.
