import { NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

// Polyfill URL.canParse for older Node.js versions (e.g. Node 18 or older)
if (typeof URL.canParse !== 'function') {
  (URL as any).canParse = function (url: string | URL, base?: string | URL) {
    try {
      new URL(url, base);
      return true;
    } catch {
      return false;
    }
  };
}
const LOCAL_DICTIONARY: Record<string, string> = {
  // Urdu Script to English
  "نکاح": "nikah marriage",
  "شادی": "shadi marriage",
  "عمر": "age",
  "عمریں": "ages",
  "قانونی": "legal statutory",
  "قانون": "law legal legislation",
  "طلاق": "talaq divorce",
  "خلع": "khula dissolution of marriage",
  "بچے": "children child minor",
  "بچوں": "children child minor",
  "بچہ": "children child minor",
  "نابالغ": "minor juvenile",
  "خرچہ": "maintenance expenses allowance",
  "نان": "maintenance",
  "نفقہ": "maintenance",
  "حق": "right dower",
  "مهر": "dower haq mehr",
  "مہر": "dower haq mehr",
  "حراست": "custody",
  "تحویل": "custody",
  "سرپرستی": "guardianship guardian",
  "سرپرست": "guardianship guardian",
  "عدالت": "court",
  "عدالتی": "court judicial",
  "ایف": "fir",
  "آئی": "fir",
  "آر": "fir",
  "پولیس": "police",
  "گرفتار": "arrest arrested",
  "گرفتاری": "arrest arrested",
  "ضمانت": "bail security",
  "قتل": "murder qatl homicide",
  "چوری": "theft stolen",
  "فراڈ": "fraud cheat cheating",
  "دھمکی": "threat intimidate intimidation",
  "سزا": "punishment penalty sentence",
  "جرم": "offense crime criminal",
  "سارق": "theft",
  "قبضہ": "possession qabza encroachment illegal possession",
  "زمین": "land property plot",
  "پلاٹ": "land property plot",
  "پراپرٹی": "property",
  "جائیداد": "property land",
  "رجسٹری": "registry deed",
  "انتقال": "mutation intiqal transfer",
  "وراثت": "inheritance wirasat",
  "وارث": "heir inheritor inheritance",
  "معاہدہ": "agreement contract",
  "معاہدے": "agreement contract",
  "قرض": "debt loan money",
  "ہرجانہ": "damages compensation",
  "نوکری": "job employment employee work",
  "ملازمت": "job employment employee work",
  "ملازم": "employee worker",
  "تنخواہ": "salary wages payment",
  "مالک": "owner landlord employer",
  "کرایہ": "rent kiraya",
  "کرایہ دار": "tenant",
  "ٹیکس": "tax fbr",
  "گوشوارہ": "tax return filing",
  "صارف": "consumer",
  "وارنٹی": "warranty",
  "خریداری": "shopping purchase consumer",
  "رسید": "receipt invoice",
  "بل": "bill invoice",
  "نقصان": "damage loss damages",
  
  // Roman Urdu to English
  "nikah": "nikah marriage",
  "nikaah": "nikah marriage",
  "shadi": "shadi marriage",
  "shaadi": "shadi marriage",
  "umar": "age",
  "umr": "age",
  "qanooni": "legal statutory",
  "kanooni": "legal statutory",
  "qanoon": "law legal legislation",
  "kanoon": "law legal legislation",
  "talaq": "talaq divorce",
  "talaaq": "talaq divorce",
  "khula": "khula dissolution of marriage",
  "kula": "khula dissolution of marriage",
  "bache": "children child minor",
  "bachay": "children child minor",
  "bachon": "children child minor",
  "bacha": "children child minor",
  "nabaligh": "minor juvenile",
  "kharcha": "maintenance expenses allowance",
  "kharja": "maintenance expenses allowance",
  "nafaqa": "maintenance",
  "mehr": "dower haq mehr",
  "dower": "dower haq mehr",
  "custody": "custody",
  "guardianship": "guardianship guardian",
  "guardian": "guardianship guardian",
  "adalat": "court",
  "fir": "fir",
  "police": "police",
  "giraftar": "arrest arrested",
  "giraftari": "arrest arrested",
  "zamanat": "bail security",
  "qatl": "murder qatl homicide",
  "chori": "theft stolen",
  "fraud": "fraud cheat cheating",
  "dhamki": "threat intimidate intimidation",
  "saza": "punishment penalty sentence",
  "jurm": "offense crime criminal",
  "qabza": "possession qabza encroachment illegal possession",
  "kabza": "possession qabza encroachment illegal possession",
  "zameen": "land property plot",
  "zamin": "land property plot",
  "plot": "land property plot",
  "property": "property",
  "registry": "registry deed",
  "intiqal": "mutation intiqal transfer",
  "wirasat": "inheritance",
  "virasat": "inheritance",
  "contract": "agreement contract",
  "agreement": "agreement contract",
  "qarz": "debt loan money",
  "harjana": "damages compensation",
  "naukri": "job employment employee work",
  "mulazmat": "job employment employee work",
  "tankhwa": "salary wages payment",
  "salary": "salary wages payment",
  "owner": "owner landlord employer",
  "employer": "owner landlord employer",
  "malik": "owner landlord employer",
  "kiraya": "rent",
  "kirayedar": "tenant",
  "tax": "tax fbr",
  "consumer": "consumer",
  "warranty": "warranty",
  "receipt": "receipt invoice",
  "raseed": "receipt invoice",
  "bill": "bill invoice"
};

const LOCAL_RECORD_TRANSLATIONS: Record<string, Record<string, string>> = {
  "Travel Consent & International Relocation of Minors": {
    "ur": `**Category (زمرہ)**: Family Laws

**Title**: بچوں کی بیرون ملک منتقلی اور سفری اجازت نامہ

**1. Direct Answer**:
کوئی بھی والدین جن کے پاس بچوں کی جسمانی تحویل (custody) ہو، وہ دوسرے والدین (جو قدرتی سرپرست ہیں) کی تحریری رضامندی یا گارڈین کورٹ کی اجازت کے بغیر بچوں کو مستقل طور پر بیرون ملک نہیں لے جا سکتے۔

**2. Relevant Pakistani Law**:
گارڈینز اینڈ وارڈز ایکٹ 1890 کے سیکشن 25 کے تحت، دوسرے والدین کی اجازت کے بغیر بچوں کو منتقل کرنا قانونی تحویل سے بچوں کو محروم کرنا تصور کیا جاتا ہے۔ اگر کوئی والدین غیر قانونی طور پر بچوں کو بیرون ملک لے جانے کی کوشش کریں تو دوسرے والدین ان کا نام ایگزٹ کنٹرول لسٹ (ECL) پر ڈلوانے کے لیے درخواست دائر کر سکتے۔ (Source: Section 25 of the Guardians and Wards Act, 1890)

**3. Practical Next Steps**:
1. بچوں کو بیرون ملک لے جانے سے پہلے دوسرے والدین سے تحریری سفری اجازت نامہ (Travel Consent) حاصل کریں۔
2. اگر دوسرا فریق انکار کرے تو مناسب وجوہات کے ساتھ گارڈین کورٹ سے رجوع کر کے اجازت حاصل کریں۔
3. غیر قانونی منتقلی کی صورت میں سیکیورٹی اداروں کو مطلع کریں اور نام ECL میں شامل کروائیں۔

**4. Required Documents**:
دوسرے والدین کا تحریری اجازت نامہ، بچوں کے شناختی دستاویزات (ب فارم/CNIC)، پاسپورٹ، اور عدالت کا حکمنامہ (اگر لاگو ہو)۔

**5. Important Notes**:
رول 7 کے تحت یہ نظام تعلیمی مقاصد کے لیے معلومات فراہم کرتا ہے اور پیشہ ورانہ قانونی مشورے کا متبادل نہیں ہے۔`,
    "roman": `**Category (زمرہ)**: Family Laws

**Title**: Bachon Ki Beroon-e-Mulk Muntaqili aur Travel Consent

**1. Direct Answer**:
Parents mein se jis ke paas bachon ki custody ho, wo doosray parent (natural guardian) ki written consent ya Guardian Court ki permission ke baghair bachon ko beroon-e-mulk nahi le ja sakte.

**2. Relevant Pakistani Law**:
Section 25 Guardians and Wards Act 1890 ke tehat, doosray parent ki marzi ke baghair bachon ko le jana illegal removal mana jata hai. Agar koi parent bachon ko illegal tarike se bahar le jane ki koshish kare, to doosra parent un ka naam Exit Control List (ECL) mein shamil karwane ke liye apply kar sakta hai. (Source: Section 25 of the Guardians and Wards Act, 1890)

**3. Practical Next Steps**:
1. Bachon ko bahar le jane se pehle doosray parent se written Travel Consent Deed sign karwain.
2. Agar doosra parent refuse kare, to proper grounds par Guardian Court se court permission claim karein.
3. Illegal removal par immediately security agencies ko report karein aur ECL list ke liye application dein.

**4. Required Documents**:
Written Consent Deed, CNIC of parents, Children B-Form, Passports, and Guardian Court Order (if applicable).

**5. Important Notes**:
Rule 7 ke tehat yeh system informational purposes ke liye hai aur professional legal advice ka badal nahi hai.`
  },
  "Child Maintenance Obligations (Child Support)": {
    "ur": `**Category (زمرہ)**: Family Laws

**Title**: بچوں کا نان و نفقہ (خرچہ)

**1. Direct Answer**:
پاکستانی قانون کے تحت، والد غیر مشروط طور پر اپنے نابالغ بچوں کے کھانے، کپڑے، تعلیم اور رہائش کا خرچہ اٹھانے کا پابند ہے۔

**2. Relevant Pakistani Law**:
مسلم فیملی لاز آرڈیننس 1961 کے سیکشن 9 کے تحت، بچوں کی تحویل (custody) ماں کے پاس ہونے کے باوجود والد خرچہ دینے کا ذمہ دار ہے۔ والد بیٹوں کا خرچہ 18 سال کی عمر تک اور بیٹیوں کا خرچہ ان کی شادی ہونے تک دینے کا پابند ہے۔ والد کے انکار کی صورت میں، یونین کونسل یا فیملی کورٹ کے ذریعے نان و نفقہ کا دعویٰ دائر کیا جا سکتا ہے۔ (Source: Section 9 of the Muslim Family Laws Ordinance, 1961)

**3. Practical Next Steps**:
1. والد سے خرچے کا مطالبہ کریں، انکار پر مقامی یونین کونسل کے چیئرمین کو درخواست دیں۔
2. اگر یونین کونسل سے مسئلہ حل نہ ہو تو فیملی کورٹ میں خرچے کا دعویٰ دائر کریں۔
3. بقایا جات کی وصولی کے لیے عدالت کے ذریعے والد کے اثاثے یا تنخواہ قرق کروائیں۔

**4. Required Documents**:
بچوں کا پیدائشی سرٹیفکیٹ یا بی فارم، اسکول فیس کی رسیدیں، والد کی آمدنی کا ثبوت، اور دعویٰ کا مسودہ۔

**5. Important Notes**:
رول 7 کے تحت یہ نظام تعلیمی مقاصد کے لیے معلومات فراہم کرتا ہے اور پیشہ ورانہ قانونی مشورے کا متبادل نہیں ہے۔`,
    "roman": `**Category (زمرہ)**: Family Laws

**Title**: Bachon Ka Maintenance (Kharcha)

**1. Direct Answer**:
Pakistani qanoon ke tehat, baap apnay nabaligh bachon ke khane, kapre, taleem aur rehaish ka kharcha uthanay ka unconditionally paband hai.

**2. Relevant Pakistani Law**:
Section 9 MFLO 1961 ke tehat, custody jiske paas bhi ho, baap kharcha dene ka zimmedar hai. Baap beton ko 18 saal ka hone tak aur larkiyon ko shadi hone tak kharcha dene ka paband hai. Agar baap inkar kare to Family Court mein suit file kiya ja sakta hai aur unpaid kharcha court ke zariye recover kiya ja sakta hai. (Source: Section 9 of the Muslim Family Laws Ordinance, 1961)

**3. Practical Next Steps**:
1. Baap se kharcha claim karein, agar inkar ho to Union Council Chairman ko application dein.
2. Resolution na hone par Family Court mein child maintenance recovery suit file karein.
3. Unpaid arrears ke liye baap ki property attach karwane ya salary deduct karwane ke orders lein.

**4. Required Documents**:
Children B-Form/Birth Certificate, School fee slips, proof of father's income, and CNIC copies.

**5. Important Notes**:
Rule 7 ke tehat yeh system informational purposes ke liye hai aur professional legal advice ka badal nahi hai.`
  },
  "Women's Inheritance Rights under Shariah": {
    "ur": `**Category (زمرہ)**: Family Laws

**Title**: شریعت کے تحت خواتین کے وراثت کے حقوق

**1. Direct Answer**:
خواتین شریعت اور پاکستانی قوانین کے تحت وراثت میں اپنے قانونی حصے کی مکمل حقدار ہیں۔

**2. Relevant Pakistani Law**:
کسی خاتون کو طاقت، دھوکے، یا جبر کے ذریعے وراثت کے حق سے محروم کرنا تعزیراتِ پاکستان (PPC) کے سیکشن 498-A کے تحت ایک سنگین جرم ہے، جس کی سزا 5 سے 10 سال تک قید اور 10 لاکھ روپے تک جرمانہ ہے۔ متاثرہ خواتین وراثت کی وصولی کے لیے سول عدالتوں میں تقسیمِ جائیداد (Partition suit) کا دعویٰ دائر کر سکتی ہیں۔ (Source: Section 498-A of the Pakistan Penal Code, 1860)

**3. Practical Next Steps**:
1. پٹواری یا اراضی ریکارڈ سینٹر (ARC) سے متوفی کے نام جائیداد کا شجرہ نسب اور وراثت کی تفصیلات حاصل کریں۔
2. اگر خاندان حصہ دینے سے انکار کرے تو فوری طور پر سول کورٹ میں تقسیمِ جائیداد کا دعویٰ دائر کریں۔
3. کسی بھی قسم کے جبر یا جعل سازی پر مقامی پولیس اسٹیشن میں سیکشن 498-A کے تحت شکایت درج کروائیں۔

**4. Required Documents**:
متوفی کا ڈیتھ سرٹیفکیٹ، وراثت نامہ (Succession certificate)، جائیداد کے مالکانہ کاغذات (فرد/رجسٹری)، اور بی فارم/شناختی کارڈ۔

**5. Important Notes**:
رول 7 کے تحت یہ نظام تعلیمی مقاصد کے لیے معلومات فراہم کرتا ہے اور پیشہ ورانہ قانونی مشورے کا متبادل نہیں ہے۔`,
    "roman": `**Category (زمرہ)**: Family Laws

**Title**: Khwateen Ke Wirasat Ke Huqooq (Under Shariah)

**1. Direct Answer**:
Pakistan ke qanoon aur Shariah ke tehat khwateen apnay legal inheritance share ki mukammal haqdar hain.

**2. Relevant Pakistani Law**:
Kisi aurat ko zor-zabardasti, deceit, ya coercion se wirasat se mehroom karna Section 498-A PPC ke tehat criminal offense hai, jis ki saza 5 se 10 saal tak imprisonment aur 10 lakh rupay tak jurmana ho sakti hai. Khwateen recovery ke liye Civil Court mein suit for partition file kar sakti hain. (Source: Section 498-A of the Pakistan Penal Code, 1860)

**3. Practical Next Steps**:
1. Arazi Record Center (ARC) ya Patwari se deceased person ki land registry aur Mutation (Intiqal) records nikaluwain.
2. Family members share dene se inkar karein to Civil Court mein partition suit file karein.
3. Coercion ya fraud hone par local police station mein Section 498-A ke tehat FIR register karwain.

**4. Required Documents**:
Death certificate of deceased, inheritance certificate (Wirasatnama), property registry/Fard, and CNIC copies.

**5. Important Notes**:
Rule 7 ke tehat yeh system informational purposes ke liye hai aur professional legal advice ka badal nahi hai.`
  },
  "Iddat Period Rules and Rights": {
    "ur": `**Category (زمرہ)**: Family Laws

**Title**: عدت کی مدت کے قوانین اور حقوق

**1. Direct Answer**:
عدت ایک لازمی انتظار کی مدت ہے جو ایک مسلمان عورت کو طلاق یا شوہر کی موت کے بعد گزارنا ہوتی ہے۔

**2. Relevant Pakistani Law**:
طلاق کی صورت میں عدت کی مدت یونین کونسل کو طلاق کا نوٹس موصول ہونے سے 90 دن (یا حمل کی صورت میں بچے کی پیدائش تک) ہے۔ شوہر کی موت کی صورت میں یہ مدت 4 ماہ اور 10 دن ہے۔ عدت کے دوران شوہر بیوی کو رہائش اور نان و نفقہ فراہم کرنے کا پابند ہے۔ (Source: Section 7 of the Muslim Family Laws Ordinance, 1961)

**3. Practical Next Steps**:
1. طلاق کی صورت میں نوٹس یونین کونسل میں جمع ہونے کی تاریخ نوٹ کریں کیونکہ عدت کا آغاز وہیں سے ہوتا ہے۔
2. عدت کی مدت کے دوران شوہر سے رہائش اور نان و نفقہ (خرچہ) کا مطالبہ کریں۔
3. اگر شوہر خرچہ نہ دے تو فیملی کورٹ میں عدت کے خرچے کا دعویٰ دائر کریں۔

**4. Required Documents**:
طلاق کا نوٹس، نکاح نامہ، شوہر کا ڈیتھ سرٹیفکیٹ (موت کی صورت میں)، اور بچوں کی تفصیلات (اگر حاملہ ہو)۔

**5. Important Notes**:
رول 7 کے تحت یہ نظام تعلیمی مقاصد کے لیے معلومات فراہم کرتا ہے اور پیشہ ورانہ قانونی مشورے کا متبادل نہیں ہے۔`,
    "roman": `**Category (زمرہ)**: Family Laws

**Title**: Iddat Period Ke Rules aur Huqooq

**1. Direct Answer**:
Iddat ek mandatory waiting period hai jo Muslim aurat ko divorce ya shohar ki death ke baad observe karna hota hai.

**2. Relevant Pakistani Law**:
Divorce ke baad iddat 90 days (ya pregnancy mein bachay ki delivery tak) hoti hai, jo Union Council ko notice milne se shuru hoti hai. Shohar ki death par iddat 4 months aur 10 days hai. Iddat ke dauran shohar rehaish aur kharcha (maintenance) dene ka paband hai. (Source: Section 7 of the Muslim Family Laws Ordinance, 1961)

**3. Practical Next Steps**:
1. Divorce notice Union Council mein receive hone ki exact date verify karein, kyunki iddat wahan se start hoti hai.
2. Iddat period ke dauran shohar se rehaish (housing) aur maintenance claim karein.
3. Shohar ke inkar par Family Court mein suit for maintenance during iddat file karein.

**4. Required Documents**:
Divorce notice, Nikahnama, Death Certificate (in case of husband's demise), and pregnancy proof (if applicable).

**5. Important Notes**:
Rule 7 ke tehat yeh system informational purposes ke liye hai aur professional legal advice ka badal nahi hai.`
  },
  "Parental Visitation Rights & Schedules": {
    "ur": `**Category (زمرہ)**: Family Laws

**Title**: بچوں سے ملاقات کے حقوق اور شیڈول

**1. Direct Answer**:
بچوں کی تحویل نہ رکھنے والے والدین (عام طور پر والد) کو اپنے بچوں سے ملنے کا مکمل قانونی حق حاصل ہے۔

**2. Relevant Pakistani Law**:
بچوں کی تحویل نہ رکھنے والے والدین گارڈینز اینڈ وارڈز ایکٹ 1890 کے سیکشن 12 کے تحت گارڈین کورٹ میں ملاقات کے حقوق (Visitation rights) کے لیے درخواست دائر کر سکتے ہیں۔ عدالت ملاقات کا تفصیلی شیڈول (مثلاً عدالتی احاطے میں ملاقات، اختتام ہفتہ پر گھر لے جانے کی اجازت، یا تعطیلات کی عارضی تحویل) طے کرتی ہے۔ (Source: Section 12 of the Guardians and Wards Act, 1890)

**3. Practical Next Steps**:
1. دوسرے فریق سے پرامن ملاقات کی کوشش کریں، اگر وہ بچوں سے ملنے نہ دے تو وکیل سے رجوع کریں۔
2. گارڈین کورٹ میں ملاقات کے حقوق (Visitation application) کی درخواست دائر کریں۔
3. عدالتی حکم نامے کی کاپی حاصل کر کے طے شدہ شیڈول کے مطابق ملاقاتیں کریں۔ اگر حکم نامے کی خلاف ورزی ہو تو عدالت میں توہینِ عدالت کی کارروائی دائر کریں۔

**4. Required Documents**:
بچوں کے پیدائشی سرٹیفکیٹ/بی فارم کی کاپی، نکاح نامہ/طلاق نامہ، اور ملاقات کی درخواست کا مسودہ۔

**5. Important Notes**:
رول 7 کے تحت یہ نظام تعلیمی مقاصد کے لیے معلومات فراہم کرتا ہے اور پیشہ ورانہ قانونی مشورے کا متبادل نہیں ہے۔`,
    "roman": `**Category (زمرہ)**: Family Laws

**Title**: Bachon Se Mulaqat Ke Huqooq (Visitation)

**1. Direct Answer**:
Non-custodial parent (amuman baap) ko apnay bachon se mulaqat ka mukammal legal right ha.

**2. Relevant Pakistani Law**:
Non-custodial parent Section 12 Guardians and Wards Act 1890 ke tehat Guardian Court mein visitation application file kar sakte hain. Court visitation schedule (court premises mein, weekend stay ya vacations/eid par custody) tay karti hai. (Source: Section 12 of the Guardians and Wards Act, 1890)

**3. Practical Next Steps**:
1. Agar doosray parent bachon se na milne dein, to immediately legal advocate se consult karein.
2. Guardian Court mein visitation rights suite file karein taake interim meetings setup ho sakein.
3. Court order pass hone ke baad, visitation schedule enforce karwain. Violation par court fine ya custody change ho sakti hai.

**4. Required Documents**:
Children B-Form, Nikahnama/Divorce deeds, and visitation application draft.

**5. Important Notes**:
Rule 7 ke tehat yeh system informational purposes ke liye hai aur professional legal advice ka badal nahi hai.`
  },
  "Nikah Nama Contract Clauses & column rights": {
    "ur": `**Category (زمرہ)**: Family Laws

**Title**: نکاح نامہ کی شرائط اور کالمز کے حقوق

**1. Direct Answer**:
نکاح نامہ اسلام میں ایک قانونی اور مذہبی معاہدہ ہے۔ اس کے تمام کالمز کو پر کرنا دلہن کے قانونی حقوق کے تحفظ کے لیے انتہائی ضروری ہے۔

**2. Relevant Pakistani Law**:
کالم 18 (طلاقِ تفویض - بیوی کا طلاق کا حق)، کالم 19 (شوہر کی دوسری شادی پر پابندیاں)، اور کالم 20 (حق مہر کی تفصیلات—معجل مہر جو فوری ادا کرنا ہو، اور مؤجل مہر جو طلاق یا موت پر واجب الادا ہو) انتہائی اہم ہیں۔ ان کالمز کو کاٹنا یا خالی چھوڑنا بیوی کے قانونی حقوق کو غصب کرتا ہے۔ (Source: Section 5 of the Muslim Family Laws Ordinance, 1961)

**3. Practical Next Steps**:
1. شادی کی تقریب سے پہلے نکاح نامہ کی شرائط پر دونوں خاندانوں میں واضح گفتگو کریں۔
2. نکاح نامہ کے کالم 18، 19 اور 20 کو قلم زد (cross) کرنے کے بجائے واضح طور پر پر کریں۔
3. رجسٹریشن کے بعد یونین کونسل سے نکاح نامہ کی تصدیق شدہ کاپی حاصل کر کے محفوظ رکھیں۔

**4. Required Documents**:
دلہا دلہن کے قومی شناختی کارڈ (CNIC) اور رجسٹریشن کے لیے نکاح نامہ کے پرت۔

**5. Important Notes**:
رول 7 کے تحت یہ نظام تعلیمی مقاصد کے لیے معلومات فراہم کرتا ہے اور پیشہ ورانہ قانونی مشورے کا متبادل نہیں ہے۔`,
    "roman": `**Category (زمرہ)**: Family Laws

**Title**: Nikahnama Ke Columns aur Huqooq

**1. Direct Answer**:
Nikahnama Islam mein ek legally binding marriage contract hai. Is ke columns ko sahi tarike se fill karna dulhan ke legal rights ke liye zaroori hai.

**2. Relevant Pakistani Law**:
Column 18 (wife ka delegated right of divorce/Talaq-e-Tafweez), Column 19 (restrictions on second marriage), aur Column 20 (dower details—Prompt Mehr payable immediately, Deferred Mehr payable at divorce/death) main columns hain. In columns ko cross karna ya blank chhorna dulhan ke rights ko restrict karta hai. (Source: Section 5 of the Muslim Family Laws Ordinance, 1961)

**3. Practical Next Steps**:
1. Nikah se pehle dono families in columns ki conditions par mutual agreement karein.
2. Ensure karein ke Nikah Khwan in columns ko bina permission ke blank ya cross na kare.
3. Nikahnama register hone ke baad Union Council se computerized registered copy hasil karein.

**4. Required Documents**:
CNIC of bride and groom, and original Nikahnama copies for registration.

**5. Important Notes**:
Rule 7 ke tehat yeh system informational purposes ke liye hai aur professional legal advice ka badal nahi hai.`
  },
  "Child Custody - Father's Rights & Natural Guardianship": {
    "ur": `**Category (زمرہ)**: Family Laws

**Title**: بچوں کی سرپرستی اور والد کے حقوق

**1. Direct Answer**:
پاکستانی قانون کے تحت والد بچوں کا قدرتی سرپرست (Vilayah) ہے جبکہ والدہ کے پاس بچوں کی جسمانی تحویل (Hizanat) ہوتی ہے۔

**2. Relevant Pakistani Law**:
والد بچوں کی تعلیم، صحت اور مذہبی تربیت کا ذمہ دار ہے۔ گارڈینز اینڈ وارڈز ایکٹ 1890 کے سیکشن 17 کے تحت، والد 7 سال سے بڑے بیٹے اور بلوغت کو پہنچنے والی بیٹی کی تحویل (custody) کے لیے گارڈین کورٹ میں دعویٰ دائر کر سکتا ہے، جہاں عدالت بچے کی فلاح و بہبود کو مدنظر رکھ کر فیصلہ کرتی ہے۔ (Source: Section 17 of the Guardians and Wards Act, 1890)

**3. Practical Next Steps**:
1. اگر والدہ بچوں کی نگہداشت صحیح طریقے سے نہ کر رہی ہو تو والد تحویل کے لیے گارڈین کورٹ سے رجوع کر سکتا ہے۔
2. گارڈین کورٹ میں تحویلِ اطفال (Custody petition) کا دعویٰ دائر کریں۔
3. بچوں کی تعلیم اور پرورش کے اخراجات برداشت کرنے کی اپنی مالی صلاحیت کا ثبوت عدالت میں پیش کریں۔

**4. Required Documents**:
بچوں کے شناختی دستاویزات (B-Form)، والد کا شناختی کارڈ، مالی استحکام کے ثبوت (بینک سٹیٹمنٹ/آمدنی کا ثبوت)، اور دعویٰ کا مسودہ۔

**5. Important Notes**:
رول 7 کے تحت یہ نظام تعلیمی مقاصد کے لیے معلومات فراہم کرتا ہے اور پیشہ ورانہ قانونی مشورے کا متبادل نہیں ہے۔`,
    "roman": `**Category (زمرہ)**: Family Laws

**Title**: Child Custody aur Baap Ke Huqooq

**1. Direct Answer**:
Pakistani qanoon ke tehat baap natural legal guardian (Vilayah) hai, jabke maa ke paas physical custody (Hizanat) hoti hai.

**2. Relevant Pakistani Law**:
Baap bachon ki education, healthcare aur welfare ka zimmedar hai. Section 17 Guardians and Wards Act 1890 ke tehat, baap 7 saal se baray larkay aur puberty tak pohnchnay wali larki ki physical custody claim karne ke liye Guardian Court mein case file kar sakta hai, bashart-e-ke wo prove kare ke custody transfer bachay ki welfare mein hai. (Source: Section 17 of the Guardians and Wards Act, 1890)

**3. Practical Next Steps**:
1. Agar mother negligent ho ya doosri shadi kar le, to father custody ke liye consult karein.
2. Guardian Court mein child custody petition file karein.
3. Court mein proof pesh karein ke aap financial aur environmental tor par bachon ki behtar parvarish kar sakte hain.

**4. Required Documents**:
CNIC of father, Children B-Form, school progress reports, financial proofs, and custody suit draft.

**5. Important Notes**:
Rule 7 ke tehat yeh system informational purposes ke liye hai aur professional legal advice ka badal nahi hai.`
  },
  "Spousal Maintenance Claims (Wife's Nafqah)": {
    "ur": `**Category (زمرہ)**: Family Laws

**Title**: بیوی کا نان و نفقہ (خرچہ)

**1. Direct Answer**:
شوہر قانونی طور پر اپنی بیوی کو مناسب نان و نفقہ (کھانا، کپڑے، رہائش اور طبی سہولیات) فراہم کرنے کا پابند ہے۔

**2. Relevant Pakistani Law**:
مسلم فیملی لاز آرڈیننس 1961 کے سیکشن 9 کے تحت، اگر شوہر خرچہ دینے سے انکار کرے تو بیوی یونین کونسل کے چیئرمین کو درخواست دے کر ثالثی کونسل کے ذریعے خرچے کا سرٹیفکیٹ حاصل کر سکتی ہے، یا فیملی کورٹ میں نان و نفقہ کا دعویٰ دائر کر سکتی ہے۔ گزشتہ 3 سال تک کا بقایا خرچہ بھی وصول کیا جا سکتا ہے۔ (Source: Section 9 of the Muslim Family Laws Ordinance, 1961)

**3. Practical Next Steps**:
1. شوہر سے اخراجات کا مطالبہ کریں، انکار پر اپنے علاقے کے یونین کونسل کے چیئرمین کو درخواست دیں۔
2. اگر ثالثی کونسل کے ذریعے مسئلہ حل نہ ہو تو فیملی کورٹ میں خرچے کا دعویٰ دائر کریں۔
3. بقایا جات کی وصولی کے لیے شوہر کی تنخواہ یا اثاثوں کو ضبط کرنے کے لیے عدالتی احکامات حاصل کریں۔

**4. Required Documents**:
نکاح نامہ کی کاپی، اپنا قومی شناختی کارڈ، شوہر کی آمدنی کا ثبوت، اور اخراجات کا تخمینہ۔

**5. Important Notes**:
رول 7 کے تحت یہ نظام تعلیمی مقاصد کے لیے معلومات فراہم کرتا ہے اور پیشہ ورانہ قانونی مشورے کا متبادل نہیں ہے۔`,
    "roman": `**Category (زمرہ)**: Family Laws

**Title**: Biwi Ka Kharcha (Spousal Maintenance)

**1. Direct Answer**:
Shohar legally apni biwi ko munasib kharcha (Nafqah), khana, kapre, rehaish aur medical treatment dene ka paband hai.

**2. Relevant Pakistani Law**:
Section 9 MFLO 1961 ke tehat, agar shohar maintenance na de to biwi Union Council Chairman ko application de kar Arbitration Council ke zariye maintenance certificate le sakti hai, ya Family Court mein suit file kar sakti hai. Past maintenance (arrears) 3 saal tak ka recover kiya ja sakta hai. (Source: Section 9 of the Muslim Family Laws Ordinance, 1961)

**3. Practical Next Steps**:
1. Shohar se maintenance demand karein, agar inkar kare to local Union Council mein application dein.
2. Resolution na hone par Family Court mein recovery of spousal maintenance suit file karein.
3. Court ke execution phase mein shohar ke assets attach karwa kar arrears recover karein.

**4. Required Documents**:
Nikahnama copy, CNIC of wife, proof of husband's employment/salary, and monthly expense list.

**5. Important Notes**:
Rule 7 ke tehat yeh system informational purposes ke liye hai aur professional legal advice ka badal nahi hai.`
  },
  "Child Custody (Hizanat) - Mother's Primary Rights": {
    "ur": `**Category (زمرہ)**: Family Laws

**Title**: بچوں کی کسٹڈی (حضانت) اور ماں کا حق

**1. Direct Answer**:
بچوں کی تحویل (Hizanat) کا فیصلہ کرتے وقت فیملی کورٹ ہمیشہ بچے کی فلاح و بہبود اور بہترین مفاد کو ترجیح دیتی ہے۔

**2. Relevant Pakistani Law**:
گارڈینز اینڈ وارڈز ایکٹ 1890 کے سیکشن 17 کے تحت، ماں کو نابالغ بیٹے کی 7 سال کی عمر تک اور نابالغ بیٹی کی بلوغت تک تحویل حاصل کرنے کا بنیادی حق حاصل ہے۔ تاہم، اگر ماں بچوں کی دیکھ بھال میں غفلت برتے، بدچلنی ثابت ہو، یا وہ کسی غیر محرم سے دوسری شادی کر لے تو وہ یہ حق کھو سکتی ہے۔ (Source: Section 17 of the Guardians and Wards Act, 1890)

**3. Practical Next Steps**:
1. طلاق یا علیحدگی کی صورت میں بچوں کو اپنے پاس رکھیں، کیونکہ ماں کے پاس حضانت کا بنیادی حق ہوتا ہے۔
2. اگر والد بچوں کو زبردستی چھیننے کی کوشش کرے تو فوری طور پر فیملی کورٹ میں حضانتِ اطفال (Custody petition) کا دعویٰ دائر کریں۔
3. بچوں کے بہترین مفاد اور ان کی اچھی پرورش کے ثبوت عدالت میں پیش کریں۔

**4. Required Documents**:
بچوں کے پیدائشی سرٹیفکیٹ/بی فارم، نکاح نامہ/طلاق نامہ، اپنی آمدنی کے ثبوت (اگر کوئی ہوں)، اور وکیل کا مسودہ۔

**5. Important Notes**:
رول 7 کے تحت یہ نظام تعلیمی مقاصد کے لیے معلومات فراہم کرتا ہے اور پیشہ ورانہ قانونی مشورے کا متبادل نہیں ہے۔`,
    "roman": `**Category (زمرہ)**: Family Laws

**Title**: Child Custody aur Maa Ke Huqooq (Hizanat)

**1. Direct Answer**:
Child custody (Hizanat) ka faisla hamesha bachay ki welfare aur best interest ke mutabiq tay hota hai.

**2. Relevant Pakistani Law**:
Section 17 Guardians and Wards Act 1890 ke tehat, maa ko larkay ki 7 saal ki age tak aur larki ki puberty tak physical custody (Hizanat) ka primary right hai. Maa doosri shadi kare (ghair-mahram se) ya bachon ki parvarish na kar sake, to custody baap ko transfer ho sakti hai. (Source: Section 17 of the Guardians and Wards Act, 1890)

**3. Practical Next Steps**:
1. Separation ke baad bachon ko apne paas rakhein aur un ki education/well-being ka khyal rakhein.
2. Father ki taraf se forceful custody lene ke threat par Family Court mein custody suit file karein.
3. Prove karein ke bachon ka future aap ke sath secure aur healthy hai.

**4. Required Documents**:
CNIC of mother, Children B-Form, proof of mother's accommodation, and custody suit draft.

**5. Important Notes**:
Rule 7 ke tehat yeh system informational purposes ke liye hai aur professional legal advice ka badal nahi hai.`
  },
  "Legal Age of Marriage (Child Marriage Restraint Act)": {
    "ur": `**Category (زمرہ)**: Family Laws

**Title**: شادی کی قانونی عمر (چائلڈ میرج ریسٹرینٹ ایکٹ)

**1. Direct Answer**:
پاکستان میں شادی کی قانونی عمر چائلڈ میرج ریسٹرینٹ ایکٹ کے تحت طے ہوتی ہے۔

**2. Relevant Pakistani Law**:
چائلڈ میرج ریسٹرینٹ ایکٹ کے تحت پاکستان میں شادی کی کم از کم عمر درج ذیل ہے:
- **صوبہ سندھ**: لڑکے اور لڑکی دونوں کے لیے شادی کی کم از کم قانونی عمر 18 سال ہے۔
- **دیگر صوبے اور وفاق (پنجاب، اسلام آباد، خیبر پختونخوا، اور بلوچستان)**: لڑکوں کے لیے کم از کم عمر 18 سال اور لڑکیوں کے لیے 16 سال ہے۔
کم عمری کی شادی کروانا یا اس میں سہولت کاری فراہم کرنا ایک قابلِ سزا جرم ہے جس کی سزا جرمانہ اور 2 سال تک قید ہو سکتی ہے۔ (Source: Child Marriage Restraint Act, 1929)

**3. Practical Next Steps**:
1. شادی رجسٹر کرنے سے پہلے فریقین کے قومی شناختی کارڈ (CNIC) یا بی فارم (B-Form) سے عمر کی تصدیق کریں۔
2. نکاح خواں کو دولہا اور دلہن کی تاریخ پیدائش کا ثبوت فراہم کریں۔
3. اگر زبردستی یا قانون کے خلاف کم عمری کی شادی ہو رہی ہو تو قریبی تھانے یا فیملی کورٹ سے رجوع کریں۔

**4. Required Documents**:
فریقین کے شناختی کارڈ (CNIC)، یونین کونسل سے جاری کردہ کمپیوٹرائزڈ پیدائشی سرٹیفکیٹ یا بی فارم (B-Form)۔

**5. Important Notes**:
رول 7 کے تحت یہ نظام تعلیمی مقاصد کے لیے معلومات فراہم کرتا ہے اور پیشہ ورانہ قانونی مشورے کا متبادل نہیں ہے۔`,
    "roman": `**Category (زمرہ)**: Family Laws

**Title**: Shadi Ki Qanooni Umar (Child Marriage Restraint Act)

**1. Direct Answer**:
Pakistan mein shadi ki qanooni umar Child Marriage Restraint Act ke tehat tay hoti hai.

**2. Relevant Pakistani Law**:
Child Marriage Restraint Act ke mutabiq shadi ki kam az kam legal age darj zail hai:
- **Province of Sindh**: Larke aur larki dono ke liye shadi ki kam az kam legal age 18 saal hai.
- **Punjab, Islamabad, KPK, aur Balochistan**: Larkon ke liye legal age 18 saal aur larkiyon ke liye 16 saal hai.
Nabaligh (child) ki shadi karwana ya is mein madad karna qanoonan jurm hai jis ki saza 2 saal tak qaid aur jurmana ho sakti hai. (Source: Child Marriage Restraint Act, 1929)

**3. Practical Next Steps**:
1. Shadi se pehle dulha aur dulhan ke CNIC ya B-Form se age verify karein.
2. Nikah khwan ko date of birth ka verified proof (Birth Certificate) dein.
3. Agar ghair-qanooni child marriage ho rahi ho to police station ya Family Court se contact karein.

**4. Required Documents**:
Parties ke CNIC, Union Council se computerized birth certificate ya B-Form.

**5. Important Notes**:
Rule 7 ke tehat yeh system informational purposes ke liye hai aur professional legal advice ka badal nahi hai.`
  },
  "Polygamy & Second Marriage Permission": {
    "ur": `**Category (زمرہ)**: Family Laws

**Title**: دوسری شادی کی اجازت اور قوانین

**1. Direct Answer**:
شوہر کے لیے دوسری شادی کرنے سے پہلے پہلی بیوی اور یونین کونسل کی ثالثی کونسل سے تحریری اجازت حاصل کرنا لازمی ہے۔

**2. Relevant Pakistani Law**:
مسلم فیملی لاز آرڈیننس 1961 کے سیکشن 6 کے تحت، پہلی بیوی کی رضامندی اور ثالثی کونسل کی منظوری کے بغیر دوسری شادی کرنا ایک سنگین جرم ہے۔ بغیر اجازت شادی کرنے پر شوہر کو فوری طور پر پورا حق مہر ادا کرنا ہوگا، اور اسے 1 سال تک قید اور 5 لاکھ روپے تک جرمانے کی سزا ہو سکتی ہے۔ (Source: Section 6 of the Muslim Family Laws Ordinance, 1961)

**3. Practical Next Steps**:
1. دوسری شادی سے پہلے پہلی بیوی سے رضامندی حاصل کریں اور یونین کونسل میں اجازت کے لیے درخواست دیں۔
2. یونین کونسل کی ثالثی کونسل کی باقاعدہ سماعت کے بعد تحریری اجازت نامہ حاصل کریں۔
3. اگر شوہر نے بغیر اجازت دوسری شادی کی ہو، تو پہلی بیوی فیملی کورٹ میں فوری حق مہر کی وصولی کا دعویٰ دائر کرے اور پولیس میں شکایت درج کروائے۔

**4. Required Documents**:
پہلی بیوی کا تحریری رضامندی فارم، یونین کونسل کا اجازت نامہ، فریقین کے شناختی کارڈ، اور نکاح نامہ۔

**5. Important Notes**:
رول 7 کے تحت یہ نظام تعلیمی مقاصد کے لیے معلومات فراہم کرتا ہے اور پیشہ ورانہ قانونی مشورے کا متبادل نہیں ہے۔`,
    "roman": `**Category (زمرہ)**: Family Laws

**Title**: Doosri Shadi aur Polygamy Laws

**1. Direct Answer**:
Shohar ke liye doosri shadi karne se pehle pehli biwi aur Arbitration Council se written permission lena mandatory hai.

**2. Relevant Pakistani Law**:
Section 6 MFLO 1961 ke tehat, permission ke baghair doosri shadi karna criminal offense hai. Aisa karne par shohar ko pura Haq Mehr foran dena hoga, aur use 1 saal tak qaid aur 5 lakh rupay tak jurmana ho sakta hai. (Source: Section 6 of the Muslim Family Laws Ordinance, 1961)

**3. Practical Next Steps**:
1. Shohar doosri shadi se pehle Arbitration Council ko written application de.
2. Council pehli biwi aur shohar ke arguments sunne ke baad permission decide karegi.
3. Agar bina permission ke shadi ho, to pehli biwi Family Court mein suit for immediate recovery of entire dower file kare.

**4. Required Documents**:
CNIC copies, existing Nikahnama, application to Arbitration Council, and written consent of first wife (if available).

**5. Important Notes**:
Rule 7 ke tehat yeh system informational purposes ke liye hai aur professional legal advice ka badal nahi hai.`
  },
  "Mandatory Marriage Registration under MFLO": {
    "ur": `**Category (زمرہ)**: Family Laws

**Title**: نکاح کی لازمی رجسٹریشن

**1. Direct Answer**:
پاکستان میں مسلم قوانین کے تحت ہونے والی ہر شادی کا نکاح رجسٹرار کے پاس رجسٹرڈ ہونا لازمی ہے۔

**2. Relevant Pakistani Law**:
مسلم فیملی لاز آرڈیننس 1961 کے سیکشن 5 کے تحت نکاح کی رجسٹریشن لازمی ہے۔ رجسٹریشن نہ کروانا ایک قابلِ سزا جرم ہے جس کی سزا 3 ماہ تک قید یا 1 لاکھ روپے جرمانہ ہو سکتی ہے۔ غیر رجسٹرڈ نکاح کی صورت میں حق مہر اور نان و نفقہ کے حقوق کو عدالت میں ثابت کرنا مشکل ہو جاتا ہے۔ (Source: Section 5 of the Muslim Family Laws Ordinance, 1961)

**3. Practical Next Steps**:
1. نکاح کے فوری بعد نکاح نامہ کے چاروں پرتوں پر دستخط کریں اور نکاح رجسٹرار کے پاس رجسٹریشن یقینی بنائیں۔
2. یونین کونسل میں نکاح نامہ جمع کروا کر کمپیوٹرائزڈ میرج سرٹیفکیٹ حاصل کریں۔
3. نکاح نامہ کی اصل کاپی اپنے پاس محفوظ رکھیں۔

**4. Required Documents**:
نکاح نامہ کا پرت، دولہا دلہن اور گواہان کے قومی شناختی کارڈ، اور رجسٹریشن فیس۔

**5. Important Notes**:
رول 7 کے تحت یہ نظام تعلیمی مقاصد کے لیے معلومات فراہم کرتا ہے اور پیشہ ورانہ قانونی مشورے کا متبادل نہیں ہے۔`,
    "roman": `**Category (زمرہ)**: Family Laws

**Title**: Shadi Ki Mandatory Registration (Nikah)

**1. Direct Answer**:
Pakistan mein har Muslim marriage ka Nikah Registrar ke paas register hona mandatory hai.

**2. Relevant Pakistani Law**:
Section 5 MFLO 1961 ke tehat registration lazmi hai. Registration na karwane par 3 months qaid ya 1 lakh rupay jurmana ho sakta hai. Unregistered marriage ko court mein prove karna aur Haq Mehr claim karna bohat mushkil hota hai. (Source: Section 5 of the Muslim Family Laws Ordinance, 1961)

**3. Practical Next Steps**:
1. Nikah ke foran baad Nikah Registrar se Nikahnama sign aur stamp karwain.
2. Union Council mein register karwa kar computerized Marriage Registration Certificate (MRC) hasil karein.
3. MRC aur original Nikahnama ko safe custody mein rakhein.

**4. Required Documents**:
Signed Nikahnama, CNICs of bride, groom, Nikah Khwan, and witnesses.

**5. Important Notes**:
Rule 7 ke tehat yeh system informational purposes ke liye hai aur professional legal advice ka badal nahi hai.`
  },
  "Divorce by Husband (Talaq Notice & Certificate)": {
    "ur": `**Category (زمرہ)**: Family Laws

**Title**: شوہر کی طرف سے طلاق اور نوٹس کا طریقہ کار

**1. Direct Answer**:
شوہر کے لیے طلاق دینے کے بعد متعلقہ یونین کونسل کے چیئرمین کو تحریری نوٹس بھیجنا اور بیوی کو اس کی کاپی دینا لازمی ہے۔

**2. Relevant Pakistani Law**:
مسلم فیملی لاز آرڈیننس 1961 کے سیکشن 7 کے تحت، طلاق کا نوٹس موصول ہونے کے بعد یونین کونسل 90 دن کے اندر مصالحت کے لیے ایک ثالثی کونسل تشکیل دیتی ہے۔ اگر مصالحت ناکام ہو جائے تو نوٹس ملنے کے 90 دن (یا حمل کی صورت میں بچے کی پیدائش) کے بعد طلاق مؤثر ہو جاتی ہے اور طلاق کا سرٹیفکیٹ جاری کیا جاتا ہے۔ (Source: Section 7 of the Muslim Family Laws Ordinance, 1961)

**3. Practical Next Steps**:
1. طلاق دینے کے بعد، تحریری نوٹس بذریعہ رجسٹرڈ ڈاک یونین کونسل چیئرمین کو بھیجیں اور ایک کاپی بیوی کو ارسال کریں۔
2. یونین کونسل کی ثالثی کارروائیوں میں شرکت کریں۔
3. 90 دن کی مدت مکمل ہونے کے بعد یونین کونسل سے طلاق کا مؤثر سرٹیفکیٹ (Divorce Effectiveness Certificate) حاصل کریں۔

**4. Required Documents**:
تحریری طلاق نامہ، یونین کونسل کا نوٹس فارم، شناختی کارڈ کی کاپی، اور ڈاک کی رسید۔

**5. Important Notes**:
رول 7 کے تحت یہ نظام تعلیمی مقاصد کے لیے معلومات فراہم کرتا ہے اور پیشہ ورانہ قانونی مشورے کا متبادل نہیں ہے۔`,
    "roman": `**Category (زمرہ)**: Family Laws

**Title**: Shohar Ki Taraf Se Talaq (Notice & Certificate)

**1. Direct Answer**:
Shohar ke liye talaq dene ke baad Union Council ko written notice bhejna aur biwi ko copy dena mandatory hai.

**2. Relevant Pakistani Law**:
Section 7 MFLO 1961 ke tehat, notice milne ke baad Union Council 90 days ke andar reconciliation ki koshish karti hai. Agar reconciliation fail ho jaye to 90 days baad divorce effective certificate issue kar diya jata hai. (Source: Section 7 of the Muslim Family Laws Ordinance, 1961)

**3. Practical Next Steps**:
1. Talaq pronounce karne ke baad, immediately Union Council Chairman ko written notice registered post se send karein aur copy biwi ko dein.
2. Union Council ke summons par Arbitration proceedings join karein.
3. 90 days ka iddat period pass hone par Union Council se Divorce Effectiveness Certificate hasil karein.

**4. Required Documents**:
Written Talaqnama, Union Council notice form, CNICs, and postal receipts.

**5. Important Notes**:
Rule 7 ke tehat yeh system informational purposes ke liye hai aur professional legal advice ka badal nahi hai.`
  },
  "Divorce by Wife (Court Khula & Dower Waiver)": {
    "ur": `**Category (زمرہ)**: Family Laws

**Title**: بیوی کی طرف سے خلع اور حق مہر کی دستبرداری

**1. Direct Answer**:
اگر بیوی کے پاس نکاح نامہ میں طلاق کا حق (Talaq-e-Tafweez) نہ ہو، تو وہ فیملی کورٹ میں خلع کا دعویٰ دائر کر کے اپنی شادی ختم کر سکتی ہے۔

**2. Relevant Pakistani Law**:
مسلم فیملی لاز آرڈیننس 1961 کے سیکشن 8 کے تحت، بیوی کو فیملی کورٹ کے ذریعے خلع حاصل کرنے کا حق حاصل ہے۔ خلع حاصل کرنے کی صورت میں، بیوی کو عام طور پر اپنا غیر ادا شدہ حق مہر (Haq Mehr) معاف کرنا پڑتا ہے یا موصول شدہ حق مہر کا کچھ حصہ واپس کرنا پڑتا ہے۔ (Source: Section 8 of the Muslim Family Laws Ordinance, 1961)

**3. Practical Next Steps**:
1. فیملی وکیل سے رجوع کر کے فیملی کورٹ میں خلع اور دائرہ مہر کا دعویٰ دائر کریں۔
2. عدالتی سمن جاری ہونے کے بعد، مصالحتی کارروائی (Pre-trial reconciliation) میں شرکت کریں۔
3. اگر مصالحت ناکام ہو جائے تو عدالت سے خلع کی ڈگری حاصل کریں اور اسے یونین کونسل میں رجسٹریشن کے لیے جمع کروائیں۔

**4. Required Documents**:
اصل نکاح نامہ (یا یونین کونسل سے تصدیق شدہ کاپی)، شناختی کارڈ، اور دعویٰ خلع کا مسودہ۔

**5. Important Notes**:
رول 7 کے تحت یہ نظام تعلیمی مقاصد کے لیے معلومات فراہم کرتا ہے اور پیشہ ورانہ قانونی مشورے کا متبادل نہیں ہے۔`,
    "roman": `**Category (زمرہ)**: Family Laws

**Title**: Biwi Ki Taraf Se Khula (Court Dissolution)

**1. Direct Answer**:
Agar biwi ke paas divorce ka right na ho, to wo Family Court mein Khula ka suit file kar ke marriage dissolve karwa sakti hai.

**2. Relevant Pakistani Law**:
Section 8 MFLO 1961 ke tehat biwi court se Khula le sakti hai. Khula ke badle mein biwi ko amuman apna deferred dower (Haq Mehr) waive karna parta hai ya received prompt Mehr return karna hota hai. (Source: Section 8 of the Muslim Family Laws Ordinance, 1961)

**3. Practical Next Steps**:
1. Family lawyer ke zariye Family Court mein suit for dissolution of marriage on basis of Khula file karein.
2. Court ke pre-trial reconciliation hearing mein appear hon.
3. Reconciliation fail hone par court se decree of Khula hasil karein aur Union Council mein submit karein.

**4. Required Documents**:
Original Nikahnama, CNIC of wife, and suit draft copy.

**5. Important Notes**:
Rule 7 ke tehat yeh system informational purposes ke liye hai aur professional legal advice ka badal nahi hai.`
  },
  "Court Marriage Procedure & Consent": {
    "ur": `**Category (زمرہ)**: Family Laws

**Title**: کورٹ میرج کا طریقہ کار اور رضامندی

**1. Direct Answer**:
پاکستان میں بالغ لڑکا اور لڑکی (18 سال یا اس سے زیادہ) مجسٹریٹ اور نکاح رجسٹرار کے سامنے آزادانہ رضامندی سے کورٹ میرج کر سکتے ہیں۔

**2. Relevant Pakistani Law**:
شادی کے لیے لڑکی کا مجسٹریٹ کے سامنے اپنی آزاد مرضی کا حلف نامہ (Affidavit of Free Will) دینا لازمی ہے جس میں وہ بیان کرے کہ وہ بغیر کسی دباؤ یا اغوا کے شادی کر رہی ہے۔ لڑکی کے خاندان کی طرف سے دائر کیے جانے والے اغوا کے جھوٹے مقدمات (FIRs) سے بچنے کے لیے جوڑا ہائی کورٹ سے حفاظتی پٹیشن (Protection petition) دائر کر سکتا ہے۔ (Source: Specific Provisions of Shariah & Child Marriage Restraint Act)

**3. Practical Next Steps**:
1. نکاح رجسٹرار اور وکیل کے سامنے نکاح فارم اور حلف ناموں پر دستخط کریں۔
2. مجسٹریٹ کے سامنے لڑکی کا بیان ریکارڈ کروائیں کہ وہ اپنی مرضی سے شادی کر رہی ہے۔
3. تحفظ حاصل کرنے اور جھوٹے پولیس مقدمات کو خارج کروانے کے لیے ہائی کورٹ میں پروٹیکشن پٹیشن دائر کریں۔

**4. Required Documents**:
دولہا دلہن کے شناختی کارڈ یا تعلیمی اسناد (عمر کے ثبوت کے لیے)، پاسپورٹ سائز تصاویر، اور گواہان کے شناختی کارڈ۔

**5. Important Notes**:
رول 7 کے تحت یہ نظام تعلیمی مقاصد کے لیے معلومات فراہم کرتا ہے اور پیشہ ورانہ قانونی مشورے کا متبادل نہیں ہے۔`,
    "roman": `**Category (زمرہ)**: Family Laws

**Title**: Court Marriage Ka Procedure aur Consent

**1. Direct Answer**:
Pakistan mein adult larka aur larki (18 saal ya us se baray) Magistrate aur Nikah Registrar ke samnay apni free will se court marriage kar sakte hain.

**2. Relevant Pakistani Law**:
Larki ko magistrate ke samnay free will affidavit sign karna hota hai jahan wo state karti hai ke wo bina kisi coercion ya force ke shadi kar rahi hai. False abduction FIRs se bachne ke liye couple High Court mein protection petition file kar sakta hai. (Source: Specific Provisions of Shariah & Child Marriage Restraint Act)

**3. Practical Next Steps**:
1. Nikah Registrar aur lawyer ke samnay Nikah paper aur Free Will Affidavit sign karein.
2. Magistrate ke samnay larki ka free will statement record karwain.
3. Local police aur family ki harassment se bachne ke liye High Court mein protection suit file karein.

**4. Required Documents**:
CNIC/Matric certificate (as age proof), passport size pictures, and CNIC of witnesses.

**5. Important Notes**:
Rule 7 ke tehat yeh system informational purposes ke liye hai aur professional legal advice ka badal nahi hai.`
  }
};

const EXPANSION_RULES: Array<{ triggers: string[]; expansions: string[] }> = [
  {
    triggers: ["talaq", "talaaq", "divorce", "dissolution", "طلاق"],
    expansions: ["divorce", "dissolution of marriage", "talaq notice", "talaq certificate", "union council notice"]
  },
  {
    triggers: ["iddat", "waiting period", "عدت"],
    expansions: ["iddat period", "iddat rules", "waiting period", "iddat maintenance"]
  },
  {
    triggers: ["khula", "kula", "خلع"],
    expansions: ["khula", "dissolution of marriage", "dower waiver"]
  },
  {
    triggers: ["nikah", "nikaah", "shadi", "shaadi", "marriage", "نکاح", "شادی"],
    expansions: ["marriage registration", "nikahnama", "marriage contract"]
  },
  {
    triggers: ["kharcha", "nafaqa", "maintenance", "expenses", "خرچہ", "نفقہ"],
    expansions: ["child maintenance", "wife maintenance", "expenses allowance"]
  },
  {
    triggers: ["custody", "guardian", "guardianship", "ward", "bache", "bachay", "children", "minor", "کسٹڈی", "تحویل", "سرپرستی", "بچے"],
    expansions: ["child custody", "visitation rights", "guardianship", "minor ward"]
  },
  {
    triggers: ["qabza", "kabza", "possession", "encroachment", "قبضہ", "تجاوز"],
    expansions: ["illegal possession", "encroachment", "dispossession", "illegal dispossession"]
  },
  {
    triggers: ["rent", "kiraya", "kirayedar", "tenant", "landlord", "eviction", "evict", "کرایہ", "کرایہ دار"],
    expansions: ["tenancy agreement", "tenant rights", "eviction", "landlord dispute"]
  },
  {
    triggers: ["fir", "police", "sho", "thana", "ایف آئی آر", "تھانہ"],
    expansions: ["fir registration", "police complaint", "section 154 crpc"]
  },
  {
    triggers: ["bail", "zamanat", "ضمانت"],
    expansions: ["pre-arrest bail", "post-arrest bail", "protective bail"]
  },
  {
    triggers: ["tax", "fbr", "filer", "return", "ٹیکس", "ایف بی آر"],
    expansions: ["income tax return", "fbr audit", "tax assessment"]
  },
  {
    triggers: ["consumer", "refund", "warranty", "fake", "defective", "ریفنڈ", "وارنٹی"],
    expansions: ["consumer court", "defective product", "refund replacement"]
  },
  {
    triggers: ["age", "عمر", "minor", "child marriage", "na-baligh", "نابالغ"],
    expansions: ["legal age of marriage", "minimum marriageable age", "child marriage restraint act"]
  }
];

const CLARIFYING_QUESTIONS: Record<string, Record<string, string>> = {
  "Property Laws": {
    ur: "کیا آپ کے پاس جائیداد کی رجسٹری یا کوئی تحریری معاہدہ (Registry/Tenancy/Agreement) موجود ہے؟ اور کیا آپ مالک ہیں یا کرایہ دار؟",
    roman: "Kya aap ke paas property ki registry ya koi written agreement (Tenancy/Registry) mojood hai? Aur kya aap owner hain ya tenant?",
    en: "Do you have a written property registry, mutation, or tenancy agreement? Also, are you the owner or a tenant?"
  },
  "Family Laws": {
    ur: "کیا آپ کا نکاح نامہ رجسٹرڈ ہے؟ اور کیا آپ نان و نفقہ (خرچہ)، خلع، یا بچوں کی کسٹڈی کے بارے میں پوچھ رہے ہیں؟",
    roman: "Kya aap ka Nikahnama registered hai? Aur kya aap maintenance (kharcha), Khula, ya child custody ke baare mein pooch rahe hain?",
    en: "Is the marriage registered with a Nikahnama? Are you seeking maintenance, Khula, child custody, or divorce?"
  },
  "Criminal Laws": {
    ur: "کیا اس معاملے کی ایف آئی آر (FIR) پہلے سے درج ہو چکی ہے؟ اور کیا ملزم پولیس کی حراست میں ہے یا ضمانت چاہتے ہیں؟",
    roman: "Kya is mamlay ki FIR pehle se registered ho chuki hai? Aur kya accused police custody mein hai ya bail chahtay hain?",
    en: "Has a First Information Report (FIR) already been registered? Is the accused currently arrested or seeking bail?"
  },
  "Civil Laws": {
    ur: "کیا فریقین کے درمیان کوئی تحریری معاہدہ یا اقرار نامہ موجود ہے؟ کیا آپ نے کوئی قانونی نوٹس بھیجا ہے؟",
    roman: "Kya parties ke darmiyan koi written agreement ya contract mojood hai? Kya aapne koi legal notice send kiya hai?",
    en: "Is there a written contract or agreement between the parties? Have you served a formal legal notice yet?"
  },
  "Labour Laws": {
    ur: "کیا آپ کے پاس تقرری کا تحریری خط (Appointment Letter) یا معاہدہ موجود ہے؟ اور کیا معاملہ تنخواہ کا ہے یا برطرفی کا؟",
    roman: "Kya aap ke paas appointment letter ya written employment contract hai? Aur kya masla salary ka hai ya termination ka?",
    en: "Do you have a written appointment letter or employment contract? Is the dispute regarding unpaid wages or termination?"
  },
  "Tax Laws": {
    ur: "کیا آپ ایف بی آر (FBR) میں فائلر رجسٹرڈ ہیں؟ اور کیا یہ نوٹس انکم ٹیکس کا ہے یا سیلز ٹیکس کا؟",
    roman: "Kya aap FBR ke filer hain ya non-filer? Aur kya yeh notice income tax ka hai ya sales tax ka?",
    en: "Are you registered as a filer or non-filer with FBR? Is this query regarding an income tax notice or sales tax?"
  },
  "Consumer Protection Laws": {
    ur: "کیا آپ کے پاس خریداری کی رسید (Receipt) یا وارنٹی کارڈ موجود ہے؟ اور کیا آپ نے دکاندار کو 15 دن کا تحریری قانونی نوٹس بھیجا ہے؟",
    roman: "Kya aap ke paas purchase receipt ya warranty document hai? Aur kya aapne shopkeeper ko 15 days ka written legal notice send kiya hai?",
    en: "Do you have the purchase receipt or warranty document? Have you served the mandatory 15-day legal notice to the seller?"
  },
  "Constitutional Laws": {
    ur: "کیا یہ خلاف ورزی کسی سرکاری افسر یا سرکاری ادارے (Government Department) کی طرف سے کی گئی ہے یا کسی نجی شخص کی طرف سے؟",
    roman: "Kya yeh violation kisi government department/official ne ki hai ya kisi private individual ne?",
    en: "Was this violation committed by a government official or public authority, or a private entity?"
  }
};

function getQueryExpansions(text: string): string[] {
  const textLower = text.toLowerCase();
  const expansions: string[] = [];
  for (const rule of EXPANSION_RULES) {
    let matched = false;
    for (const trigger of rule.triggers) {
      const regex = new RegExp('(?<![\\p{L}\\p{N}_])' + trigger.replace(/[\\^$*+?.()|[\\]{}]/g, '\\$&') + '(?![\\p{L}\\p{N}_])', 'iu');
      if (regex.test(textLower)) {
        matched = true;
        break;
      }
    }
    if (matched) {
      expansions.push(...rule.expansions);
    }
  }
  return Array.from(new Set(expansions));
}

// Cache the dataset in memory to make subsequent requests fast
let cachedDataset: any[] | null = null;
let cachedBM25: any | null = null;
let cachedIdToIndex: Map<string, number> | null = null;

const ROMAN_URDU_WORDS = new Set([
  "hai", "hain", "aur", "ko", "se", "ka", "ki", "ke", "mein", "kya", "kiya", "nahi", "nahin", 
  "hota", "hote", "hoti", "hoga", "hogi", "hogay", "tha", "thi", "the", "par", "pe", "per", "ya", 
  "agar", "ho", "krna", "karna", "kr", "kar", "rha", "raha", "rahi", "rhe", "rahe", "hun", "hoon", 
  "sath", "saath", "liye", "liya", "diya", "de", "ek", "aik", "puchna", "bolna", 
  "smjh", "samajh", "chahiye", "kuch", "kuchh", "baare", "bare", "kare", "karey", "karta", "kartay", 
  "karti", "khatam", "shuru", "nikaah", "nikah", "shadi", "talaq", "khula", "masla", "qanoon", 
  "kanoon", "adalat", "mujhe", "mujh", "mera", "meri", "mere", "tum", "tumhara", "aap", "aapka", 
  "apka", "apki", "aapki", "bhai", "behan", "abbu", "ammi", "walid", "walida", "bacha", "bache", 
  "larki", "larka", "aurat", "mard", "khawateen", "shohar", "biwi", "talaaq", "zameen", "ghar", "bhi"
]);

const ENGLISH_INDICATORS = new Set([
  "the", "be", "to", "of", "and", "a", "in", "that", "have", "it", "for", "not", "on", "with", "he", 
  "as", "you", "do", "at", "this", "but", "his", "by", "from", "they", "we", "say", "her", "she", 
  "or", "an", "will", "my", "one", "all", "would", "there", "their", "what", "so", "up", "out", 
  "if", "about", "who", "get", "which", "go", "me", "when", "make", "can", "like", "time", "no", 
  "just", "him", "know", "take", "people", "into", "year", "your", "good", "some", "could", 
  "them", "see", "other", "than", "then", "now", "look", "only", "come", "its", "over", 
  "think", "also", "back", "after", "use", "two", "how", "our", "work", "first", "well", 
  "way", "even", "new", "want", "because", "any", "these", "give", "day", "most", "us", 
  "is", "are", "was", "were", "been", "has", "had", "should", "would", "could", "law", 
  "legal", "court", "pakistani", "process", "rights", "harassment", "cyber", "tenant"
]);

const RULES: Record<string, string[]> = {
  "Constitutional Laws": [
    "constitution", "constitutional", "article", "fundamental right", "supreme court", 
    "high court", "writ", "petition", "suo motu", "senate", "parliament", "national assembly", 
    "president", "prime minister", "justice of peace", "fundamental rights", "habeas corpus", 
    "mandamus", "prohibition", "certiorari", "quo warranto", "legislation", "act of parliament",
    "amendment", "state of pakistan",
    "constitutional rights", "government", "freedom", "speech", "privacy", "sarkari", "idara",
    "بنیادی حقوق", "آئینی حقوق", "آئین", "دستور", "حکومت", "آزادی", "تقریر", "اظہار رائے", "پرائیویسی",
    "freedom of speech", "writ petition", "judicial review", "article 199"
  ],
  "Family Laws": [
    "divorce", "khula", "talaq", "maintenance", "iddat", "dowry", "dower", "nikah", 
    "custody", "guardian", "marriage", "domestic violence", "court marriage", "spouse",
    "ward", "union council", "dower amount", "shariah", "dissolution of marriage", "bride",
    " bridal", "wife", "husband", "children", "minor", "visitation",
    "talaaq", "kula", "shohar", "shoher", "biwi", "beewi", "nikah", "nikaah", "bachay", "kharcha", "kharja", "nafaqa", "shadi", "shaadi", "khawand", "bache", "larki", "larka", "aurat", "mard",
    "طلاق", "خلع", "شوہر", "بیوی", "نکاح", "بچے", "بچوں", "بچہ", "خرچہ", "نفقہ", "کسٹڈی", "شادی", "خاوند", "اولاد", "تحویل", "سرپرستی",
    "nikahnama", "guardianship"
  ],
  "Property Laws": [
    "property", "possession", "illegal possession", "land", "dispute", "inheritance", 
    "registry", "patwari", "fard", "mutation", "transfer fee", "gift deed", "hiba", 
    "stamp paper", "encroachment", "title deed", "wirasat", "intiqal", "qabza", "mafia",
    "dispossess", "dispossession", "sub-registrar", "mortgage", "charge", "lease", "tenancy",
    "actionable claim", "compulsory registration", "benami", "stamp duty", "easement",
    "prescription", "partition", "co-ownership", "adverse possession", "squatter",
    "illegal dispossession act", "transfer of property act",
    "landlord", "tenant", "evict", "eviction", "rent", "rented", "house", "lease agreement",
    "malik makan", "kirayedar", "kiraya", "makan", "ghar se nikal",
    "kabza", "kabja", "qabzah", "kabzah", "qabzaa", "zameen", "jameen", "zamin", "jamin", "plot", "diwar", "boundary", "virasat", "malikmakan", "kirayedaar", "ghar",
    "قبضہ", "قبضے", "زمین", "پلاٹ", "پراپرٹی", "جائیداد", "جائداد", "رجسٹری", "انتقال", "دیوار", "حدود", "وراثت", "مالک مکان", "کرایہ دار", "کرائے دار", "کرایہ", "مکان", "گھر"
  ],
  "Criminal Laws": [
    "fir", "police", "arrest", "false fir", "bail", "thana", "sho", "complaint", 
    "refusal", "remand", "custodial", "crpc", "cognizable", "pre-arrest bail", 
    "post-arrest bail", "section 22", "theft", "mischief", "murder", "assault", "conspiracy",
    "forgery", "penal code", "ppc", "criminal", "stolen", "perpetrator",
    "302", "489-f", "497", "498", "cnsa", "peca", "self-defense", "private defense", 
    "kidnapping", "abduction", "defamation", "ransom", "fraud", "trust", "trespass", 
    "narcotics", "harassment", "drugs", "rape", "cheating", "cyber",
    "giraftar", "qatl", "chori", "dhamki", "zamanat", "saza", "jurm",
    "ایف آئی آر", "پولیس", "گرفتار", "گرفتاری", "قتل", "چوری", "فراڈ", "دھمکی", "تھانہ", "ضمانت", "سزا", "جرم",
    "threat", "intimidation"
  ],
  "Consumer Protection Laws": [
    "consumer", "refund", "faulty", "fake product", "damaged item", "warranty", 
    "consumer court", "online store scam", "expiry date", "defective goods", 
    "unfair trade", "misleading advertisement", "receipt", "deficient service", "replacement",
    "defective", "substandard", "negligence", "invoice", "overcharging", "notice", "frivolous",
    "online shopping", "raseed", "bill",
    "ریفنڈ", "وارنٹی", "آن لائن خریداری", "ناقص مصنوعات", "ناقص اشیاء", "نقلی", "فیک", "رسید", "بل",
    "fake", "misleading"
  ],
  "Labour Laws": [
    "salary", "employer", "termination", "contract", "wrongful termination", 
    "overtime", "gratuity", "pension", "provident fund", "labor court", "wages", 
    "resignation", "severance", "employment agreement", "notice period", "workplace",
    "employee", "worker", "maternity", "social security", "pessi", "sessi", "eobi",
    "working hours", "weekly holiday", "paid leave", "sick leave", "workplace safety",
    "occupational health", "workmen compensation", "child labor", "trade union", "cba",
    "tankhwa", "boss", "job", "dismissal", "mulazmat", "naukri",
    "تنخواہ", "مالک", "ملازمت", "نوکری", "برطرفی", "گریجویٹی", "پنشن", "ملازم", "آجر", "اوور ٹائم", "اوورٹائم",
    "labour court", "employment"
  ],
  "Tax Laws": [
    "tax", "income tax", "sales tax", "fbr", "tax return", "tax assessment", 
    "default surcharge", "filing return", "audit", "tax tribunal", "withholding",
    "invoice", "taxpayer", "revenue board", "inland revenue",
    "wht", "surcharge", "atl", "customs", "excise", "provincial", "cgt",
    "filer", "non-filer", "adrc", "pra", "srb", "kpra", "bra",
    "non filer", "ntn", "return",
    "ٹیکس", "ایف بی آر", "فائلر", "نان فائلر", "این ٹی این", "ریٹرن", "گوشوارہ"
  ],
  "Civil Laws": [
    "civil", "specific relief", "specific performance", "injunction", "stay order", 
    "declaratory", "declaration", "specific performance of contract", "indemnity",
    "arbitration", "contract act", "void contract", "voidable contract", "void agreement",
    "guarantee", "surety", "principal debtor", "bailment", "pledge", "agency", "principal and agent",
    "cancellation of deed", "rectification of contract", "civil court", "pecuniary jurisdiction",
    "territorial jurisdiction", "plaint", "written statement", "summons", "execution of decree",
    "civil appeal", "revision petition", "review petition", "limitation period", "limitation act",
    "cpc", "civil procedure",
    "agreement", "paisay", "qarz", "recovery", "harjana", "muahida", "stay",
    "معاہدہ", "اقرار نامہ", "اقرارنامہ", "پیسے", "قرض", "ریکوری", "ہرجانہ", "سٹے", "حکم امتناعی", "منسوخی",
    "money", "debt", "damages", "compensation", "breach", "civil suit"
  ]
};

const BM25_STOP_WORDS = new Set([
  "the", "be", "to", "of", "and", "a", "in", "that", "have", "it", "for", "not", "on", "with", "he", 
  "as", "you", "do", "at", "this", "but", "his", "by", "from", "they", "we", "say", "her", "she", 
  "or", "an", "will", "my", "one", "all", "would", "there", "their", "what", "so", "up", "out", 
  "if", "about", "who", "get", "which", "go", "me", "when", "make", "can", "like", "time", "no", 
  "just", "him", "know", "take", "people", "into", "year", "your", "good", "some", "could", 
  "them", "see", "other", "than", "then", "now", "look", "only", "come", "its", "over", 
  "think", "also", "back", "after", "use", "two", "how", "our", "work", "first", "well", 
  "way", "even", "new", "want", "because", "any", "these", "give", "day", "most", "us", 
  "is", "are", "was", "were", "been", "has", "had", "should", "would", "could"
]);

class BM25 {
  corpus: string[][];
  docLengths: number[];
  avgDocLength: number;
  docFreqs: Record<string, number>;
  idf: Record<string, number>;
  k1: number;
  b: number;

  constructor(corpus: string[], k1 = 1.5, b = 0.75) {
    this.k1 = k1;
    this.b = b;
    this.corpus = corpus.map(doc => this.tokenize(doc));
    this.docLengths = this.corpus.map(doc => doc.length);
    const totalLength = this.docLengths.reduce((a, b) => a + b, 0);
    this.avgDocLength = corpus.length > 0 ? totalLength / corpus.length : 1.0;
    
    this.docFreqs = {};
    for (const doc of this.corpus) {
      const seen = new Set(doc);
      for (const w of seen) {
        this.docFreqs[w] = (this.docFreqs[w] || 0) + 1;
      }
    }
    
    this.idf = {};
    const corpusSize = corpus.length;
    for (const [w, freq] of Object.entries(this.docFreqs)) {
      this.idf[w] = Math.log((corpusSize - freq + 0.5) / (freq + 0.5) + 1.0);
    }
  }

  tokenize(text: string): string[] {
    return text.toLowerCase()
      .replace(/[^\p{L}\p{N}\s]/gu, ' ')
      .split(/\s+/)
      .filter(w => w && !BM25_STOP_WORDS.has(w));
  }

  getScore(queryTokens: string[], docIdx: number): number {
    let score = 0.0;
    const docTokens = this.corpus[docIdx];
    const docLen = this.docLengths[docIdx];
    
    const wordCounts: Record<string, number> = {};
    for (const w of docTokens) {
      wordCounts[w] = (wordCounts[w] || 0) + 1;
    }
    
    for (const w of queryTokens) {
      if (wordCounts[w] !== undefined) {
        const freq = wordCounts[w];
        const idf_val = this.idf[w] || 0.0;
        const tfNumerator = freq * (this.k1 + 1);
        const tfDenominator = freq + this.k1 * (1 - this.b + this.b * (docLen / this.avgDocLength));
        score += idf_val * (tfNumerator / tfDenominator);
      }
    }
    return score;
  }
}

function loadDataset() {
  if (cachedDataset) return cachedDataset;
  try {
    const filePath = path.join(process.cwd(), 'legal_ai', 'dataset', 'legal_dataset.json');
    if (fs.existsSync(filePath)) {
      const data = fs.readFileSync(filePath, 'utf8');
      cachedDataset = JSON.parse(data);
      console.log(`Loaded dataset of size ${cachedDataset?.length}`);
    } else {
      console.warn("Dataset file not found at:", filePath);
      cachedDataset = [];
    }
  } catch (error) {
    console.error("Failed to load dataset:", error);
    cachedDataset = [];
  }
  return cachedDataset;
}

function getDatasetAndIndex() {
  const dataset = loadDataset();
  if (cachedBM25 && cachedIdToIndex) {
    return { dataset, bm25: cachedBM25, idToIndex: cachedIdToIndex };
  }

  const start = Date.now();
  console.log("Starting BM25 index initialization...");
  const corpusTexts = dataset.map(r => {
    const qText = r.question || '';
    const kwText = r.keywords ? (Array.isArray(r.keywords) ? r.keywords.join(' ') : String(r.keywords)) : '';
    return cleanText(`${r.title || ''} ${r.statute || ''} ${qText} ${kwText} ${r.answer || ''}`);
  });
  cachedBM25 = new BM25(corpusTexts);

  cachedIdToIndex = new Map<string, number>();
  for (let i = 0; i < dataset.length; i++) {
    cachedIdToIndex.set(dataset[i].id, i);
  }
  console.log(`BM25 index initialized in ${Date.now() - start}ms`);

  return { dataset, bm25: cachedBM25, idToIndex: cachedIdToIndex };
}

function detectLanguage(text: string): string {
  if (!text || !text.trim()) return 'english';

  if (/[\u0600-\u06FF]/.test(text)) {
    return 'urdu_script';
  }

  const words = text.toLowerCase().match(/\b\w+\b/g) || [];
  if (words.length === 0) return 'english';

  let romanMatches = 0;
  let englishMatches = 0;

  for (const w of words) {
    if (ROMAN_URDU_WORDS.has(w)) romanMatches++;
    if (ENGLISH_INDICATORS.has(w)) englishMatches++;
  }

  if (englishMatches > romanMatches) {
    return 'english';
  }

  if (romanMatches > 1 || (words.length <= 4 && romanMatches >= 1)) {
    return 'roman_urdu';
  }

  return 'english';
}

async function translateText(text: string, sl = 'auto', tl = 'en'): Promise<string> {
  if (!text || !text.trim()) return text;
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 1500);
  try {
    const url = 'https://translate.googleapis.com/translate_a/single';
    const params = new URLSearchParams();
    params.append('client', 'gtx');
    params.append('sl', sl);
    params.append('tl', tl);
    params.append('dt', 't');
    params.append('q', text);

    const res = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0'
      },
      body: params.toString(),
      signal: controller.signal
    });
    clearTimeout(timeoutId);
    if (!res.ok) return text;
    const data = await res.json();
    return data[0].map((s: any) => s[0]).join('');
  } catch (e) {
    clearTimeout(timeoutId);
    console.error("Translation failed:", e);
    return text;
  }
}

async function translateToUrduAndRoman(text: string): Promise<{ urdu: string, roman: string }> {
  if (!text || !text.trim()) return { urdu: text, roman: text };
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 1500);
  try {
    const url = 'https://translate.googleapis.com/translate_a/single';
    const params = new URLSearchParams();
    params.append('client', 'gtx');
    params.append('sl', 'en');
    params.append('tl', 'ur');
    params.append('dt', 't');
    params.append('dt', 'rm');
    params.append('q', text);
    
    const res = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0'
      },
      body: params.toString(),
      signal: controller.signal
    });
    clearTimeout(timeoutId);
    if (!res.ok) return { urdu: text, roman: text };
    
    const data = await res.json();
    let urduScript = '';
    for (const s of data[0]) {
      if (s[0]) urduScript += s[0];
    }
    
    let romanUrdu = '';
    if (data[0] && data[0].length > 0) {
      const lastSegment = data[0][data[0].length - 1];
      if (lastSegment && lastSegment.length > 2 && lastSegment[2]) {
        romanUrdu = lastSegment[2];
      }
    }
    
    if (!romanUrdu) {
      romanUrdu = urduScript;
    }
    
    return { urdu: urduScript, roman: romanUrdu };
  } catch (e) {
    clearTimeout(timeoutId);
    console.error("Urdu/Roman translation failed:", e);
    return { urdu: text, roman: text };
  }
}

function classify(text: string): { category: string; maxScore: number } {
  const textLower = text.toLowerCase();
  const scores: Record<string, number> = {};
  
  for (const [category, keywords] of Object.entries(RULES)) {
    scores[category] = 0;
    for (const kw of keywords) {
      const regex = new RegExp('(?<![\\p{L}\\p{N}_])' + kw.replace(/[\\^$*+?.()|[\\]{}]/g, '\\$&') + '(?![\\p{L}\\p{N}_])', 'iu');
      const matches = textLower.match(regex);
      if (matches) {
        scores[category] += matches.length + 1;
      }
    }
  }
  
  let bestCategory = "Constitutional Laws";
  let maxScore = 0;
  for (const [cat, score] of Object.entries(scores)) {
    if (score > maxScore) {
      maxScore = score;
      bestCategory = cat;
    }
  }
  return { category: bestCategory, maxScore };
}

function cleanText(text: string): string {
  if (!text) return "";
  // Keep all letter and number characters in any language (including Urdu), plus common punctuation and spaces.
  return text.replace(/[^\p{L}\p{N}\s\.,\?\-–⚖️]/gu, ' ').replace(/\s+/g, ' ').trim();
}

function formatStructuredResponse(query: string, category: string, record: any): string {
  const title = record.title || `Pakistani Legal Analysis: ${category}`;
  const source = record.source || "Constitution and Statutes of Pakistan";
  const statute = record.statute || "Statutory Provisions of Pakistan";
  const answerText = record.answer || "";
  
  let directAnswer = `Based on your query regarding **${title}** under **${category}** in Pakistan: `;
  
  if (category === "Family Laws") {
    directAnswer += "Your family law matter is governed by the Muslim Family Laws Ordinance 1961 and the Guardians and Wards Act 1890. You have the right to seek recourse through the Family Courts or local Union Council.";
  } else if (category === "Criminal Laws") {
    directAnswer += "The relevant procedural and penal code actions dictate filing an FIR and seeking appropriate bail or prosecution remedies under CrPC/PPC.";
  } else if (category === "Civil Laws") {
    directAnswer += "Equitable relief and contract dispute resolutions must be sought through civil courts under the Specific Relief Act 1877 or Contract Act 1872.";
  } else if (category === "Property Laws") {
    directAnswer += "Possession, transfer, and ownership protection fall under the Transfer of Property Act 1882, the Registration Act 1908, or the Illegal Dispossession Act 2005.";
  } else if (category === "Labour Laws") {
    directAnswer += "Wages, wrongful termination, and gratuity claims are adjudicated in Labor Courts under the Standing Orders Ordinance 1968 or Payment of Wages Act 1936.";
  } else if (category === "Tax Laws") {
    directAnswer += "Tax assessments, return filings, and FBR audit appeals are governed by the Income Tax Ordinance 2001 and Sales Tax Act 1990.";
  } else if (category === "Consumer Protection Laws") {
    directAnswer += "Consumer grievances regarding defective goods or negligent services are filed in District Consumer Courts under provincial Consumer Protection Acts.";
  } else if (category === "Constitutional Laws") {
    directAnswer += "Fundamental rights are protected and enforced via writ petitions in the High Court under Article 199 of the Constitution of Pakistan.";
  } else {
    directAnswer += "Statutory regulations and relevant local laws govern the legal resolution of this matter.";
  }

  let nextSteps = "";
  if (category === "Family Laws") {
    nextSteps = "1. Gather supporting evidence (Nikahnama, CNIC of parties, children B-Form).\n2. Consult a family lawyer to draft a suit for maintenance, khula, or custody.\n3. File the suit in the local Family Court of the district where the wife resides.";
  } else if (category === "Criminal Laws") {
    nextSteps = "1. Visit the local police station (Thana) immediately to report the offense.\n2. Request the SHO to register a First Information Report (FIR) under Section 154 CrPC.\n3. If the police refuse to register the FIR, file a petition under Section 22-A/22-B CrPC before the Sessions Judge (Justice of Peace) to seek a court order directing the police to register the FIR.";
  } else if (category === "Civil Laws") {
    nextSteps = "1. Serve a written legal notice to the opposite party demanding compliance or settlement.\n2. If unresolved, consult a civil lawyer to draft a plaint (suit).\n3. File the suit (for specific performance, declaration, or injunction) in the competent Civil Court having jurisdiction.";
  } else if (category === "Property Laws") {
    nextSteps = "1. Obtain verified land registry/mutation documents from the Arazi Record Center (ARC) or Patwari.\n2. If facing illegal dispossession or land grabbing, file a petition under the Illegal Dispossession Act 2005 in the Sessions Court.\n3. For boundaries or partition disputes, file a partition suit in the Civil Court.";
  } else if (category === "Labour Laws") {
    nextSteps = "1. Serve a written grievance notice to the employer within 30 days under Section 25-A of the Industrial Relations Act.\n2. If the employer does not resolve the issue, file a petition in the Labour Court within 30 days.\n3. For delayed/unpaid wages, file an application before the Authority under the Payment of Wages Act.";
  } else if (category === "Tax Laws") {
    nextSteps = "1. Log into the FBR IRIS portal to file annual returns, or respond to FBR notices under Section 122.\n2. If aggrieved by an assessment amendment, file an appeal before the Commissioner Inland Revenue (Appeals) within 30 days.\n3. For further disputes, appeal before the Appellate Tribunal Inland Revenue (ATIR).";
  } else if (category === "Consumer Protection Laws") {
    nextSteps = "1. Draft and serve a mandatory 15-day written legal notice to the seller/manufacturer under Section 28 (demanding refund, replacement, or damages).\n2. Send the notice via registered post with acknowledgment due (AD) and keep the receipt.\n3. If unresolved after 15 days, file a formal complaint in the District Consumer Court within 30 days of the cause of action.";
  } else if (category === "Constitutional Laws") {
    nextSteps = "1. Consult a registered High Court Advocate to draft a Writ Petition under Article 199 of the Constitution.\n2. Specify the violation of fundamental rights or illegal actions of the public authority.\n3. File the petition in the High Court of the relevant province.";
  } else {
    nextSteps = "1. Consult an appropriate legal advocate specializing in this area.\n2. Review all relevant documents and contracts.\n3. File a claim or representation in the competent court or regulatory authority.";
  }

  let requiredDocs = "";
  if (category === "Family Laws") {
    requiredDocs = "Nikahnama (Marriage Contract), CNIC of parties, Children's B-Form, list of dowry articles, proof of husband's income.";
  } else if (category === "Criminal Laws") {
    requiredDocs = "Copy of the FIR (if registered), written complaint, medical report (in injury cases), CNIC, list of witnesses.";
  } else if (category === "Civil Laws") {
    requiredDocs = "Written agreement/contract, correspondence/notices exchanged, payment receipts, CNIC.";
  } else if (category === "Property Laws") {
    requiredDocs = "Registry deed, mutation (intiqal) document, Fard (ownership record), layout plan, CNIC.";
  } else if (category === "Labour Laws") {
    requiredDocs = "Appointment letter, salary slips, bank statements showing salary deposit, termination letter, copy of grievance notice.";
  } else if (category === "Tax Laws") {
    requiredDocs = "FBR tax returns, withholding tax certificates, bank statements, transaction invoices, show-cause notices received.";
  } else if (category === "Consumer Protection Laws") {
    requiredDocs = "Purchase receipt/cash memo, warranty card, copy of the served 15-day legal notice, courier/postage receipt of the notice.";
  } else if (category === "Constitutional Laws") {
    requiredDocs = "Copy of the illegal order or action being challenged, representations sent to authorities, CNIC, supporting affidavit.";
  } else {
    requiredDocs = "All relevant agreements, CNIC, and proof of dispute/transactions.";
  }

  const disclaimer = `Under Rule 7, this system provides legal information for educational purposes only. It does not constitute professional legal advice, court representation, or any legal guarantees.`;

  return `**Category (زمرہ)**: ${category}\n\n**Title**: ${title}\n\n**1. Direct Answer**:\n${directAnswer}\n\n**2. Relevant Pakistani Law**:\n${answerText} (Source: ${statute} - ${source})\n\n**3. Practical Next Steps**:\n${nextSteps}\n\n**4. Required Documents**:\n${requiredDocs}\n\n**5. Important Notes**:\n${disclaimer}`;
}

const LOCAL_TRANSLATIONS: Record<string, Record<string, string>> = {
  "Constitutional Laws": {
    "ur": `**Category (زمرہ)**: Constitutional Laws

**Title**: بنیادی حقوق اور ہائی کورٹ کی رٹ پٹیشنز

**Direct Answer**:
دستورِ پاکستان کے آئینی قوانین کے تحت آپ کا سوال بنیادی حقوق کے تحفظ اور آرٹیکل 199 کے تحت ان کے نفاذ سے متعلق ہے۔

**Relevant Legal Information**:
دستورِ پاکستان 1973 کے تحت، آرٹیکل 9 شہریوں کی جان و آزادی کا تحفظ فراہم کرتا ہے، آرٹیکل 10-A منصفانہ ٹرائل کا حق دیتا ہے، آرٹیکل 19 آزادیِ اظہارِ رائے کی ضمانت دیتا ہے، اور آرٹیکل 25 قانون کی نظر میں تمام شہریوں کی برابری کی ضمانت دیتا ہے۔ آرٹیکل 199 کے تحت اگر سرکاری حکام بنیادی حقوق کی خلاف ورزی کریں تو شہری ہائیکورٹ میں آئینی رٹ پٹیشن (جیسے حبسِ بے جا یا حکمِ امتناعی) دائر کر سکتے ہیں۔

**Important Notes**:
1. **حفاظتی دستبرداری**: رول 7 کے تحت یہ نظام تعلیمی مقاصد کے لیے معلومات فراہم کرتا ہے اور پیشہ ورانہ قانونی مشورہ کا متبادل نہیں ہے۔
2. **طریقہ کار**: آئینی مقدمات پیچیدہ ہوتے ہیں۔ اپنی رٹ پٹیشن تیار کرنے اور پیش کرنے کے لیے ہائیکورٹ کے مستند وکیل سے رجوع کریں۔

**Source Document**: دستورِ پاکستان، 1973 (حصہ دوم اور آرٹیکل 199)`,
    "roman": `**Category (زمرہ)**: Constitutional Laws

**Title**: Bunyadi Huqooq aur High Court ki Writ Petitions

**Direct Answer**:
Aap ka sawal Pakistan ke aaeeni qawaneen, bunyadi huqooq aur Article 199 ke tehat writ petition ke nafadh se mutalliq hai.

**Relevant Legal Information**:
Constitution of Pakistan 1973 ke tehat, Article 9 jaan aur azaadi ka tahaffuz deta hai, Article 10A fair trial ka haq deta hai, Article 19 freedom of speech ki guarantee deta hai, aur Article 25 sab shehriyon ki barabri ka haq deta hai. Article 199 ke tehat agar sarkari idaray aap ke bunyadi huqooq ko violate karein, to aap High Court mein writ petition (Habeas Corpus, Mandamus) file kar sakte hain.

**Important Notes**:
1. **Safety Disclaimer**: Under Rule 7, yeh system sirf educational purposes ke liye legal information deta hai. Yeh professional advice ya legal guarantee nahi hai.
2. **Procedural Action**: Aaeeni mamlat ke liye High Court ke registered lawyer se consult karein taake wo proper petition draft kar sakein.

**Source Document**: Constitution of the Islamic Republic of Pakistan, 1973 (Part II & Article 199)`
  },
  "Family Laws": {
    "ur": `**Category (زمرہ)**: Family Laws

**Title**: خاندانی قوانین: شادی، طلاق، خلع اور بچوں کی کسٹڈی

**Direct Answer**:
پاکستان کے خاندانی قوانین کے تحت آپ کا سوال مسلم فیملی لاز آرڈیننس 1961 اور گارڈینز اینڈ وارڈز ایکٹ 1890 کے تحت حل ہوتا ہے۔

**Relevant Legal Information**:
مسلم فیملی لاز آرڈیننس (MFLO) 1961 کے تحت، شوہر کے لیے دوسری شادی کرنے سے پہلے پہلی بیوی اور ثالثی کونسل سے تحریری اجازت لینا لازمی ہے (دفعہ 6)۔ طلاق کی صورت میں شوہر یونین کونسل کو نوٹس دینے کا پابند ہے اور طلاق 90 دن کی عدت کے بعد مؤثر ہوتی ہے (دفعہ 7)۔ بیوی فیملی کورٹ سے خلع کا دعویٰ دائر کر سکتی ہے۔ بچوں کی تحویل اور سرپرستی گارڈینز اینڈ وارڈز ایکٹ 1890 کے تحت بچے کی فلاح و بہبود کے اصول پر طے ہوتی ہے۔ شوہر بیوی اور بچوں کو نان و نفقہ دینے کا پابند ہے (دفعہ 9)۔

**Important Notes**:
1. **حفاظتی دستبرداری**: رول 7 کے تحت یہ نظام تعلیمی مقاصد کے لیے معلومات فراہم کرتا ہے اور پیشہ ورانہ قانونی مشورہ کا متبادل نہیں ہے۔
2. **طریقہ کار**: نان و نفقہ، حق مہر، اور بچوں کی کسٹڈی کے مقدمات فیملی کورٹ میں دائر کیے جاتے ہیں۔ نکاح نامہ کی شرائط کو بغور پر کریں۔

**Source Document**: مسلم فیملی لاز آرڈیننس، 1961 اور گارڈینز اینڈ وارڈز ایکٹ، 1890`,
    "roman": `**Category (زمرہ)**: Family Laws

**Title**: Khandani Qawaneen: Shadi, Talaq, Khula aur Custody

**Direct Answer**:
Aap ka family law se mutalliq sawal Muslim Family Laws Ordinance 1961 aur Guardians and Wards Act 1890 ke tehat hal hota hai.

**Relevant Legal Information**:
Muslim Family Laws Ordinance (MFLO) 1961 ke Section 6 ke tehat, shohar pehli biwi aur Arbitration Council ki written consent ke baghair doosri shadi nahi kar sakta. Section 7 ke tehat Talaq dene ke baad Union Council ko written notice bhejna aur 90 days iddat guzarna lazmi hai. Biwi court se Khula le sakti hai. Bachon ki custody Guardians and Wards Act 1890 ke tehat bachay ki welfare ke mutabiq tay hoti hai. Shohar par biwi aur bachon ka monthly kharcha (maintenance) dena lazmi hai (Section 9).

**Important Notes**:
1. **Safety Disclaimer**: Under Rule 7, yeh system sirf educational purposes ke liye legal information deta hai. Yeh professional advice ya legal guarantee nahi hai.
2. **Procedural Action**: Kharcha, Haq Mehr, aur custody ke suits Family Court mein file kiye jaate hain. Nikahnama ke columns ko dhyan se check karein.

**Source Document**: Muslim Family Laws Ordinance, 1961 & Guardians and Wards Act, 1890`
  },
  "Criminal Laws": {
    "ur": `**Category (زمرہ)**: Criminal Laws

**Title**: ایف آئی آر کی رجسٹریشن، گرفتاری، ضمانت اور تعزیراتی سزائیں

**Direct Answer**:
آپ کا فوجداری قانون کا سوال تعزیراتِ پاکستان 1860 اور ضابطہ فوجداری 1898 کے دائرہ اختیار میں آتا ہے۔

**Relevant Legal Information**:
دفعہ 154 ضابطہ فوجداری کے تحت پولیس قابل دست اندازی جرائم کی ایف آئی آر (FIR) درج کرنے کی پابند ہے۔ اگر ایس ایچ او انکار کرے تو دفعہ 22-A/22-B کے تحت سیشن جج (جسٹس آف پیس) کو درخواست دی جا سکتی ہے۔ ضمانت کی درخواستیں دفعہ 496 (قابلِ ضمانت)، 497 (ناقابلِ ضمانت) اور 498 (قبل از گرفتاری حفاظتی ضمانت) کے تحت دائر کی جاتی ہیں۔ تعزیراتِ پاکستان (PPC) کے تحت چوری کی سزا دفعہ 379 (تین سال تک قید)، جائیداد کو نقصان پہنچانے کی سزا دفعہ 427 اور جعل سازی کی سزا دفعہ 468 کے تحت مقرر ہے۔

**Important Notes**:
1. **حفاظتی دستبرداری**: رول 7 کے تحت یہ نظام تعلیمی مقاصد کے لیے معلومات فراہم کرتا ہے اور پیشہ ورانہ قانونی مشورہ کا متبادل نہیں ہے۔
2. **طریقہ کار**: گرفتاری کی صورت میں پولیس ملزم کو 24 گھنٹے کے اندر مجسٹریٹ کے سامنے پیش کرنے کی پابند ہے (دفعہ 61)۔ ایف آئی آر کی مصدقہ نقل حاصل کریں اور فوجداری وکیل سے رجوع کریں۔

**Source Document**: تعزیراتِ پاکستان (PPC) 1860 اور ضابطہ فوجداری (CrPC) 1898`,
    "roman": `**Category (زمرہ)**: Criminal Laws

**Title**: FIR Registration, Arrest, Bail aur Penal Code Actions

**Direct Answer**:
Aap ka criminal law ka sawal Pakistan Penal Code 1860 aur Code of Criminal Procedure 1898 ke tehat aata hai.

**Relevant Legal Information**:
Section 154 CrPC ke tehat police cognizable offenses ki FIR register karne ki paband hai. Agar SHO mana kare to Section 22-A/22-B CrPC ke tehat Sessions Judge (Justice of Peace) ke paas complaint ki ja sakti hai. Bail applications Section 496, 497, aur 498 (pre-arrest protective bail) ke tehat file hoti hain. PPC ke tehat Theft (Section 378/379), Mischief (Section 427), aur Forgery (Section 468) ke liye specific punishments hain.

**Important Notes**:
1. **Safety Disclaimer**: Under Rule 7, yeh system sirf educational purposes ke liye legal information deta hai. Yeh professional advice ya legal guarantee nahi hai.
2. **Procedural Action**: Arrest hone par police ko 24 hours ke andar accused ko magistrate ke samnay pesh karna zaroori hai (Section 61). FIR ki copy hasil karein aur criminal defense advocate se consult karein.

**Source Document**: Pakistan Penal Code (PPC), 1860 & Code of Criminal Procedure (CrPC), 1898`
  },
  "Civil Laws": {
    "ur": `**Category (زمرہ)**: Civil Laws

**Title**: مخصوص دادرسی، حکمِ امتناعی (سٹے آرڈر)، اور معاہدوں کا قانون

**Direct Answer**:
پاکستان کے دیوانی قوانین کے تحت آپ کا سوال مخصوص دادرسی ایکٹ 1877 اور معاہدہ ایکٹ 1872 کے تحت حل ہوتا ہے۔

**Relevant Legal Information**:
مخصوص دادرسی ایکٹ 1877 کے تحت، اگر کسی شخص کو مرضی کے بغیر جائیداد سے بے دخل کیا جائے تو وہ 6 ماہ کے اندر قبضہ کی بحالی کا دعویٰ دائر کر سکتا ہے (دفعہ 9)۔ دفعہ 12 کے تحت معاہدوں کی مخصوص تعمیل کروائی جا سکتی ہے۔ دفعہ 42 کے تحت اعلانیہ دعویٰ (ڈیکلریٹری سوٹ) دائر کیا جاتا ہے تاکہ مالکانہ حقوق یا قانونی حیثیت کا اعلان کروایا جا سکے۔ دفعہ 54 کے تحت حکمِ امتناعی (سٹے آرڈر) جاری کیا جاتا ہے۔ معاہدہ ایکٹ 1872 کے تحت، معاہدے کے لیے آزاد رضامندی (دفعہ 10) لازمی ہے اور معاہدے کی خلاف ورزی پر ہرجانے (دفعہ 73) کا دعویٰ کیا جا سکتا ہے۔

**Important Notes**:
1. **حفاظتی دستبرداری**: رول 7 کے تحت یہ نظام تعلیمی مقاصد کے لیے معلومات فراہم کرتا ہے اور پیشہ ورانہ قانونی مشورہ کا متبادل نہیں ہے۔
2. **طریقہ کار**: دیوانی مقدمات سول عدالتوں میں دائر کیے جاتے ہیں۔ مقدمہ بازی سے پہلے فریق مخالف کو باضابطہ قانونی نوٹس بھیجیں۔

**Source Document**: مخصوص دادرسی ایکٹ، 1877 اور معاہدہ ایکٹ، 1872`,
    "roman": `**Category (زمرہ)**: Civil Laws

**Title**: Specific Relief, Stay Orders, aur Contract Act Rules

**Direct Answer**:
Aap ka civil law ka sawal Specific Relief Act 1877 aur Contract Act 1872 ke tehat hal hota hai.

**Relevant Legal Information**:
Specific Relief Act 1877 ke Section 9 ke tehat, agar kisi ko property se be-dakhal kiya jaye to wo 6 months ke andar possession bahal karwane ka suit dalk sakta hai. Section 12 ke tehat contract ki specific performance claim ki ja sakti hai. Section 42 ke tehat declaratory suit file hota hai. Injunctions (stay orders) Section 54 ke tehat issue hote hain. Contract Act 1872 ke mutabiq, breach of contract par damages (Section 73) claim kiye ja sakte hain.

**Important Notes**:
1. **Safety Disclaimer**: Under Rule 7, yeh system sirf educational purposes ke liye legal information deta hai. Yeh professional advice ya legal guarantee nahi hai.
2. **Procedural Action**: Civil disputes Civil Court mein file hote hain. Legal action se pehle proper written legal notice send karna advisable hai.

**Source Document**: Specific Relief Act, 1877 & Contract Act, 1872`
  },
  "Property Laws": {
    "ur": `**Category (زمرہ)**: Property Laws

**Title**: انتقالِ جائیداد، ہبہ نامہ (تحفہ)، اور غیر قانونی قبضے کے خلاف دادرسی

**Direct Answer**:
پاکستان کے جائیداد کے قوانین کے تحت آپ کا تنازعہ ٹرانسفر آف پراپرٹی ایکٹ 1882، رجسٹریشن ایکٹ 1908، اور الیگل ڈسپوزیشن ایکٹ 2005 کے تحت آتا ہے۔

**Relevant Legal Information**:
ٹرانسفر آف پراپرٹی ایکٹ 1882 کے تحت جائیداد کی فروخت کے لیے رجسٹرڈ سیل ڈیڈ لازمی ہے (دفعہ 54)۔ ہبہ (تحفے) کے لیے تحریر، قبولیت، اور جائیداد کا قبضہ منتقل کرنا لازمی ہے (دفعہ 122)۔ پٹواری نظام میں جائیداد کے ریکارڈ فرد اور انتقال (Mutation) کے ذریعے رکھے جاتے ہیں۔ قبضہ مافیا کے خلاف الیگل ڈسپوزیشن ایکٹ 2005 کے تحت سیشن کورٹ میں براہِ راست شکایت درج کی جا سکتی ہے، جہاں عدالت پولیس کو فوری قبضہ بحال کرنے اور قبضہ کرنے والوں کو 10 سال تک قید کی سزا دینے کا اختیار رکھتی ہے۔

**Important Notes**:
1. **حفاظتی دستبرداری**: رول 7 کے تحت یہ نظام تعلیمی مقاصد کے لیے معلومات فراہم کرتا ہے اور پیشہ ورانہ قانونی مشورہ کا متبادل نہیں ہے۔
2. **طریقہ کار**: جائیداد خریدنے سے پہلے اراضی ریکارڈ سینٹر (ARC) یا سب رجسٹرار آفس سے فرد اور رجسٹری کی تصدیق کریں۔ زبانی سودے کی کوئی قانونی حیثیت نہیں ہے۔

**Source Document**: ٹرانسفر آف پراپرٹی ایکٹ، 1882 اور الیگل ڈسپوزیشن ایکٹ، 2005`,
    "roman": `**Category (زمرہ)**: Property Laws

**Title**: Transfer of Property, Gift Deeds (Hiba), aur Illegal Qabza Remedies

**Direct Answer**:
Property disputes, Hiba, aur illegal qabza ke khilaf action Transfer of Property Act 1882 aur Illegal Dispossession Act 2005 ke tehat aata hai.

**Relevant Legal Information**:
Transfer of Property Act 1882 ke Section 54 ke tehat property sale ke liye registered deed lazmi hai. Gift deed (Hiba) ke liye Section 122 ke mutabiq donor ki taraf se property ka physical possession hand over karna zaroori hai. Qabza mafia aur land grabbing ke khilaf Illegal Dispossession Act 2005 ke tehat Sessions Court mein direct complaint file ki ja sakti hai, jahan court immediate restoration (Section 8) ka order de sakti hai.

**Important Notes**:
1. **Safety Disclaimer**: Under Rule 7, yeh system sirf educational purposes ke liye legal information deta hai. Yeh professional advice ya legal guarantee nahi hai.
2. **Procedural Action**: Property purchase karne se pehle Arazi Record Center se Fard aur Mutation (Intiqal) verify karein. Oral property deals invalid hote hain.

**Source Document**: Transfer of Property Act, 1882 & Illegal Dispossession Act, 2005`
  },
  "Labour Laws": {
    "ur": `**Category (زمرہ)**: Labour Laws

**Title**: تنخواہوں کی ادائیگی، شرائطِ ملازمت اور لیبر کورٹ کی کارروائی

**Direct Answer**:
ملازمت کے تنازعات، تنخواہوں میں تاخیر، اور برطرفی پیمنٹ آف ویجز ایکٹ 1936 اور اسٹینڈنگ آرڈرز آرڈیننس 1968 کے تحت حل ہوتے ہیں۔

**Relevant Legal Information**:
پیمنٹ آف ویجز ایکٹ 1936 کے سیکشن 5 کے تحت آجر (Employer) تنخواہ مقررہ وقت پر ادا کرنے کا پابند ہے۔ تنخواہ میں تاخیر یا کٹوتی کو لیبر کمشنر کے پاس سیکشن 15 کے تحت چیلنج کیا جا سکتا ہے۔ اسٹینڈنگ آرڈر 12 کے تحت مستقل ملازم کو برطرف کرنے کے لیے ایک ماہ کا تحریری نوٹس یا تنخواہ دینا اور گریجویٹی (ہر سال کے بدلے 30 دن کی بنیادی تنخواہ) ادا کرنا لازم ہے۔ بدتمیزی یا کوتاہی پر نوکری سے نکالنے سے پہلے شوکاز نوٹس اور آزادانہ انکوائری لازم ہے (اسٹینڈنگ آرڈر 15)۔

**Important Notes**:
1. **حفاظتی دستبرداری**: رول 7 کے تحت یہ نظام تعلیمی مقاصد کے لیے معلومات فراہم کرتا ہے اور پیشہ ورانہ قانونی مشورہ کا متبادل نہیں ہے۔
2. **طریقہ کار**: غیر قانونی برطرفی کی صورت میں ملازم کو 30 دن کے اندر اپنے آجر کو تحریری شکایت بھیجنی ہوتی ہے اور لیبر کورٹ سے رجوع کرنا ہوتا ہے۔ اپنا تقرری خط محفوظ رکھیں۔

**Source Document**: پیمنٹ آف ویجز ایکٹ، 1936 اور اسٹینڈنگ آرڈرز آرڈیننس، 1968`,
    "roman": `**Category (زمرہ)**: Labour Laws

**Title**: Payment of Wages, Gratuity, aur Labor Court Grievance

**Direct Answer**:
Labor aur employment disputes Payment of Wages Act 1936 aur Standing Orders Ordinance 1968 ke tehat hal hote hain.

**Relevant Legal Information**:
Wages Act ke Section 5 ke tehat employer salary waqt par dene ka paband hai. Agar delayed salary ya unauthorized deduction ho to Section 15 ke tehat Labor Commissioner ke paas case file ho sakta hai. Standing Order 12 ke tehat permanent worker ki termination par 1-month notice aur gratuity (30 days basic pay per year) lazmi hai. Dismissal for misconduct se pehle show-cause aur inquiry mandatory hai (Order 15).

**Important Notes**:
1. **Safety Disclaimer**: Under Rule 7, yeh system sirf educational purposes ke liye legal information deta hai. Yeh professional advice ya legal guarantee nahi hai.
2. **Procedural Action**: Labor Court jaane se pehle employer ko written grievance notice bhejna zaroori hai. Employment contract aur salary slips ka record save rakhein.

**Source Document**: Payment of Wages Act, 1936 & Standing Orders Ordinance, 1968`
  },
  "Tax Laws": {
    "ur": `**Category (زمرہ)**: Tax Laws

**Title**: انکم ٹیکس ریٹرن، ایف بی آر اسیسمنٹس اور ٹیکس اپیلیں

**Direct Answer**:
ٹیکس کے معاملات، ریٹرن فائلنگ، اور ایف بی آر اسیسمنٹس انکم ٹیکس آرڈیننس 2001 اور سیلز ٹیکس ایکٹ 1990 کے تحت حل ہوتے ہیں۔

**Relevant Legal Information**:
انکم ٹیکس آرڈیننس 2001 کے سیکشن 114 کے تحت ہر وہ شخص جس کی آمدنی ٹیکس کی حد سے زیادہ ہو، سالانہ ریٹرن فائل کرنے کا پابند ہے۔ فائل کردہ ریٹرن اسیسمنٹ مانی جاتی ہے (سیکشن 120) لیکن ایف بی آر کمشنر شوکاز نوٹس جاری کر کے اسیسمنٹ میں ترمیم کر سکتا ہے (سیکشن 122)۔ دیر سے ادائیگی پر ڈیفالٹ سرچارج عائد ہوتا ہے (سیکشن 205)۔ سیلز ٹیکس ایکٹ 1990 کے سیکشن 3 کے تحت سپلائیز پر 18 فیصد سیلز ٹیکس وصول کیا جاتا ہے۔ ٹیکس کے فیصلوں کے خلاف اپیلیں کمشنر اپیل اور پھر اپیلٹ ٹریبیونل (ATIR) میں دائر ہوتی ہیں۔

**Important Notes**:
1. **حفاظتی دستبرداری**: رول 7 کے تحت یہ نظام تعلیمی مقاصد کے لیے معلومات فراہم کرتا ہے اور پیشہ ورانہ قانونی مشورہ کا متبادل نہیں ہے۔
2. **طریقہ کار**: فائلر بننے سے ودہولڈنگ ٹیکس کی شرح آدھی ہو جاتی ہے۔ ایف بی آر کے کسی بھی نوٹس کا 15 دن کے اندر تحریری جواب دیں اور اپنے بینک سٹیٹمنٹس کا ریکارڈ رکھیں۔

**Source Document**: انکم ٹیکس آرڈیننس، 2001 اور سیلز ٹیکس ایکٹ، 1990`,
    "roman": `**Category (زمرہ)**: Tax Laws

**Title**: Income Tax return FBR Audit, aur Sales Tax appeals

**Direct Answer**:
Tax matters, income tax return filing, aur FBR audits Income Tax Ordinance 2001 aur Sales Tax Act 1990 ke tehat aate hain.

**Relevant Legal Information**:
Section 114 Income Tax Ordinance ke tehat taxable income limits cross hone par annual tax return file karna zaroori hai. FBR Commissioner Section 122 ke tehat show-cause notice de kar assessment order amend kar sakta hai. Late tax payment par Section 205 ke tehat default surcharge lagta hai. Sales Tax Act 1990 ke Section 3 ke tehat standard sales tax 18% hai. Tax disputes ki appeals CIR (Appeals) aur ATIR mein file hoti hain.

**Important Notes**:
1. **Safety Disclaimer**: Under Rule 7, yeh system sirf educational purposes ke liye legal information deta hai. Yeh professional advice ya legal guarantee nahi hai.
2. **Procedural Action**: Tax filer banne se withholding tax rates kam hote hain. Audit compliance ke liye transaction records 6 years tak save rakhein.

**Source Document**: Income Tax Ordinance, 2001 & Sales Tax Act, 1990`
  },
  "Consumer Protection Laws": {
    "ur": `**Category (زمرہ)**: Consumer Protection Laws

**Title**: ناقص اشیاء، ناقص خدمات اور کنزیومر عدالتیں

**Direct Answer**:
ناقص اشیاء، آن لائن فراڈ اور ناقص سروسز کے خلاف شکایات صوبائی کنزیومر پروٹیکشن ایکٹ (جیسے پنجاب کنزیومر پروٹیکشن ایکٹ 2005) کے تحت حل ہوتی ہیں۔

**Relevant Legal Information**:
پنجاب کنزیومر پروٹیکشن ایکٹ 2005 کے سیکشن 13 کے تحت مینوفیکچرر یا دکاندار ناقص مصنوعات اور ناقص خدمات کے لیے ذمہ دار ہے۔ دعویٰ دائر کرنے سے پہلے دکاندار کو سیکشن 28 کے تحت 15 روزہ تحریری قانونی نوٹس بھیجنا لازمی ہے۔ اگر نوٹس کا جواب نہ ملے یا مسئلہ حل نہ ہو تو 30 دن کے اندر کنزیومر کورٹ میں کیس دائر کیا جا سکتا ہے۔ کنزیومر کورٹ مصنوعات کی واپسی، قیمت کی واپسی اور ذہنی اذیت کے نقصانات (سیکشن 21) کی دگری دے سکتی ہے۔

**Important Notes**:
1. **حفاظتی دستبرداری**: رول 7 کے تحت یہ نظام تعلیمی مقاصد کے لیے معلومات فراہم کرتا ہے اور پیشہ ورانہ قانونی مشورہ کا متبادل نہیں ہے۔
2. **طریقہ کار**: کنزیومر کورٹ میں دعویٰ دائر کرنے کے لیے کوئی فیس نہیں ہے اور آپ بغیر وکیل کے بھی اپنا کیس لڑ سکتے ہیں۔ خریداری کی رسید اور قانونی نوٹس کی رسید ہمیشہ سنبھال کر رکھیں۔

**Source Document**: پنجاب کنزیومر پروٹیکشن ایکٹ، 2005 (یا دیگر صوبائی مساوی قوانین)`,
    "roman": `**Category (زمرہ)**: Consumer Protection Laws

**Title**: Defective products, online store fraud aur Consumer Courts

**Direct Answer**:
Defective products ya poor services ke khilaf complaints provincial Consumer Protection Acts (e.g. Punjab Consumer Protection Act 2005) ke tehat aati hain.

**Relevant Legal Information**:
Section 13 Punjab Consumer Protection Act ke tehat manufacturer/seller defective goods ya deficient services ke liye liable hai. Section 28 ke tehat suit file karne se pehle seller ko 15-day written legal notice bhejna mandatory hai. Agar response na aye, to 30 days ke andar Consumer Court mein complaint file ki ja sakti hai. Court refund, replacement aur mental agony ke liye damages (Section 21) de sakti hai.

**Important Notes**:
1. **Safety Disclaimer**: Under Rule 7, yeh system sirf educational purposes ke liye legal information deta hai. Yeh professional advice ya legal guarantee nahi hai.
2. **Procedural Action**: Consumer Court mein case file karne ke liye koi fees nahi hoti aur aap self-represent kar sakte hain. Purchase receipt aur legal notice ka record save rakhein.

**Source Document**: Punjab Consumer Protection Act, 2005`
  }
};

export async function POST(request: NextRequest) {
  try {
    const { message, category: categoryFocus } = await request.json();
    if (!message || !message.trim()) {
      return NextResponse.json({ error: "Query message cannot be blank." }, { status: 400 });
    }

    const { dataset, bm25, idToIndex } = getDatasetAndIndex();
    if (!dataset || dataset.length === 0) {
      return NextResponse.json({ error: "Legal dataset is unavailable." }, { status: 500 });
    }

    // Clean text input
    const cleanedMessage = cleanText(message);

    // 1. Detect language of the input query
    const lang = detectLanguage(cleanedMessage);

    // 2. Translate query to English to handle Urdu script, Roman Urdu, and mixed English/Roman Urdu inputs
    let searchQuery = cleanedMessage;
    if (lang === 'urdu_script') {
      searchQuery = await translateText(cleanedMessage, 'ur', 'en');
    } else {
      searchQuery = await translateText(cleanedMessage, 'auto', 'en');
    }

    // If query translation failed (remained in Urdu or Roman), we can extract search keywords manually
    // or let it use targetCategory lock to search.
    searchQuery = cleanText(searchQuery);

    const isTranslationFailed = (lang === 'urdu_script' && searchQuery === cleanedMessage) ||
                                 (lang === 'roman_urdu' && searchQuery === cleanedMessage);

    if (isTranslationFailed) {
      const tokens = cleanedMessage.toLowerCase()
        .replace(/[^\p{L}\p{N}\s]/gu, ' ')
        .split(/\s+/)
        .filter(w => w);
      
      const translatedWords: string[] = [];
      for (const token of tokens) {
        if (LOCAL_DICTIONARY[token]) {
          translatedWords.push(LOCAL_DICTIONARY[token]);
        }
      }
      
      if (translatedWords.length > 0) {
        searchQuery += " " + translatedWords.join(" ");
      }
    }

    // Preserve key Roman Urdu legal keywords that are often lost or mistranslated by Google Translate
    const originalWords = cleanedMessage.toLowerCase().split(/\s+/);
    const searchWords = new Set(searchQuery.toLowerCase().split(/\s+/));
    const legalKeywordsToPreserve = [
      "khula", "talaq", "talaaq", "nikah", "nikaah", "shadi", "shaadi", "qabza", "patwari", "fard", "wirasat", 
      "intiqal", "fir", "sho", "thana", "gratuity", "eobi", "pessi", "sessi", "fbr", "naqis", "raseed"
    ];
    for (const kw of legalKeywordsToPreserve) {
      if (originalWords.includes(kw) && !searchWords.has(kw)) {
        searchQuery += " " + kw;
      }
    }

    // 3. Classify Category of the input query on both original message and translated query to maximize keyword matching accuracy
    const classified = classify(cleanedMessage + " " + searchQuery);

    const frontendCategoryMap: Record<string, string> = {
      "General": "Constitutional Laws",
      "Family Laws": "Family Laws",
      "Criminal Laws": "Criminal Laws",
      "Civil Laws": "Civil Laws",
      "Property Laws": "Property Laws",
      "Labour Laws": "Labour Laws",
      "Tax Laws": "Tax Laws",
      "Consumer Protection Laws": "Consumer Protection Laws",
      "Constitutional Laws": "Constitutional Laws",
      // Legacy compatibility
      "Family Law": "Family Laws",
      "Cyber Crime": "Criminal Laws",
      "Property Law": "Property Laws",
      "Tenant Rights": "Property Laws",
      "Consumer Rights": "Consumer Protection Laws",
      "Employment Law": "Labour Laws",
      "FIR & Police Complaints": "Criminal Laws",
      "Women Protection Laws": "Family Laws"
    };

    let targetCategory = classified.category;
    if (categoryFocus && categoryFocus in frontendCategoryMap) {
      targetCategory = frontendCategoryMap[categoryFocus];
    }
                                 
    if (categoryFocus && targetCategory && classified.category !== targetCategory && classified.maxScore > 0 && !isTranslationFailed) {
      let lockReply = "This question belongs to another legal category. Please switch to the appropriate category to receive an accurate answer.";
      
      if (lang === 'urdu_script') {
        lockReply = await translateText(lockReply, 'en', 'ur');
        if (lockReply === "This question belongs to another legal category. Please switch to the appropriate category to receive an accurate answer.") {
          lockReply = "یہ سوال کسی دوسری قانونی کیٹیگری سے تعلق رکھتا ہے۔ درست جواب حاصل کرنے کے لیے براہ کرم مناسب کیٹیگری پر جائیں۔";
        }
      } else if (lang === 'roman_urdu') {
        lockReply = "Yeh sawal kisi doosri qanooni category se talluq rakhta hai. Sahi jawab ke liye baraye meherbani mutalliga category select karein.";
      }

      return NextResponse.json({
        category: classified.category,
        reply: lockReply,
        sources: ["System Category Lock"],
        disclaimer: "This AI system provides informational legal guidance only and is not a substitute for professional legal advice."
      });
    }

    // Filter dataset for current category to enforce category retrieval
    const subRecords = dataset.filter(r => r.category === targetCategory);
    
    if (subRecords.length === 0) {
      let notFoundReply = "Information not found in the selected legal knowledge base.";
      if (lang === 'urdu_script') {
        notFoundReply = await translateText(notFoundReply, 'en', 'ur');
        if (notFoundReply === "Information not found in the selected legal knowledge base.") {
          notFoundReply = "منتخب کردہ قانونی معلومات کے ذخیرے میں معلومات نہیں مل سکیں۔";
        }
      } else if (lang === 'roman_urdu') {
        notFoundReply = "Selected legal knowledge base mein malomat nahi mil saki.";
      }
      return NextResponse.json({
        category: targetCategory,
        reply: notFoundReply,
        sources: ["Dataset Boundary"],
        disclaimer: "This AI system provides informational legal guidance only and is not a substitute for professional legal advice."
      });
    }

    // 5. Multi-Query Retrieval and Query Expansion
    // Identify trigger expansions
    const expansions = getQueryExpansions(cleanedMessage + " " + searchQuery);
    
    // Build search queries (Original query + combined expansions to keep it grounded in context)
    const searchQueries = [searchQuery];
    if (expansions.length > 0) {
      searchQueries.push(searchQuery + " " + expansions.join(" "));
    }

    // Track maximum score for each record across all queries
    const recordScores: Record<string, { record: any; score: number }> = {};
    for (const r of subRecords) {
      recordScores[r.id] = { record: r, score: 0.0 };
    }

    for (const q of searchQueries) {
      const qClean = cleanText(q);
      if (!qClean.trim()) continue;
      const queryTokens = bm25.tokenize(qClean);

      for (const record of subRecords) {
        const globalIdx = idToIndex.get(record.id);
        const score = (globalIdx !== undefined && globalIdx !== -1) ? bm25.getScore(queryTokens, globalIdx) : 0.0;
        if (score > recordScores[record.id].score) {
          recordScores[record.id].score = score;
        }
      }
    }

    const scoredRecords = Object.values(recordScores);
    // Rank candidates by BM25 relevance score
    scoredRecords.sort((a, b) => b.score - a.score);
    const bestMatch = scoredRecords[0];

    // 5.5 Relevance Guard (Intercept completely irrelevant/out-of-scope non-legal queries)
    const textLower = searchQuery.toLowerCase();
    const origTextLower = cleanedMessage.toLowerCase();
    
    // Legal indicators tested on the original raw message to ensure keywords are not lost in translation
    const hasUrduLegalTerm = /[\u0600-\u06FF]/.test(origTextLower) && 
      /(قانون|عدالت|طلاق|خلع|نکاح|شادی|پولیس|ایف\s*آئی\s*آر|جائیداد|زمین|حقوق|کیس|عدت|وکیل|ضمانت|سزا|جرم|معاہدہ|نان\s*و\s*نفقہ|رہن|پٹہ|تقسیم|بےنامی|سٹامپ|حکم\s*امتناعی|منسوخی|داوا|تنخواہ|ملازمت|نوکری|لیبر|پنشن|یونین|زچگی|سوشل\s*سیکیورٹی|ٹیکس|کسٹمز|انکم\s*ٹیکس|سیس|آڈٹ|جرمانہ|صارف|کنزیومر|وارنٹی|شکایت|ہرجانہ|ناقص|غیر\s*معیاری|غفلت|رسید|بل|اوورچارجنگ|زیادہ\s*قیمت|گمراہ\s*کن|نوٹس|فضول)/.test(origTextLower);
      
    const hasRomanLegalTerm = (lang === 'roman_urdu' || lang === 'english') && 
      /\b(qanoon|kanoon|talaq|talaaq|khula|nikah|nikaah|shadi|shaadi|adalat|masla|case|court|law|police|fir|bail|property|zameen|zameeni|qabza|tax|fbr|salary|employer|employee|rights|contract|stay|injunction|gratuity|wages|accident|theft|murder|arrest|void|guarantee|agency|surety|bailment|pledge|cpc|plaint|written|summons|decree|appeal|review|revision|limitation|mortgage|lease|partition|benami|easement|maternity|pessi|sessi|eobi|overtime|safety|union|cba|dismissal|misconduct|workplace|pension|resignation|labor|lebar|withholding|wht|audit|assessment|surcharge|atl|customs|excise|provincial|cgt|filer|non-filer|adrc|pra|srb|kpra|bra|defective|warranty|substandard|negligence|receipt|invoice|overcharging|misleading|notice|frivolous)\b/i.test(origTextLower);

    const isUrduQuery = /[\u0600-\u06FF]/.test(textLower);
    
    let isIrrelevant = false;
    
    if (isTranslationFailed) {
      // Offline fallback: check if the raw query contains any known legal terms in their respective script/romanization
      if (isUrduQuery) {
        isIrrelevant = !hasUrduLegalTerm;
      } else {
        isIrrelevant = !hasRomanLegalTerm;
      }
    } else {
      isIrrelevant = (classified.maxScore === 0 && (!bestMatch || bestMatch.score < 0.2));
      
      // Override: if the raw original message has a known Roman or Urdu legal term, it is relevant!
      if (isIrrelevant && (hasRomanLegalTerm || hasUrduLegalTerm)) {
        isIrrelevant = false;
      }
    }

    if (isIrrelevant) {
      let irrelevantReply = "I am sorry, but I can only assist with Pakistani legal matters. Please ask a question related to Pakistani laws or select one of the legal categories.";
      let localizedDisclaimer = "This AI system provides informational legal guidance only and is not a substitute for professional legal advice.";
      
      if (lang === 'urdu_script') {
        irrelevantReply = "معذرت، میں صرف پاکستانی قانونی معاملات میں مدد کر سکتا ہوں۔ براہ کرم پاکستانی قوانین سے متعلق سوال پوچھیں یا کسی قانونی کیٹیگری کا انتخاب کریں۔";
        localizedDisclaimer = "یہ اے آئی سسٹم صرف معلوماتی قانونی رہنمائی فراہم کرتا ہے اور پیشہ ورانہ قانونی مشورے کا متبادل نہیں ہے۔";
      } else if (lang === 'roman_urdu') {
        irrelevantReply = "Maazrat, mein sirf Pakistani qanooni mamlat mein madad kar sakta hoon. Baraye meherbani Pakistani qanoon se mutalliq sawal poochein.";
        localizedDisclaimer = "Yeh AI system sirf malomati kanooni rehnumai faraham karta hai aur peshawarana kanooni mashwaray ka badal nahi hai.";
      }
      
      return NextResponse.json({
        category: targetCategory,
        reply: irrelevantReply,
        sources: ["Relevance Guard"],
        disclaimer: localizedDisclaimer
      });
    }

    // 6. Low Confidence Rule (If no strong match is found, ask a focused clarification question)
    const threshold = (bestMatch && bestMatch.score > 0.0) ? 0.005 : 0.05;
    const hasLegalKeywords = (classified.maxScore > 0 || expansions.length > 0 || hasUrduLegalTerm || hasRomanLegalTerm);
    
    if (!bestMatch || bestMatch.score < threshold || !hasLegalKeywords) {
      const clarification = CLARIFYING_QUESTIONS[targetCategory] || {
        en: "Could you please provide more details about your legal query?",
        ur: "کیا آپ اپنے قانونی سوال کے بارے میں مزید تفصیلات فراہم کر سکتے ہیں؟",
        roman: "Kya aap apne legal query ke baare mein mazeed details faraham kar sakte hain?"
      };
      
      let fallbackReply = clarification[lang] || clarification.en;
      let localizedDisclaimer = "This AI system provides informational legal guidance only and is not a substitute for professional legal advice.";
      
      if (lang === 'urdu_script') {
        localizedDisclaimer = "یہ اے آئی سسٹم صرف معلوماتی قانونی رہنمائی فراہم کرتا ہے اور پیشہ ورانہ قانونی مشورے کا متبادل نہیں ہے۔";
      } else if (lang === 'roman_urdu') {
        localizedDisclaimer = "Yeh AI system sirf malomati kanooni rehnumai faraham karta hai aur peshawarana kanooni mashwaray ka badal nahi hai.";
      }

      return NextResponse.json({
        category: targetCategory,
        reply: fallbackReply,
        sources: ["Low Confidence Fallback"],
        disclaimer: localizedDisclaimer
      });
    }

    // 7. Format structured response
    const formattedReply = formatStructuredResponse(searchQuery, targetCategory, bestMatch.record);

    let reply = formattedReply;
    let disclaimer = "This AI system provides informational legal guidance only and is not a substitute for professional legal advice.";

    if (lang === 'urdu_script') {
      const urduTranslation = await translateToUrduAndRoman(reply);
      if (urduTranslation.urdu === reply) {
        // Fallback to high quality offline translation template
        const recordTitle = bestMatch?.record?.title || "";
        reply = LOCAL_RECORD_TRANSLATIONS[recordTitle]?.["ur"] || LOCAL_TRANSLATIONS[targetCategory]?.["ur"] || reply;
      } else {
        reply = urduTranslation.urdu;
      }
      disclaimer = await translateText(disclaimer, 'en', 'ur');
      if (disclaimer === "This AI system provides informational legal guidance only and is not a substitute for professional legal advice.") {
        disclaimer = "یہ اے آئی سسٹم صرف معلوماتی قانونی رہنمائی فراہم کرتا ہے اور پیشہ ورانہ قانونی مشورے کا متبادل نہیں ہے۔";
      }
    } else if (lang === 'roman_urdu') {
      const urduTranslation = await translateToUrduAndRoman(reply);
      if (urduTranslation.roman === reply) {
        // Fallback to high quality offline translation template
        const recordTitle = bestMatch?.record?.title || "";
        reply = LOCAL_RECORD_TRANSLATIONS[recordTitle]?.["roman"] || LOCAL_TRANSLATIONS[targetCategory]?.["roman"] || reply;
      } else {
        reply = urduTranslation.roman;
      }
      disclaimer = "Yeh AI system sirf malomati kanooni rehnumai faraham karta hai aur peshawarana kanooni mashwaray ka badal nahi hai.";
    }

    return NextResponse.json({
      category: targetCategory,
      reply: reply,
      sources: [bestMatch.record.source],
      disclaimer: disclaimer
    });
  } catch (error: any) {
    console.error("API processing error:", error);
    return NextResponse.json({ error: error.message || "Internal server error" }, { status: 500 });
  }
}

// Pre-warm the dataset and BM25 index on startup/import
Promise.resolve().then(() => {
  try {
    getDatasetAndIndex();
  } catch (err) {
    console.error("Error pre-warming dataset and index:", err);
  }
});

