import os
import re
import math
import numpy as np
from typing import List, Dict, Any, Tuple
from .utils import logger, get_config
from .category_classifier import CategoryClassifier
from .embeddings import EmbeddingsManager
from .vector_store import VectorStoreManager
from .language_manager import detect_language, translate_text, translate_to_urdu_and_roman

try:
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

class BM25:
    def __init__(self, corpus: List[str], k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.corpus_size = len(corpus)
        self.tokenized_corpus = [self.tokenize(doc) for doc in corpus]
        self.doc_lengths = [len(doc) for doc in self.tokenized_corpus]
        self.avg_doc_length = sum(self.doc_lengths) / self.corpus_size if self.corpus_size > 0 else 1.0
        
        self.doc_freqs = {}
        self.idf = {}
        
        # Calculate document frequencies
        for doc in self.tokenized_corpus:
            seen = set(doc)
            for word in seen:
                self.doc_freqs[word] = self.doc_freqs.get(word, 0) + 1
                
        # Calculate IDF
        for word, freq in self.doc_freqs.items():
            # Standard BM25 IDF formulation
            self.idf[word] = math.log((self.corpus_size - freq + 0.5) / (freq + 0.5) + 1.0)
            
    def tokenize(self, text: str) -> List[str]:
        # Lowercase, clean non-alphanumeric and split into tokens, filtering out stop words
        stop_words = {
            "the", "be", "to", "of", "and", "a", "in", "that", "have", "it", "for", "not", "on", "with", "he", 
            "as", "you", "do", "at", "this", "but", "his", "by", "from", "they", "we", "say", "her", "she", 
            "or", "an", "will", "my", "one", "all", "would", "there", "their", "what", "so", "up", "out", 
            "if", "about", "who", "get", "which", "go", "me", "when", "make", "can", "like", "time", "no", 
            "just", "him", "know", "take", "people", "into", "year", "your", "good", "some", "could", 
            "them", "see", "other", "than", "then", "now", "look", "only", "come", "its", "over", 
            "think", "also", "back", "after", "use", "two", "how", "our", "work", "first", "well", 
            "way", "even", "new", "want", "because", "any", "these", "give", "day", "most", "us", 
            "is", "are", "was", "were", "been", "has", "had", "should", "would", "could"
        }
        # Keep unicode letters and digits (supported by \w in python 3 regex by default) + Urdu script
        cleaned = re.sub(r'[^\w\s\u0600-\u06ff]', '', text.lower())
        return [w for w in cleaned.split() if w not in stop_words]

    def get_score(self, query_tokens: List[str], doc_idx: int) -> float:
        score = 0.0
        doc_tokens = self.tokenized_corpus[doc_idx]
        doc_len = self.doc_lengths[doc_idx]
        
        word_counts = {}
        for word in doc_tokens:
            word_counts[word] = word_counts.get(word, 0) + 1
            
        for word in query_tokens:
            if word in word_counts:
                freq = word_counts[word]
                idf = self.idf.get(word, 0.0)
                tf_numerator = freq * (self.k1 + 1)
                tf_denominator = freq + self.k1 * (1 - self.b + self.b * (doc_len / self.avg_doc_length))
                score += idf * (tf_numerator / tf_denominator)
        return score

def clean_text(text: str) -> str:
    """
    Cleans text by removing extra spaces, newlines, and punctuation.
    """
    if not text:
        return ""
    # Remove special characters except common punctuation and Urdu script characters
    text = re.sub(r'[^\w\s\.,\?\-–⚖️\u0600-\u06ff]', ' ', text)
    # Normalize whitespace
    return " ".join(text.split()).strip()

LOCAL_TRANSLATIONS = {
    "Constitutional Laws": {
        "ur": """**Category (زمرہ)**: Constitutional Laws

**Title**: بنیادی حقوق اور ہائی کورٹ کی رٹ پٹیشنز

**Direct Answer**:
دستورِ پاکستان کے آئینی قوانین کے تحت آپ کا سوال بنیادی حقوق کے تحفظ اور آرٹیکل 199 کے تحت ان کے نفاذ سے متعلق ہے۔

**Relevant Legal Information**:
دستورِ پاکستان 1973 کے تحت، آرٹیکل 9 شہریوں کی جان و آزادی کا تحفظ فراہم کرتا ہے، آرٹیکل 10-A منصفانہ ٹرائل کا حق دیتا ہے، آرٹیکل 19 آزادیِ اظہارِ رائے کی ضمانت دیتا ہے، اور آرٹیکل 25 قانون کی نظر میں تمام شہریوں کی برابری کی ضمانت دیتا ہے۔ آرٹیکل 199 کے تحت اگر سرکاری حکام بنیادی حقوق کی خلاف ورزی کریں تو شہری ہائیکورٹ میں آئینی رٹ پٹیشن (جیسے حبسِ بے جا یا حکمِ امتناعی) دائر کر سکتے ہیں۔

**Important Notes**:
1. **حفاظتی دستبرداری**: رول 7 کے تحت یہ نظام تعلیمی مقاصد کے لیے معلومات فراہم کرتا ہے اور پیشہ ورانہ قانونی مشورہ کا متبادل نہیں ہے۔
2. **طریقہ کار**: آئینی مقدمات پیچیدہ ہوتے ہیں۔ اپنی رٹ پٹیشن تیار کرنے اور پیش کرنے کے لیے ہائیکورٹ کے مستند وکیل سے رجوع کریں۔

**Source Document**: دستورِ پاکستان، 1973 (حصہ دوم اور آرٹیکل 199)""",
        "roman": """**Category (زمرہ)**: Constitutional Laws

**Title**: Bunyadi Huqooq aur High Court ki Writ Petitions

**Direct Answer**:
Aap ka sawal Pakistan ke aaeeni qawaneen, bunyadi huqooq aur Article 199 ke tehat writ petition ke nafadh se mutalliq hai.

**Relevant Legal Information**:
Constitution of Pakistan 1973 ke tehat, Article 9 jaan aur azaadi ka tahaffuz deta hai, Article 10A fair trial ka haq deta hai, Article 19 freedom of speech ki guarantee deta hai, aur Article 25 sab shehriyon ki barabri ka haq deta hai. Article 199 ke tehat agar sarkari idaray aap ke bunyadi huqooq ko violate karein, to aap High Court mein writ petition (Habeas Corpus, Mandamus) file kar sakte hain.

**Important Notes**:
1. **Safety Disclaimer**: Under Rule 7, yeh system sirf educational purposes ke liye legal information deta hai. Yeh professional advice ya legal guarantee nahi hai.
2. **Procedural Action**: Aaeeni mamlat ke liye High Court ke registered lawyer se consult karein taake wo proper petition draft kar sakein.

**Source Document**: Constitution of the Islamic Republic of Pakistan, 1973 (Part II & Article 199)"""
    },
    "Family Laws": {
        "ur": """**Category (زمرہ)**: Family Laws

**Title**: خاندانی قوانین: شادی، طلاق، خلع اور بچوں کی کسٹڈی

**Direct Answer**:
پاکستان کے خاندانی قوانین کے تحت آپ کا سوال مسلم فیملی لاز آرڈیننس 1961 اور گارڈینز اینڈ وارڈز ایکٹ 1890 کے تحت حل ہوتا ہے۔

**Relevant Legal Information**:
مسلم فیملی لاز آرڈیننس (MFLO) 1961 کے تحت، شوہر کے لیے دوسری شادی کرنے سے پہلے پہلی بیوی اور ثالثی کونسل سے تحریری اجازت لینا لازمی ہے (دفعہ 6)۔ طلاق کی صورت میں شوہر یونین کونسل کو نوٹس دینے کا پابند ہے اور طلاق 90 دن کی عدت کے بعد مؤثر ہوتی ہے (دفعہ 7)۔ بیوی فیملی کورٹ سے خلع کا دعویٰ دائر کر سکتی ہے۔ بچوں کی تحویل اور سرپرستی گارڈینز اینڈ وارڈز ایکٹ 1890 کے تحت بچے کی فلاح و بہبود کے اصول پر طے ہوتی ہے۔ شوہر بیوی اور بچوں کو نان و نفقہ دینے کا پابند ہے (دفعہ 9)۔

**Important Notes**:
1. **حفاظتی دستبرداری**: رول 7 کے تحت یہ نظام تعلیمی مقاصد کے لیے معلومات فراہم کرتا ہے اور پیشہ ورانہ قانونی مشورہ کا متبادل نہیں ہے۔
2. **طریقہ کار**: نان و نفقہ، حق مہر، اور بچوں کی کسٹڈی کے مقدمات فیملی کورٹ میں دائر کیے جاتے ہیں۔ نکاح نامہ کی شرائط کو بغور پر کریں۔

**Source Document**: مسلم فیملی لاز آرڈیننس، 1961 اور گارڈینز اینڈ وارڈز ایکٹ، 1890""",
        "roman": """**Category (زمرہ)**: Family Laws

**Title**: Khandani Qawaneen: Shadi, Talaq, Khula aur Custody

**Direct Answer**:
Aap ka family law se mutalliq sawal Muslim Family Laws Ordinance 1961 aur Guardians and Wards Act 1890 ke tehat hal hota hai.

**Relevant Legal Information**:
Muslim Family Laws Ordinance (MFLO) 1961 ke Section 6 ke tehat, shohar pehli biwi aur Arbitration Council ki written consent ke baghair doosri shadi nahi kar sakta. Section 7 ke tehat Talaq dene ke baad Union Council ko written notice bhejna aur 90 days iddat guzarna lazmi hai. Biwi court se Khula le sakti hai. Bachon ki custody Guardians and Wards Act 1890 ke tehat bachay ki welfare ke mutabiq tay hoti hai. Shohar par biwi aur bachon ka monthly kharcha (maintenance) dena lazmi hai (Section 9).

**Important Notes**:
1. **Safety Disclaimer**: Under Rule 7, yeh system sirf educational purposes ke liye legal information deta hai. Yeh professional advice ya legal guarantee nahi hai.
2. **Procedural Action**: Kharcha, Haq Mehr, aur custody ke suits Family Court mein file kiye jaate hain. Nikahnama ke columns ko dhyan se check karein.

**Source Document**: Muslim Family Laws Ordinance, 1961 & Guardians and Wards Act, 1890"""
    },
    "Criminal Laws": {
        "ur": """**Title**: ایف آئی آر کی رجسٹریشن، گرفتاری، ضمانت اور تعزیراتی سزائیں

**Direct Answer**:
آپ کا فوجداری قانون کا سوال تعزیراتِ پاکستان 1860 اور ضابطہ فوجداری 1898 کے دائرہ اختیار میں آتا ہے۔

**Relevant Legal Information**:
دفعہ 154 ضابطہ فوجداری کے تحت پولیس قابل دست اندازی جرائم کی ایف آئی آر (FIR) درج کرنے کی پابند ہے۔ اگر ایس ایچ او انکار کرے تو دفعہ 22-A/22-B کے تحت سیشن جج (جسٹس آف پیس) کو درخواست دی جا سکتی ہے۔ ضمانت کی درخواستیں دفعہ 496 (قابلِ ضمانت)، 497 (ناقابلِ ضمانت) اور 498 (قبل از گرفتاری حفاظتی ضمانت) کے تحت دائر کی جاتی ہیں۔ تعزیراتِ پاکستان (PPC) کے تحت چوری کی سزا دفعہ 379 (تین سال تک قید)، جائیداد کو نقصان پہنچانے کی سزا دفعہ 427 اور جعل سازی کی سزا دفعہ 468 کے تحت مقرر ہے۔

**Important Notes**:
1. **حفاظتی دستبرداری**: رول 7 کے تحت یہ نظام تعلیمی مقاصد کے لیے معلومات فراہم کرتا ہے اور پیشہ ورانہ قانونی مشورہ کا متبادل نہیں ہے۔
2. **طریقہ کار**: گرفتاری کی صورت میں پولیس ملزم کو 24 گھنٹے کے اندر مجسٹریٹ کے سامنے پیش کرنے کی پابند ہے (دفعہ 61)۔ ایف آئی آر کی مصدقہ نقل حاصل کریں اور فوجداری وکیل سے رجوع کریں۔

**Source Document**: تعزیراتِ پاکستان (PPC) 1860 اور ضابطہ فوجداری (CrPC) 1898""",
        "roman": """**Title**: FIR Registration, Arrest, Bail aur Penal Code Actions

**Direct Answer**:
Aap ka criminal law ka sawal Pakistan Penal Code 1860 aur Code of Criminal Procedure 1898 ke tehat aata hai.

**Relevant Legal Information**:
Section 154 CrPC ke tehat police cognizable offenses ki FIR register karne ki paband hai. Agar SHO mana kare to Section 22-A/22-B CrPC ke tehat Sessions Judge (Justice of Peace) ke paas complaint ki ja sakti hai. Bail applications Section 496, 497, aur 498 (pre-arrest protective bail) ke tehat file hoti hain. PPC ke tehat Theft (Section 378/379), Mischief (Section 427), aur Forgery (Section 468) ke liye specific punishments hain.

**Important Notes**:
1. **Safety Disclaimer**: Under Rule 7, yeh system sirf educational purposes ke liye legal information deta hai. Yeh professional advice ya legal guarantee nahi hai.
2. **Procedural Action**: Arrest hone par police ko 24 hours ke andar accused ko magistrate ke samnay pesh karna zaroori hai (Section 61). FIR ki copy hasil karein aur criminal defense advocate se consult karein.

**Source Document**: Pakistan Penal Code (PPC), 1860 & Code of Criminal Procedure (CrPC), 1898"""
    },
    "Civil Laws": {
        "ur": """**Title**: مخصوص دادرسی، حکمِ امتناعی (سٹے آرڈر)، اور معاہدوں کا قانون

**Direct Answer**:
پاکستان کے دیوانی قوانین کے تحت آپ کا سوال مخصوص دادرسی ایکٹ 1877 اور معاہدہ ایکٹ 1872 کے تحت حل ہوتا ہے۔

**Relevant Legal Information**:
مخصوص دادرسی ایکٹ 1877 کے تحت، اگر کسی شخص کو مرضی کے بغیر جائیداد سے بے دخل کیا جائے تو وہ 6 ماہ کے اندر قبضہ کی بحالی کا دعویٰ دائر کر سکتا ہے (دفعہ 9)۔ دفعہ 12 کے تحت معاہدوں کی مخصوص تعمیل کروائی جا سکتی ہے۔ دفعہ 42 کے تحت اعلانیہ دعویٰ (ڈیکلریٹری سوٹ) دائر کیا جاتا ہے تاکہ مالکانہ حقوق یا قانونی حیثیت کا اعلان کروایا جا سکے۔ دفعہ 54 کے تحت حکمِ امتناعی (سٹے آرڈر) جاری کیا جاتا ہے۔ معاہدہ ایکٹ 1872 کے تحت، معاہدے کے لیے آزاد رضامندی (دفعہ 10) لازمی ہے اور معاہدے کی خلاف ورزی پر ہرجانے (دفعہ 73) کا دعویٰ کیا جا سکتا ہے۔

**Important Notes**:
1. **حفاظتی دستبرداری**: رول 7 کے تحت یہ نظام تعلیمی مقاصد کے لیے معلومات فراہم کرتا ہے اور پیشہ ورانہ قانونی مشورہ کا متبادل نہیں ہے۔
2. **طریقہ کار**: دیوانی مقدمات سول عدالتوں میں دائر کیے جاتے ہیں۔ مقدمہ بازی سے پہلے فریق مخالف کو باضابطہ قانونی نوٹس بھیجیں۔

**Source Document**: مخصوص دادرسی ایکٹ، 1877 اور معاہدہ ایکٹ، 1872""",
        "roman": """**Title**: Specific Relief, Stay Orders, aur Contract Act Rules

**Direct Answer**:
Aap ka civil law ka sawal Specific Relief Act 1877 aur Contract Act 1872 ke tehat hal hota hai.

**Relevant Legal Information**:
Specific Relief Act 1877 ke Section 9 ke tehat, agar kisi ko property se be-dakhal kiya jaye to wo 6 months ke andar possession bahal karwane ka suit dalk sakta hai. Section 12 ke tehat contract ki specific performance claim ki ja sakti hai. Section 42 ke tehat declaratory suit file hota hai. Injunctions (stay orders) Section 54 ke tehat issue hote hain. Contract Act 1872 ke mutabiq, breach of contract par damages (Section 73) claim kiye ja sakte hain.

**Important Notes**:
1. **Safety Disclaimer**: Under Rule 7, yeh system sirf educational purposes ke liye legal information deta hai. Yeh professional advice ya legal guarantee nahi hai.
2. **Procedural Action**: Civil disputes Civil Court mein file hote hain. Legal action se pehle proper written legal notice send karna advisable hai.

**Source Document**: Specific Relief Act, 1877 & Contract Act, 1872"""
    },
    "Property Laws": {
        "ur": """**Title**: انتقالِ جائیداد، ہبہ نامہ (تحفہ)، اور غیر قانونی قبضے کے خلاف دادرسی

**Direct Answer**:
پاکستان کے جائیداد کے قوانین کے تحت آپ کا تنازعہ ٹرانسفر آف پراپرٹی ایکٹ 1882، رجسٹریشن ایکٹ 1908، اور الیگل ڈسپوزیشن ایکٹ 2005 کے تحت آتا ہے۔

**Relevant Legal Information**:
ٹرانسفر آف پراپرٹی ایکٹ 1882 کے تحت جائیداد کی فروخت کے لیے رجسٹرڈ سیل ڈیڈ لازمی ہے (دفعہ 54)۔ ہبہ (تحفے) کے لیے تحریر، قبولیت، اور جائیداد کا قبضہ منتقل کرنا لازمی ہے (دفعہ 122)۔ پٹواری نظام میں جائیداد کے ریکارڈ فرد اور انتقال (Mutation) کے ذریعے رکھے جاتے ہیں۔ قبضہ مافیا کے خلاف الیگل ڈسپوزیشن ایکٹ 2005 کے تحت سیشن کورٹ میں براہِ راست شکایت درج کی جا سکتی ہے، جہاں عدالت پولیس کو فوری قبضہ بحال کرنے اور قبضہ کرنے والوں کو 10 سال تک قید کی سزا دینے کا اختیار رکھتی ہے۔

**Important Notes**:
1. **حفاظتی دستبرداری**: رول 7 کے تحت یہ نظام تعلیمی مقاصد کے لیے معلومات فراہم کرتا ہے اور پیشہ ورانہ قانونی مشورہ کا متبادل نہیں ہے۔
2. **طریقہ کار**: جائیداد خریدنے سے پہلے اراضی ریکارڈ سینٹر (ARC) یا سب رجسٹرار آفس سے فرد اور رجسٹری کی تصدیق کریں۔ زبانی سودے کی کوئی قانونی حیثیت نہیں ہے۔

**Source Document**: ٹرانسفر آف پراپرٹی ایکٹ، 1882 اور الیگل ڈسپوزیشن ایکٹ، 2005""",
        "roman": """**Title**: Transfer of Property, Gift Deeds (Hiba), aur Illegal Qabza Remedies

**Direct Answer**:
Property disputes, Hiba, aur illegal qabza ke khilaf action Transfer of Property Act 1882 aur Illegal Dispossession Act 2005 ke tehat aata hai.

**Relevant Legal Information**:
Transfer of Property Act 1882 ke Section 54 ke tehat property sale ke liye registered deed lazmi hai. Gift deed (Hiba) ke liye Section 122 ke mutabiq donor ki taraf se property ka physical possession hand over karna zaroori hai. Qabza mafia aur land grabbing ke khilaf Illegal Dispossession Act 2005 ke tehat Sessions Court mein direct complaint file ki ja sakti hai, jahan court immediate restoration (Section 8) ka order de sakti hai.

**Important Notes**:
1. **Safety Disclaimer**: Under Rule 7, yeh system sirf educational purposes ke liye legal information deta hai. Yeh professional advice ya legal guarantee nahi hai.
2. **Procedural Action**: Property purchase karne se pehle Arazi Record Center se Fard aur Mutation (Intiqal) verify karein. Oral property deals invalid hote hain.

**Source Document**: Transfer of Property Act, 1882 & Illegal Dispossession Act, 2005"""
    },
    "Labour Laws": {
        "ur": """**Title**: تنخواہوں کی ادائیگی، شرائطِ ملازمت اور لیبر کورٹ کی کارروائی

**Direct Answer**:
ملازمت کے تنازعات، تنخواہوں میں تاخیر، اور برطرفی پیمنٹ آف ویجز ایکٹ 1936 اور اسٹینڈنگ آرڈرز آرڈیننس 1968 کے تحت حل ہوتے ہیں۔

**Relevant Legal Information**:
پیمنٹ آف ویجز ایکٹ 1936 کے سیکشن 5 کے تحت آجر (Employer) تنخواہ مقررہ وقت پر ادا کرنے کا پابند ہے۔ تنخواہ میں تاخیر یا کٹوتی کو لیبر کمشنر کے پاس سیکشن 15 کے تحت چیلنج کیا جا سکتا ہے۔ اسٹینڈنگ آرڈر 12 کے تحت مستقل ملازم کو برطرف کرنے کے لیے ایک ماہ کا تحریری نوٹس یا تنخواہ دینا اور گریجویٹی (ہر سال کے بدلے 30 دن کی بنیادی تنخواہ) ادا کرنا لازم ہے۔ بدتمیزی یا کوتاہی پر نوکری سے نکالنے سے پہلے شوکاز نوٹس اور آزادانہ انکوائری لازم ہے (اسٹینڈنگ آرڈر 15)۔

**Important Notes**:
1. **حفاظتی دستبرداری**: رول 7 کے تحت یہ نظام تعلیمی مقاصد کے لیے معلومات فراہم کرتا ہے اور پیشہ ورانہ قانونی مشورہ کا متبادل نہیں ہے۔
2. **طریقہ کار**: غیر قانونی برطرفی کی صورت میں ملازم کو 30 دن کے اندر اپنے آجر کو تحریری شکایت بھیجنی ہوتی ہے اور لیبر کورٹ سے رجوع کرنا ہوتا ہے۔ اپنا تقرری خط محفوظ رکھیں۔

**Source Document**: پیمنٹ آف ویجز ایکٹ، 1936 اور اسٹینڈنگ آرڈرز آرڈیننس، 1968""",
        "roman": """**Title**: Payment of Wages, Gratuity, aur Labor Court Grievance

**Direct Answer**:
Labor aur employment disputes Payment of Wages Act 1936 aur Standing Orders Ordinance 1968 ke tehat hal hote hain.

**Relevant Legal Information**:
Wages Act ke Section 5 ke tehat shohar ya employer salary waqt par dene ka paband hai. Agar delayed salary ya unauthorized deduction ho to Section 15 ke tehat Labor Commissioner ke paas case file ho sakta hai. Standing Order 12 ke tehat permanent worker ki termination par 1-month notice aur gratuity (30 days basic pay per year) lazmi hai. Dismissal for misconduct se pehle show-cause aur inquiry mandatory hai (Order 15).

**Important Notes**:
1. **Safety Disclaimer**: Under Rule 7, yeh system sirf educational purposes ke liye legal information deta hai. Yeh professional advice ya legal guarantee nahi hai.
2. **Procedural Action**: Labor Court jaane se pehle employer ko written grievance notice bhejna zaroori hai. Employment contract aur salary slips ka record save rakhein.

**Source Document**: Payment of Wages Act, 1936 & Standing Orders Ordinance, 1968"""
    },
    "Tax Laws": {
        "ur": """**Title**: انکم ٹیکس ریٹرن، ایف بی آر اسیسمنٹس اور ٹیکس اپیلیں

**Direct Answer**:
ٹیکس کے معاملات، ریٹرن فائلنگ، اور ایف بی آر اسیسمنٹس انکم ٹیکس آرڈیننس 2001 اور سیلز ٹیکس ایکٹ 1990 کے تحت حل ہوتے ہیں۔

**Relevant Legal Information**:
انکم ٹیکس آرڈیننس 2001 کے سیکشن 114 کے تحت ہر وہ شخص جس کی آمدنی ٹیکس کی حد سے زیادہ ہو، سالانہ ریٹرن فائل کرنے کا پابند ہے۔ فائل کردہ ریٹرن اسیسمنٹ مانی جاتی ہے (سیکشن 120) لیکن ایف بی آر کمشنر شوکاز نوٹس جاری کر کے اسیسمنٹ میں ترمیم کر سکتا ہے (سیکشن 122)۔ دیر سے ادائیگی پر ڈیفالٹ سرچارج عائد ہوتا ہے (سیکشن 205)۔ سیلز ٹیکس ایکٹ 1990 کے سیکشن 3 کے تحت سپلائیز پر 18 فیصد سیلز ٹیکس وصول کیا جاتا ہے۔ ٹیکس کے فیصلوں کے خلاف اپیلیں کمشنر اپیل اور پھر اپیلٹ ٹریبیونل (ATIR) میں دائر ہوتی ہیں۔

**Important Notes**:
1. **حفاظتی دستبرداری**: رول 7 کے تحت یہ نظام تعلیمی مقاصد کے لیے معلومات فراہم کرتا ہے اور پیشہ ورانہ قانونی مشورہ کا متبادل نہیں ہے۔
2. **طریقہ کار**: فائلر بننے سے ودہولڈنگ ٹیکس کی شرح آدھی ہو جاتی ہے۔ ایف بی آر کے کسی بھی نوٹس کا 15 دن کے اندر تحریری جواب دیں اور اپنے بینک سٹیٹمنٹس کا ریکارڈ رکھیں۔

**Source Document**: انکم ٹیکس آرڈیننس، 2001 اور سیلز ٹیکس ایکٹ، 1990""",
        "roman": """**Title**: Income Tax return FBR Audit, aur Sales Tax appeals

**Direct Answer**:
Tax matters, income tax return filing, aur FBR audits Income Tax Ordinance 2001 aur Sales Tax Act 1990 ke tehat aate hain.

**Relevant Legal Information**:
Section 114 Income Tax Ordinance ke tehat taxable income limits cross hone par annual tax return file karna zaroori hai. FBR Commissioner Section 122 ke tehat show-cause notice de kar assessment order amend kar sakta hai. Late tax payment par Section 205 ke tehat default surcharge lagta hai. Sales Tax Act 1990 ke Section 3 ke tehat standard sales tax 18% hai. Tax disputes ki appeals CIR (Appeals) aur ATIR mein file hoti hain.

**Important Notes**:
1. **Safety Disclaimer**: Under Rule 7, yeh system sirf educational purposes ke liye legal information deta hai. Yeh professional advice ya legal guarantee nahi hai.
2. **Procedural Action**: Tax filer banne se withholding tax rates kam hote hain. Audit compliance ke liye transaction records 6 years tak save rakhein.

**Source Document**: Income Tax Ordinance, 2001 & Sales Tax Act, 1990"""
    },
    "Consumer Protection Laws": {
        "ur": """**Category (زمرہ)**: Consumer Protection Laws

**Title**: ناقص اشیاء، ناقص خدمات اور کنزیومر عدالتیں

**Direct Answer**:
ناقص اشیاء، آن لائن فراڈ اور ناقص سروسز کے خلاف شکایات صوبائی کنزیومر پروٹیکشن ایکٹ (جیسے پنجاب کنزیومر پروٹیکشن ایکٹ 2005) کے تحت حل ہوتی ہیں۔

**Relevant Legal Information**:
پنجاب کنزیومر پروٹیکشن ایکٹ 2005 کے سیکشن 13 کے تحت مینوفیکچرر یا دکاندار ناقص مصنوعات اور ناقص خدمات کے لیے ذمہ دار ہے۔ دعویٰ دائر کرنے سے پہلے دکاندار کو سیکشن 28 کے تحت 15 روزہ تحریری قانونی نوٹس بھیجنا لازمی ہے۔ اگر نوٹس کا جواب نہ ملے یا مسئلہ حل نہ ہو تو 30 دن کے اندر کنزیومر کورٹ میں کیس دائر کیا جا سکتا ہے۔ کنزیومر کورٹ مصنوعات کی واپسی، قیمت کی واپسی اور ذہنی اذیت کے نقصانات (سیکشن 21) کی دگری دے سکتی ہے۔

**Important Notes**:
1. **حفاظتی دستبرداری**: رول 7 کے تحت یہ نظام تعلیمی مقاصد کے لیے معلومات فراہم کرتا ہے اور پیشہ ورانہ قانونی مشورہ کا متبادل نہیں ہے۔
2. **طریقہ کار**: کنزیومر کورٹ میں دعویٰ دائر کرنے کے لیے کوئی فیس نہیں ہے اور آپ بغیر وکیل کے بھی اپنا کیس لڑ سکتے ہیں۔ خریداری کی رسید اور قانونی نوٹس کی رسید ہمیشہ سنبھال کر رکھیں۔

**Source Document**: پنجاب کنزیومر پروٹیکشن ایکٹ، 2005 (یا دیگر صوبائی مساوی قوانین)""",
        "roman": """**Category (زمرہ)**: Consumer Protection Laws

**Title**: Defective products, online store fraud aur Consumer Courts

**Direct Answer**:
Defective products ya poor services ke khilaf complaints provincial Consumer Protection Acts (e.g. Punjab Consumer Protection Act 2005) ke tehat aati hain.

**Relevant Legal Information**:
Section 13 Punjab Consumer Protection Act ke tehat manufacturer/seller defective goods ya deficient services ke liye liable hai. Section 28 ke tehat suit file karne se pehle seller ko 15-day written legal notice mandatory hai. Agar response na aye, to 30 days ke andar Consumer Court mein complaint file ki ja sakti hai. Court refund, replacement aur mental agony ke liye damages (Section 21) de sakti hai.

**Important Notes**:
1. **Safety Disclaimer**: Under Rule 7, yeh system sirf educational purposes ke liye legal information deta hai. Yeh professional advice ya legal guarantee nahi hai.
2. **Procedural Action**: Consumer Court mein case file karne ke liye koi fees nahi hoti aur aap self-represent kar sakte hain. Purchase receipt aur legal notice ka record save rakhein.

**Source Document**: Punjab Consumer Protection Act, 2005"""
    }
}

LOCAL_RECORD_TRANSLATIONS = {
    "Legal Age of Marriage (Child Marriage Restraint Act)": {
        "ur": """**Category (زمرہ)**: Family Laws

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
رول 7 کے تحت یہ نظام تعلیمی مقاصد کے لیے معلومات فراہم کرتا ہے اور پیشہ ورانہ قانونی مشورے کا متبادل نہیں ہے۔""",
        "roman": """**Category (زمرہ)**: Family Laws

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
Rule 7 ke tehat yeh system informational purposes ke liye hai aur professional legal advice ka badal nahi hai."""
    }
}

LOCAL_DICTIONARY = {
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
    "معاهدہ": "agreement contract",
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
}

EXPANSION_RULES = {
    "Property": {
        "triggers": ["qabza", "kabza", "possession", "encroachment", "قبضہ", "تجاوز"],
        "expansions": ["illegal possession", "encroachment", "dispossession", "illegal dispossession"]
    },
    "Eviction": {
        "triggers": ["rent", "kiraya", "kirayedar", "tenant", "landlord", "eviction", "evict", "کرایہ", "کرایہ دار"],
        "expansions": ["tenancy agreement", "tenant rights", "eviction", "landlord dispute"]
    },
    "Divorce": {
        "triggers": ["talaq", "talaaq", "divorce", "dissolution", "طلاق"],
        "expansions": ["divorce", "dissolution of marriage", "talaq notice", "talaq certificate", "union council notice"]
    },
    "Iddat": {
        "triggers": ["iddat", "waiting period", "عدت"],
        "expansions": ["iddat period", "iddat rules", "waiting period", "iddat maintenance"]
    },
    "Khula": {
        "triggers": ["khula", "kula", "خلع"],
        "expansions": ["khula", "dissolution of marriage", "dower waiver"]
    },
    "Marriage": {
        "triggers": ["nikah", "nikaah", "shadi", "shaadi", "marriage", "نکاح", "شادی"],
        "expansions": ["marriage registration", "nikahnama", "marriage contract"]
    },
    "Maintenance": {
        "triggers": ["kharcha", "nafaqa", "maintenance", "expenses", "خرچہ", "نفقہ"],
        "expansions": ["child maintenance", "wife maintenance", "expenses allowance"]
    },
    "Custody": {
        "triggers": ["custody", "guardian", "guardianship", "ward", "bache", "bachay", "children", "minor", "کسٹڈی", "تحویل", "سرپرستی", "بچے"],
        "expansions": ["child custody", "visitation rights", "guardianship", "minor ward"]
    },
    "FIR": {
        "triggers": ["fir", "police", "sho", "thana", "ایف آئی آر", "تھانہ"],
        "expansions": ["fir registration", "police complaint", "section 154 crpc"]
    },
    "Bail": {
        "triggers": ["bail", "zamanat", "ضمانت"],
        "expansions": ["pre-arrest bail", "post-arrest bail", "protective bail"]
    },
    "Tax": {
        "triggers": ["tax", "fbr", "filer", "return", "ٹیکس", "ایف بی آر"],
        "expansions": ["income tax return", "fbr audit", "tax assessment"]
    },
    "Consumer": {
        "triggers": ["consumer", "refund", "warranty", "fake", "defective", "ریفنڈ", "وارنٹی"],
        "expansions": ["consumer court", "defective product", "refund replacement"]
    },
    "Age": {
        "triggers": ["age", "عمر", "minor", "child marriage", "na-baligh", "نابالغ"],
        "expansions": ["legal age of marriage", "minimum marriageable age", "child marriage restraint act"]
    }
}

CLARIFYING_QUESTIONS = {
    "Property Laws": {
        "ur": "کیا آپ کے پاس جائیداد کی رجسٹری یا کوئی تحریری معاہدہ (Registry/Tenancy/Agreement) موجود ہے؟ اور کیا آپ مالک ہیں یا کرایہ دار؟",
        "roman": "Kya aap ke paas property ki registry ya koi written agreement (Tenancy/Registry) mojood hai? Aur kya aap owner hain ya tenant?",
        "en": "Do you have a written property registry, mutation, or tenancy agreement? Also, are you the owner or a tenant?"
    },
    "Family Laws": {
        "ur": "کیا آپ کا نکاح نامہ رجسٹرڈ ہے؟ اور کیا آپ نان و نفقہ (خرچہ)، خلع، یا بچوں کی کسٹڈی کے بارے میں پوچھ رہے ہیں؟",
        "roman": "Kya aap ka Nikahnama registered hai? Aur kya aap maintenance (kharcha), Khula, ya child custody ke baare mein pooch rahe hain?",
        "en": "Is the marriage registered with a Nikahnama? Are you seeking maintenance, Khula, child custody, or divorce?"
    },
    "Criminal Laws": {
        "ur": "کیا اس معاملے کی ایف آئی آر (FIR) پہلے سے درج ہو چکی ہے؟ اور کیا ملزم پولیس کی حراست میں ہے یا ضمانت چاہتے ہیں؟",
        "roman": "Kya is mamlay ki FIR pehle se registered ho chuki hai? Aur kya accused police custody mein hai ya bail chahtay hain?",
        "en": "Has a First Information Report (FIR) already been registered? Is the accused currently arrested or seeking bail?"
    },
    "Civil Laws": {
        "ur": "کیا فریقین کے درمیان کوئی تحریری معاہدہ یا اقرار نامہ موجود ہے؟ کیا آپ نے کوئی قانونی نوٹس بھیجا ہے؟",
        "roman": "Kya parties ke darmiyan koi written agreement ya contract mojood hai? Kya aapne koi legal notice send kiya hai?",
        "en": "Is there a written contract or agreement between the parties? Have you served a formal legal notice yet?"
    },
    "Labour Laws": {
        "ur": "کیا آپ کے پاس تقرری کا تحریری خط (Appointment Letter) یا معاہدہ موجود ہے؟ اور کیا معاملہ تنخواہ کا ہے یا برطرفی کا؟",
        "roman": "Kya aap ke paas appointment letter ya written employment contract hai? Aur kya masla salary ka hai ya termination ka?",
        "en": "Do you have a written appointment letter or employment contract? Is the dispute regarding unpaid wages or termination?"
    },
    "Tax Laws": {
        "ur": "کیا آپ ایف بی آر (FBR) میں فائلر رجسٹرڈ ہیں؟ اور کیا یہ نوٹس انکم ٹیکس کا ہے یا سیلز ٹیکس کا؟",
        "roman": "Kya aap FBR ke filer hain ya non-filer? Aur kya yeh notice income tax ka hai ya sales tax ka?",
        "en": "Are you registered as a filer or non-filer with FBR? Is this query regarding an income tax notice or sales tax?"
    },
    "Consumer Protection Laws": {
        "ur": "کیا آپ کے پاس خریداری کی رسید (Receipt) یا وارنٹی کارڈ موجود ہے؟ اور کیا آپ نے دکاندار کو 15 دن کا تحریری قانونی نوٹس بھیجا ہے؟",
        "roman": "Kya aap ke paas purchase receipt ya warranty document hai? Aur kya aapne shopkeeper ko 15 days ka written legal notice send kiya hai?",
        "en": "Do you have the purchase receipt or warranty document? Have you served the mandatory 15-day legal notice to the seller?"
    },
    "Constitutional Laws": {
        "ur": "کیا یہ خلاف ورزی کسی سرکاری افسر یا سرکاری ادارے (Government Department) کی طرف سے کی گئی ہے یا کسی نجی شخص کی طرف سے؟",
        "roman": "Kya yeh violation kisi government department/official ne ki hai ya kisi private individual ne?",
        "en": "Was this violation committed by a government official or public authority, or a private entity?"
    }
}

def get_query_expansions(text: str) -> List[str]:
    text_lower = text.lower()
    expansions = []
    for category, rules in EXPANSION_RULES.items():
        matched = False
        for trigger in rules["triggers"]:
            if re.search(r'\b' + re.escape(trigger) + r'\b', text_lower):
                matched = True
                break
        if matched:
            expansions.extend(rules["expansions"])
    return list(set(expansions))

class RAGPipeline:
    def __init__(self):
        self.config = get_config()
        self.classifier = CategoryClassifier()
        self.embeddings_mgr = EmbeddingsManager()
        self.vector_store = VectorStoreManager()
        
        self.index_loaded = self.vector_store.load_index()
        self.tokenizer = None
        self.model = None
        self.generator = None

    def load_llm(self):
        """
        Lazy load local model (Llama 3/Mistral) if resources permit.
        """
        if not HAS_TORCH:
            logger.info("Deep learning frameworks (torch/transformers) are missing. Running lightweight RAG compiler.")
            self.generator = None
            return

        if self.generator is not None:
            return
            
        model_id = self.config["llm_model"]
        try:
            device = 0 if torch.cuda.is_available() else -1
            logger.info(f"Initializing LLM generation model: {model_id} on device: {device}...")
            
            self.tokenizer = AutoTokenizer.from_pretrained(model_id)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_id, 
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None
            )
            self.generator = pipeline(
                "text-generation", 
                model=self.model, 
                tokenizer=self.tokenizer,
                max_new_tokens=512,
                temperature=0.2,
                top_p=0.9,
                device=device if device == 0 else None
            )
            logger.info("Llama 3/Mistral model loaded successfully.")
        except Exception as e:
            logger.warning(f"Could not load local LLM model: {str(e)}. Using corporate knowledge compiler.")
            self.generator = None

    def format_structured_response(self, query: str, category: str, record: dict) -> str:
        """
        Formats the output according to the 5 structured sections.
        """
        title = record.get("title", f"Pakistani Legal Analysis: {category}")
        source = record.get("source", "Constitution and Statutes of Pakistan")
        statute = record.get("statute", "Statutory Provisions of Pakistan")
        answer_text = record.get("answer", "")
        
        direct_answer = f"Based on your query regarding **{title}** under **{category}** in Pakistan: "
        
        if category == "Family Laws":
            direct_answer += "Your family law matter is governed by the Muslim Family Laws Ordinance 1961 and the Guardians and Wards Act 1890. You have the right to seek recourse through the Family Courts or local Union Council."
        elif category == "Criminal Laws":
            direct_answer += "The relevant procedural and penal code actions dictate filing an FIR and seeking appropriate bail or prosecution remedies under CrPC/PPC."
        elif category == "Civil Laws":
            direct_answer += "Equitable relief and contract dispute resolutions must be sought through civil courts under the Specific Relief Act 1877 or Contract Act 1872."
        elif category == "Property Laws":
            direct_answer += "Possession, transfer, and ownership protection fall under the Transfer of Property Act 1882, the Registration Act 1908, or the Illegal Dispossession Act 2005."
        elif category == "Labour Laws":
            direct_answer += "Wages, wrongful termination, and gratuity claims are adjudicated in Labor Courts under the Standing Orders Ordinance 1968 or Payment of Wages Act 1936."
        elif category == "Tax Laws":
            direct_answer += "Tax assessments, return filings, and FBR audit appeals are governed by the Income Tax Ordinance 2001 and Sales Tax Act 1990."
        elif category == "Consumer Protection Laws":
            direct_answer += "Consumer grievances regarding defective goods or negligent services are filed in District Consumer Courts under provincial Consumer Protection Acts."
        elif category == "Constitutional Laws":
            direct_answer += "Fundamental rights are protected and enforced via writ petitions in the High Court under Article 199 of the Constitution of Pakistan."
        else:
            direct_answer += "Statutory regulations and relevant local laws govern the legal resolution of this matter."

        next_steps = ""
        if category == "Family Laws":
            next_steps = "1. Gather supporting evidence (Nikahnama, CNIC of parties, children B-Form).\n2. Consult a family lawyer to draft a suit for maintenance, khula, or custody.\n3. File the suit in the local Family Court of the district where the wife resides."
        elif category == "Criminal Laws":
            next_steps = "1. Visit the local police station (Thana) immediately to report the offense.\n2. Request the SHO to register a First Information Report (FIR) under Section 154 CrPC.\n3. If the police refuse to register the FIR, file a petition under Section 22-A/22-B CrPC before the Sessions Judge (Justice of Peace) to seek a court order directing the police to register the FIR."
        elif category == "Civil Laws":
            next_steps = "1. Serve a written legal notice to the opposite party demanding compliance or settlement.\n2. If unresolved, consult a civil lawyer to draft a plaint (suit).\n3. File the suit (for specific performance, declaration, or injunction) in the competent Civil Court having jurisdiction."
        elif category == "Property Laws":
            next_steps = "1. Obtain verified land registry/mutation documents from the Arazi Record Center (ARC) or Patwari.\n2. If facing illegal dispossession or land grabbing, file a petition under the Illegal Dispossession Act 2005 in the Sessions Court.\n3. For boundaries or partition disputes, file a partition suit in the Civil Court."
        elif category == "Labour Laws":
            next_steps = "1. Serve a written grievance notice to the employer within 30 days under Section 25-A of the Industrial Relations Act.\n2. If the employer does not resolve the issue, file a petition in the Labour Court within 30 days.\n3. For delayed/unpaid wages, file an application before the Authority under the Payment of Wages Act."
        elif category == "Tax Laws":
            next_steps = "1. Log into the FBR IRIS portal to file annual returns, or respond to FBR notices under Section 122.\n2. If aggrieved by an assessment amendment, file an appeal before the Commissioner Inland Revenue (Appeals) within 30 days.\n3. For further disputes, appeal before the Appellate Tribunal Inland Revenue (ATIR)."
        elif category == "Consumer Protection Laws":
            next_steps = "1. Draft and serve a mandatory 15-day written legal notice to the seller/manufacturer under Section 28 (demanding refund, replacement, or damages).\n2. Send the notice via registered post with acknowledgment due (AD) and keep the receipt.\n3. If unresolved after 15 days, file a formal complaint in the District Consumer Court within 30 days of the cause of action."
        elif category == "Constitutional Laws":
            next_steps = "1. Consult a registered High Court Advocate to draft a Writ Petition under Article 199 of the Constitution.\n2. Specify the violation of fundamental rights or illegal actions of the public authority.\n3. File the petition in the High Court of the relevant province."
        else:
            next_steps = "1. Consult an appropriate legal advocate specializing in this area.\n2. Review all relevant documents and contracts.\n3. File a claim or representation in the competent court or regulatory authority."

        required_docs = ""
        if category == "Family Laws":
            required_docs = "Nikahnama (Marriage Contract), CNIC of parties, Children's B-Form, list of dowry articles, proof of husband's income."
        elif category == "Criminal Laws":
            required_docs = "Copy of the FIR (if registered), written complaint, medical report (in injury cases), CNIC, list of witnesses."
        elif category == "Civil Laws":
            required_docs = "Written agreement/contract, correspondence/notices exchanged, payment receipts, CNIC."
        elif category == "Property Laws":
            required_docs = "Registry deed, mutation (intiqal) document, Fard (ownership record), layout plan, CNIC."
        elif category == "Labour Laws":
            required_docs = "Appointment letter, salary slips, bank statements showing salary deposit, termination letter, copy of grievance notice."
        elif category == "Tax Laws":
            required_docs = "FBR tax returns, withholding tax certificates, bank statements, transaction invoices, show-cause notices received."
        elif category == "Consumer Protection Laws":
            required_docs = "Purchase receipt/cash memo, warranty card, copy of the served 15-day legal notice, courier/postage receipt of the notice."
        elif category == "Constitutional Laws":
            required_docs = "Copy of the illegal order or action being challenged, representations sent to authorities, CNIC, supporting affidavit."
        else:
            required_docs = "All relevant agreements, CNIC, and proof of dispute/transactions."

        disclaimer = "Under Rule 7, this system provides legal information for educational purposes only. It does not constitute professional legal advice, court representation, or any legal guarantees."

        response = f"**Category (زمرہ)**: {category}\n\n"
        response += f"**Title**: {title}\n\n"
        response += f"**1. Direct Answer**:\n{direct_answer}\n\n"
        response += f"**2. Relevant Pakistani Law**:\n{answer_text} (Source: {statute} - {source})\n\n"
        response += f"**3. Practical Next Steps**:\n{next_steps}\n\n"
        response += f"**4. Required Documents**:\n{required_docs}\n\n"
        response += f"**5. Important Notes**:\n{disclaimer}"
        
        return response

    def run(self, query: str, category_focus: str = None) -> dict:
        """
        Runs the upgraded hybrid RAG pipeline with Category Lock and exact FYP Rules.
        """
        logger.info(f"Initiating RAG pipeline for query: '{query}' with category_focus: '{category_focus}'")
        
        # Clean text input
        cleaned_query = clean_text(query)
        
        # Detect input query language
        lang = detect_language(cleaned_query)
        logger.info(f"Detected query language: {lang}")
        
        # Translate to English for processing
        search_query = cleaned_query
        if lang == "urdu_script":
            search_query = translate_text(cleaned_query, sl="ur", tl="en")
        else:
            search_query = translate_text(cleaned_query, sl="auto", tl="en")
        logger.info(f"Translated query to English: '{search_query}'")
            
        # Clean search query
        search_query = clean_text(search_query)

        # Check if translation failed
        is_translation_failed = (lang in ["urdu_script", "roman_urdu"] and search_query == cleaned_query)

        if is_translation_failed:
            tokens = re.sub(r'[^\w\s\u0600-\u06ff]', ' ', cleaned_query.lower()).split()
            translated_words = []
            for token in tokens:
                if token in LOCAL_DICTIONARY:
                    translated_words.append(LOCAL_DICTIONARY[token])
            if translated_words:
                search_query += " " + " ".join(translated_words)

        # 1. Classify Category of the input query on both original query and translated query to maximize keyword matching accuracy
        classified_category = self.classifier.classify(cleaned_query + " " + search_query)
        logger.info(f"Classified category of query: '{classified_category}'")

        # 2. RULE 1: CATEGORY LOCK Check
        frontend_category_map = {
            "General": "Constitutional Laws",
            "Family Laws": "Family Laws",
            "Criminal Laws": "Criminal Laws",
            "Civil Laws": "Civil Laws",
            "Property Laws": "Property Laws",
            "Labour Laws": "Labour Laws",
            "Tax Laws": "Tax Laws",
            "Consumer Protection Laws": "Consumer Protection Laws",
            "Constitutional Laws": "Constitutional Laws",
            # Legacy frontend compatibility mappings
            "Family Law": "Family Laws",
            "Cyber Crime": "Criminal Laws",
            "Property Law": "Property Laws",
            "Tenant Rights": "Property Laws",
            "Consumer Rights": "Consumer Protection Laws",
            "Employment Law": "Labour Laws",
            "FIR & Police Complaints": "Criminal Laws",
            "Women Protection Laws": "Family Laws"
        }
        
        target_category = None
        if category_focus:
            target_category = frontend_category_map.get(category_focus, category_focus)

        # If the query belongs to another category, return the required prompt
        if target_category and classified_category != target_category and not is_translation_failed:
            text_lower = search_query.lower()
            scores = {cat: 0 for cat in self.classifier.rules.keys()}
            for cat, keywords in self.classifier.rules.items():
                for kw in keywords:
                    if re.search(r'\b' + re.escape(kw) + r'\b', text_lower):
                        scores[cat] += 1
            
            if scores.get(classified_category, 0) > 0:
                logger.warning(f"Category Lock triggered. User selected '{target_category}' but query belongs to '{classified_category}'")
                lock_reply = "This question belongs to another legal category. Please switch to the appropriate category to receive an accurate answer."
                
                if lang == "urdu_script":
                    lock_reply = translate_text(lock_reply, sl="en", tl="ur")
                    if lock_reply == "This question belongs to another legal category. Please switch to the appropriate category to receive an accurate answer.":
                        lock_reply = "یہ سوال کسی دوسری قانونی کیٹیگری سے تعلق رکھتا ہے۔ درست جواب حاصل کرنے کے لیے براہ کرم مناسب کیٹیگری پر جائیں۔"
                elif lang == "roman_urdu":
                    lock_reply = "Yeh sawal kisi doosri qanooni category se talluq rakhta hai. Sahi jawab ke liye baraye meherbani mutalliga category select karein."
                    
                return {
                    "category": classified_category,
                    "reply": lock_reply,
                    "sources": ["System Category Lock"],
                    "disclaimer": self.config["disclaimer"]
                }

        retrieval_category = target_category if target_category else classified_category

        # 3. Vector Database Retrieval
        if not self.index_loaded:
            self.index_loaded = self.vector_store.load_index()

        sub_records = []
        if self.index_loaded:
            sub_records = [meta for meta in self.vector_store.metadata if meta.get("category") == retrieval_category]
        
        if not sub_records:
            not_found_reply = "Information not found in the selected legal knowledge base."
            if lang == "urdu_script":
                not_found_reply = translate_text(not_found_reply, sl="en", tl="ur")
                if not_found_reply == "Information not found in the selected legal knowledge base.":
                    not_found_reply = "منتخب کردہ قانونی معلومات کے ذخیرے میں معلومات نہیں مل سکیں۔"
            elif lang == "roman_urdu":
                not_found_reply = "Selected legal knowledge base mein malomat nahi mil saki."
            return {
                "category": retrieval_category,
                "reply": not_found_reply,
                "sources": ["Dataset Boundary"],
                "disclaimer": self.config["disclaimer"]
            }

        # 4. Multi-Query Retrieval and Query Expansion
        # Identify trigger expansions from original query and translated search query
        expansions = get_query_expansions(cleaned_query + " " + search_query)
        logger.info(f"Query expansions identified: {expansions}")
        
        # Build search queries (Original query + combined expansions to keep it grounded in context)
        search_queries = [search_query]
        if expansions:
            search_queries.append(search_query + " " + " ".join(expansions))
        
        # Prepare BM25
        global_corpus = []
        for r in self.vector_store.metadata:
            q_text = r.get("question", "")
            kw_list = r.get("keywords", [])
            kw_text = " ".join(kw_list) if isinstance(kw_list, list) else str(kw_list)
            global_corpus.append(clean_text(f"{r.get('title', '')} {r.get('statute', '')} {q_text} {kw_text} {r.get('answer', '')}"))
        bm25 = BM25(global_corpus)
        
        # Track maximum scores for each sub-record across all queries
        record_scores = {r["id"]: {"record": r, "score": 0.0, "max_bm_score": 0.0} for r in sub_records}
        
        for q in search_queries:
            q_clean = clean_text(q)
            if not q_clean.strip():
                continue
                
            # Generate embedding for vector search
            query_vector = self.embeddings_mgr.encode(q_clean)
            
            # Retrieve vectors matching our target category
            vector_results = self.vector_store.search(query_vector, k=len(self.vector_store.metadata), category=retrieval_category)
            dist_map = {res_meta["id"]: distance for res_meta, distance in vector_results}
            
            # Tokenize for BM25
            query_tokens = bm25.tokenize(q_clean)
            
            for r in sub_records:
                dist = dist_map.get(r["id"], 999.0)
                vec_sim = 1.0 / (1.0 + dist)
                
                try:
                    global_idx = next(i for i, meta in enumerate(self.vector_store.metadata) if meta["id"] == r["id"])
                    bm_score = bm25.get_score(query_tokens, global_idx)
                except StopIteration:
                    bm_score = 0.0
                    
                bm_sim = bm_score / (bm_score + 1.0) if bm_score > 0 else 0.0
                hybrid_score = vec_sim * 0.5 + bm_sim * 0.5
                
                # Keep maximum score achieved across all search terms
                if hybrid_score > record_scores[r["id"]]["score"]:
                    record_scores[r["id"]]["score"] = hybrid_score
                if bm_score > record_scores[r["id"]]["max_bm_score"]:
                    record_scores[r["id"]]["max_bm_score"] = bm_score
                    
        # Rank sub-records by their highest score
        hybrid_results = [(info["record"], info["score"], info["max_bm_score"]) for info in record_scores.values()]
        hybrid_results.sort(key=lambda x: x[1], reverse=True)
        
        best_record, best_score, best_max_bm_score = hybrid_results[0]
        logger.info(f"Top Hybrid RAG Match ID: {best_record['id']} with Combined Score: {best_score} (Max BM25: {best_max_bm_score})")

        # 5. Relevance Guard (Intercept completely irrelevant/out-of-scope non-legal queries)
        text_lower = search_query.lower()
        has_urdu_legal_term = any(c in text_lower for c in ["قانون", "عدالت", "طلاق", "خلع", "نکاح", "شادی", "پولیس", "ایف آئی آر", "جائیداد", "زمین", "حقوق", "کیس", "عدت", "وکیل", "ضمانت", "سزا", "جرم", "معاہدہ", "نان و نفقہ"])
        has_roman_legal_term = any(w in text_lower for w in ["qanoon", "kanoon", "talaq", "talaaq", "khula", "nikah", "nikaah", "shadi", "shaadi", "adalat", "masla", "case", "court", "law", "police", "fir", "bail", "property", "zameen", "qabza", "tax", "fbr", "salary", "employer", "employee", "rights", "contract", "stay", "injunction", "gratuity", "wages", "accident", "theft", "murder", "arrest"])
        is_urdu_query = any(ord(c) >= 0x0600 and ord(c) <= 0x06FF for c in text_lower)

        keyword_score = 0
        for category, keywords in self.classifier.rules.items():
            for kw in keywords:
                if re.search(r'\b' + re.escape(kw) + r'\b', text_lower):
                    keyword_score += 1

        is_irrelevant = False
        if is_translation_failed:
            if is_urdu_query:
                is_irrelevant = not has_urdu_legal_term
            else:
                is_irrelevant = not has_roman_legal_term
        else:
            # Check if there are no matching keywords and a very low hybrid/BM25 score
            is_irrelevant = (keyword_score == 0 and best_score < 0.35)

        if is_irrelevant:
            logger.warning(f"Query '{query}' classified as irrelevant by Relevance Guard.")
            irrelevant_reply = "I am sorry, but I can only assist with Pakistani legal matters. Please ask a question related to Pakistani laws or select one of the legal categories."
            if lang == "urdu_script":
                irrelevant_reply = "معذرت، میں صرف پاکستانی قانونی معاملات میں مدد کر سکتا ہوں۔ براہ کرم پاکستانی قوانین سے متعلق سوال پوچھیں یا کسی قانونی کیٹیگری کا انتخاب کریں۔"
            elif lang == "roman_urdu":
                irrelevant_reply = "Maazrat, mein sirf Pakistani qanooni mamlat mein madad kar sakta hoon. Baraye meherbani Pakistani qanoon se mutalliq sawal poochein."
            
            return {
                "category": retrieval_category,
                "reply": irrelevant_reply,
                "sources": ["Relevance Guard"],
                "disclaimer": self.config["disclaimer"]
            }

        # 5.5 Low Confidence Rule (If no strong match is found, ask a focused clarification question)
        # Trigger fallback if BM25 score is very low (no keyword match) and hybrid score is not strongly confident,
        # or if the query contains absolutely no legal keywords or expansions.
        has_legal_keywords = (keyword_score > 0 or len(expansions) > 0 or has_urdu_legal_term or has_roman_legal_term)
        if (best_max_bm_score < 0.05 and best_score < 0.45) or not has_legal_keywords:
            logger.warning(f"Relevance check failed. Top score: {best_score} (Max BM25: {best_max_bm_score})")
            clarification = CLARIFYING_QUESTIONS.get(retrieval_category, {
                "en": "Could you please provide more details about your legal query?",
                "ur": "کیا آپ اپنے قانونی سوال کے بارے میں مزید تفصیلات فراہم کر سکتے ہیں؟",
                "roman": "Kya aap apne legal query ke baare mein mazeed details faraham kar sakte hain?"
            })
            
            fallback_reply = clarification.get(lang, clarification["en"])
            
            return {
                "category": retrieval_category,
                "reply": fallback_reply,
                "sources": ["Low Confidence Fallback"],
                "disclaimer": self.config["disclaimer"]
            }

        # 6. LLM / Fallback Response Generation
        self.load_llm()

        if self.generator is not None:
            try:
                system_prompt = (
                    "# SYSTEM PROMPT – PAKISTANI LEGAL ADVISOR AI\n\n"
                    "You are a Pakistani Legal Advisor AI.\n\n"
                    "Your purpose is to provide helpful, accurate, structured, and user-friendly legal guidance based ONLY on the legal information retrieved from the knowledge base.\n\n"
                    "You specialize in:\n\n"
                    "1. Family Laws\n"
                    "2. Criminal Laws\n"
                    "3. Civil Laws\n"
                    "4. Property Laws\n"
                    "5. Labour Laws\n"
                    "6. Tax Laws\n"
                    "7. Consumer Protection Laws\n"
                    "8. Constitutional Laws\n\n"
                    "---\n\n"
                    "## PRIMARY OBJECTIVE\n\n"
                    "Your goal is not simply to answer questions.\n\n"
                    "Your goal is to:\n\n"
                    "* Understand the user's actual legal problem.\n"
                    "* Use retrieved legal information.\n"
                    "* Explain the law in simple language.\n"
                    "* Provide practical guidance.\n"
                    "* Help the user understand possible legal options.\n"
                    "* Reduce confusion.\n"
                    "* Avoid legal jargon whenever possible.\n\n"
                    "Always focus on solving the user's legal issue.\n\n"
                    "---\n\n"
                    "## LANGUAGE RULES\n\n"
                    "Reply in the same language used by the user.\n\n"
                    "Examples:\n\n"
                    "* English question → English answer\n"
                    "* Urdu question → Urdu answer\n"
                    "* Roman Urdu question → Roman Urdu answer\n"
                    "* Mixed language question → Natural mixed language answer\n\n"
                    "Never force English when the user is communicating in Urdu or Roman Urdu.\n\n"
                    "---\n\n"
                    "## USER UNDERSTANDING RULES\n\n"
                    "Users may:\n\n"
                    "* Use spelling mistakes\n"
                    "* Use incomplete sentences\n"
                    "* Use informal language\n"
                    "* Use slang\n"
                    "* Use emotional wording\n"
                    "* Use Roman Urdu\n"
                    "* Ask vague questions\n\n"
                    "You must understand meaning and intent, not just keywords.\n\n"
                    "Examples:\n\n"
                    "\"Mera shohar kharcha nahi deta\"\n\n"
                    "Interpret as:\n"
                    "Family Law → Maintenance Issue\n\n"
                    "\"Boss salary nahi de raha\"\n\n"
                    "Interpret as:\n"
                    "Labour Law → Unpaid Wages\n\n"
                    "\"Meri zameen pe qabza ho gaya\"\n\n"
                    "Interpret as:\n"
                    "Property Law → Illegal Possession\n\n"
                    "\"Police ne pakar liya\"\n\n"
                    "Interpret as:\n"
                    "Criminal Law → Arrest / FIR Related Matter\n\n"
                    "Focus on the user's actual legal issue.\n\n"
                    "---\n\n"
                    "## KNOWLEDGE BASE RULES\n\n"
                    "Always prioritize retrieved legal information.\n\n"
                    "Use the retrieved legal records as the primary source of truth.\n\n"
                    "Do not invent laws.\n\n"
                    "Do not invent legal sections.\n\n"
                    "Do not fabricate court procedures.\n\n"
                    "Do not create legal rights that are not supported by retrieved information.\n\n"
                    "If the knowledge base does not contain sufficient information:\n\n"
                    "State that additional information may be required.\n\n"
                    "Do not guess.\n\n"
                    "---\n\n"
                    "## ANSWER GENERATION RULES\n\n"
                    "Generate practical and useful responses.\n\n"
                    "Avoid one-line answers.\n"
                    "Avoid generic responses.\n"
                    "Avoid repeating the same answer for different questions.\n\n"
                    "Every answer should be tailored to the user's situation.\n\n"
                    "---\n\n"
                    "## RESPONSE STRUCTURE\n\n"
                    "Whenever possible, follow this structure:\n\n"
                    "### Legal Category\n\n"
                    "Identify the relevant legal category.\n\n"
                    "Example:\n\n"
                    "Category: Property Law\n\n"
                    "---\n\n"
                    "### Direct Answer\n\n"
                    "Provide a clear answer to the user's question immediately.\n\n"
                    "Do not make the user read multiple paragraphs before understanding the answer.\n\n"
                    "---\n\n"
                    "### Relevant Pakistani Law\n\n"
                    "Explain the applicable legal principles using the retrieved information.\n\n"
                    "Use simple language.\n"
                    "Avoid unnecessary legal complexity.\n\n"
                    "---\n\n"
                    "### Practical Next Steps\n\n"
                    "Explain what actions the user may take.\n\n"
                    "Examples:\n\n"
                    "* File a complaint\n"
                    "* Approach relevant authority\n"
                    "* Contact police\n"
                    "* Approach Family Court\n"
                    "* Approach Civil Court\n"
                    "* Approach Labour Court\n"
                    "* Contact FBR\n"
                    "* Seek legal counsel\n\n"
                    "Only mention actions supported by retrieved information.\n\n"
                    "---\n\n"
                    "### Required Documents\n\n"
                    "If applicable, list useful documents.\n\n"
                    "Examples:\n\n"
                    "* CNIC\n"
                    "* Nikahnama\n"
                    "* FIR Copy\n"
                    "* Registry\n"
                    "* Mutation\n"
                    "* Employment Contract\n"
                    "* Salary Slips\n"
                    "* Tax Records\n"
                    "* Receipts\n"
                    "* Warranty Documents\n\n"
                    "Only include documents relevant to the user's issue.\n\n"
                    "---\n\n"
                    "### Additional Information Needed\n\n"
                    "If the question is incomplete, ask focused follow-up questions.\n\n"
                    "Examples:\n\n"
                    "* Which province is the property located in?\n"
                    "* Was there a written agreement?\n"
                    "* Has an FIR already been registered?\n"
                    "* Are you a tenant or owner?\n\n"
                    "Ask only necessary questions.\n\n"
                    "Do not ask multiple unnecessary questions.\n\n"
                    "---\n\n"
                    "### Important Note\n\n"
                    "Mention important limitations or cautions.\n\n"
                    "Examples:\n\n"
                    "* Outcomes depend on facts and evidence.\n"
                    "* Court decisions depend on case-specific circumstances.\n"
                    "* Additional legal review may be required.\n\n"
                    "Keep this brief.\n\n"
                    "---\n\n"
                    "## CONFIDENCE RULE\n\n"
                    "If retrieved information is weak, unclear, or insufficient:\n\n"
                    "DO NOT GUESS.\n\n"
                    "Instead:\n\n"
                    "* Explain what information is missing.\n"
                    "* Ask a clarifying question.\n"
                    "* Request additional facts.\n\n"
                    "Accuracy is more important than completeness.\n\n"
                    "---\n\n"
                    "## HALLUCINATION PREVENTION RULE\n\n"
                    "Never:\n\n"
                    "* Invent legal provisions.\n"
                    "* Invent court powers.\n"
                    "* Invent penalties.\n"
                    "* Invent procedures.\n"
                    "* Invent legal rights.\n\n"
                    "Only use information supported by retrieved legal records.\n\n"
                    "---\n\n"
                    "## PROFESSIONAL TONE\n\n"
                    "Be:\n\n"
                    "* Helpful\n"
                    "* Respectful\n"
                    "* Neutral\n"
                    "* Professional\n"
                    "* Easy to understand\n\n"
                    "Do not be robotic.\n"
                    "Do not sound like a textbook.\n"
                    "Do not provide emotional opinions.\n"
                    "Do not take sides.\n\n"
                    "Provide clear legal guidance in plain language.\n\n"
                    "---\n\n"
                    "## FINAL CHECK BEFORE RESPONDING\n\n"
                    "Before generating the answer verify:\n\n"
                    "1. Did I understand the user's issue?\n"
                    "2. Did I use retrieved legal information?\n"
                    "3. Is the answer relevant to the question?\n"
                    "4. Is the answer practical and actionable?\n"
                    "5. Did I avoid unsupported assumptions?\n"
                    "6. Did I ask for clarification if needed?\n\n"
                    "Only then provide the final response."
                )

                prompt = (
                    f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n"
                    f"{system_prompt}\n\n"
                    f"Retrieved Document Context (Knowledge Base):\n"
                    f"Category: {retrieval_category}\n"
                    f"Title: {best_record.get('title')}\n"
                    f"Statute: {best_record.get('statute')}\n"
                    f"Content: {best_record.get('answer')}\n"
                    f"<|eot_id|><|start_header_id|>user<|end_header_id|>\n"
                    f"Query: {search_query}\n"
                    f"<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n"
                )
                output = self.generator(prompt)
                generated_text = output[0]["generated_text"].replace(prompt, "").strip()
                reply = generated_text
            except Exception as e:
                logger.error(f"Error running LLM: {str(e)}. Compiling response programmatically.")
                reply = self.format_structured_response(search_query, retrieval_category, best_record)
        else:
            reply = self.format_structured_response(search_query, retrieval_category, best_record)

        # 7. Localization Post-Processing
        final_reply = reply
        final_disclaimer = self.config["disclaimer"]
        
        if lang == "urdu_script":
            logger.info("Translating final structured response into Urdu script...")
            translated_reply, _ = translate_to_urdu_and_roman(reply)
            if translated_reply == reply:
                # Offline fallback
                record_title = best_record.get("title", "")
                final_reply = LOCAL_RECORD_TRANSLATIONS.get(record_title, {}).get("ur", LOCAL_TRANSLATIONS.get(retrieval_category, {}).get("ur", reply))
            else:
                final_reply = translated_reply
            final_disclaimer = translate_text(self.config["disclaimer"], sl="en", tl="ur")
            if final_disclaimer == self.config["disclaimer"]:
                final_disclaimer = "یہ اے آئی سسٹم صرف معلوماتی قانونی رہنمائی فراہم کرتا ہے اور پیشہ ورانہ قانونی مشورے کا متبادل نہیں ہے۔"
            
        elif lang == "roman_urdu":
            logger.info("Translating final structured response into Roman Urdu...")
            _, translated_roman = translate_to_urdu_and_roman(reply)
            if translated_roman == reply:
                # Offline fallback
                record_title = best_record.get("title", "")
                final_reply = LOCAL_RECORD_TRANSLATIONS.get(record_title, {}).get("roman", LOCAL_TRANSLATIONS.get(retrieval_category, {}).get("roman", reply))
            else:
                final_reply = translated_roman
            final_disclaimer = "Yeh AI system sirf malomati kanooni rehnumai faraham karta hai aur peshawarana kanooni mashwaray ka badal nahi hai."

        return {
            "category": retrieval_category,
            "reply": final_reply,
            "sources": [best_record.get("source", "Constitution and Statutes of Pakistan")],
            "disclaimer": final_disclaimer
        }
