const CLASSIFICATION_RULES = {
  "Constitutional Laws": [
    "constitution", "constitutional", "article", "fundamental right", "supreme court", 
    "high court", "writ", "petition", "suo motu", "senate", "parliament", "national assembly", 
    "president", "prime minister", "justice of peace", "fundamental rights", "habeas corpus", 
    "mandamus", "prohibition", "certiorari", "quo warranto", "legislation", "act of parliament",
    "amendment", "state of pakistan"
  ],
  "Family Laws": [
    "divorce", "khula", "talaq", "maintenance", "iddat", "dowry", "dower", "nikah", 
    "custody", "guardian", "marriage", "domestic violence", "court marriage", "spouse",
    "ward", "union council", "dower amount", "shariah", "dissolution of marriage", "bride",
    "wife", "husband", "children", "minor", "visitation"
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
    "malik makan", "kirayedar", "kiraya", "makan", "ghar se nikal"
  ],
  "Criminal Laws": [
    "fir", "police", "arrest", "false fir", "bail", "thana", "sho", "complaint", 
    "refusal", "remand", "custodial", "crpc", "cognizable", "pre-arrest bail", 
    "post-arrest bail", "section 22", "theft", "mischief", "murder", "assault", "conspiracy",
    "forgery", "penal code", "ppc", "criminal", "stolen", "perpetrator",
    "302", "489-f", "497", "498", "cnsa", "peca", "self-defense", "private defense", 
    "kidnapping", "abduction", "defamation", "ransom", "fraud", "trust", "trespass", 
    "narcotics", "harassment", "drugs", "rape", "cheating", "cyber"
  ],
  "Consumer Protection Laws": [
    "consumer", "refund", "faulty", "fake product", "damaged item", "warranty", 
    "consumer court", "online store scam", "expiry date", "defective goods", 
    "unfair trade", "misleading advertisement", "receipt", "deficient service", "replacement",
    "defective", "substandard", "negligence", "invoice", "overcharging", "notice", "frivolous"
  ],
  "Labour Laws": [
    "salary", "employer", "termination", "contract", "wrongful termination", 
    "overtime", "gratuity", "pension", "provident fund", "labor court", "wages", 
    "resignation", "severance", "employment agreement", "notice period", "workplace",
    "employee", "worker", "maternity", "social security", "pessi", "sessi", "eobi",
    "working hours", "weekly holiday", "paid leave", "sick leave", "workplace safety",
    "occupational health", "workmen compensation", "child labor", "trade union", "cba"
  ],
  "Tax Laws": [
    "tax", "income tax", "sales tax", "fbr", "tax return", "tax assessment", 
    "default surcharge", "filing return", "audit", "tax tribunal", "withholding",
    "invoice", "taxpayer", "revenue board", "inland revenue",
    "wht", "surcharge", "atl", "customs", "excise", "provincial", "cgt",
    "filer", "non-filer", "adrc", "pra", "srb", "kpra", "bra"
  ],
  "Civil Laws": [
    "civil", "specific relief", "specific performance", "injunction", "stay order", 
    "declaratory", "declaration", "specific performance of contract", "indemnity",
    "arbitration", "contract act", "void contract", "voidable contract", "void agreement",
    "guarantee", "surety", "principal debtor", "bailment", "pledge", "agency", "principal and agent",
    "cancellation of deed", "rectification of contract", "civil court", "pecuniary jurisdiction",
    "territorial jurisdiction", "plaint", "written statement", "summons", "execution of decree",
    "civil appeal", "revision petition", "review petition", "limitation period", "limitation act",
    "cpc", "civil procedure"
  ]
};

const CLASSIFICATION_TRIGGERS = {
  "Property Laws": [
    "qabza", "kabza", "kabja", "qabzah", "kabzah", "qabzaa", "zameen", "jameen", "zamin", "jamin", "plot", "property", "registry", "intiqal", "diwar", "boundary", "warasat", "virasat", "malik makan", "malikmakan", "kirayedar", "kirayedaar", "kiraya", "makan", "ghar",
    "قبضہ", "قبضے", "زمین", "پلاٹ", "پراپرٹی", "جائیداد", "جائداد", "رجسٹری", "انتقال", "دیوار", "حدود", "وراثت", "مالک مکان", "کرایہ دار", "کرائے دار", "کرایہ", "مکان", "گھر",
    "land", "possession", "encroachment", "mutation", "inheritance", "partition", "tenancy", "tenant", "landlord", "rent", "eviction", "house"
  ],
  "Family Laws": [
    "talaq", "talaaq", "khula", "kula", "shohar", "shoher", "biwi", "beewi", "nikah", "nikaah", "bachay", "kharcha", "kharja", "nafaqa", "custody", "shadi", "shaadi", "khawand", "bache", "larki", "larka", "aurat", "mard",
    "طلاق", "خلع", "شوہر", "بیوی", "نکاح", "بچے", "بچوں", "بچہ", "خرچہ", "نفقہ", "کسٹڈی", "شادی", "خاوند", "اولاد", "تحویل", "سرپرستی",
    "divorce", "dissolution", "marriage", "maintenance", "dower", "dowry", "nikahnama", "guardianship", "husband", "wife", "children", "minor", "spouse", "visitation"
  ],
  "Criminal Laws": [
    "fir", "police", "arrest", "giraftar", "qatl", "chori", "fraud", "dhamki", "thana", "sho", "bail", "zamanat", "saza", "jurm",
    "ایف آئی آر", "پولیس", "گرفتار", "گرفتاری", "قتل", "چوری", "فراڈ", "دھمکی", "تھانہ", "ضمانت", "سزا", "جرم",
    "murder", "theft", "stolen", "cheating", "threat", "intimidation", "assault", "complaint", "criminal", "ppc", "crpc", "forgery"
  ],
  "Civil Laws": [
    "contract", "agreement", "paisay", "qarz", "recovery", "harjana", "muahida", "stay", "injunction",
    "معاہدہ", "اقرار نامہ", "اقرارنامہ", "پیسے", "قرض", "ریکوری", "ہرجانہ", "سٹے", "حکم امتناعی", "منسوخی",
    "money", "debt", "damages", "compensation", "stay order", "breach", "civil suit", "specific performance"
  ],
  "Labour Laws": [
    "salary", "tankhwa", "employer", "boss", "overtime", "job", "dismissal", "termination", "mulazmat", "naukri", "gratuity", "pension", "eobi",
    "تنخواہ", "مالک", "ملازمت", "نوکری", "برطرفی", "گریجویٹی", "پنشن", "ملازم", "آجر", "اوور ٹائم", "اوورٹائم",
    "wages", "worker", "wrongful termination", "dismissal", "labor court", "labour court", "employment"
  ],
  "Tax Laws": [
    "tax", "fbr", "filer", "non filer", "ntn", "return",
    "ٹیکس", "ایف بی آر", "فائلر", "نان فائلر", "این ٹی این", "ریٹرن", "گوشوارہ",
    "withholding", "wht", "income tax", "sales tax", "audit", "taxpayer"
  ],
  "Consumer Protection Laws": [
    "refund", "warranty", "online shopping", "defective product", "fake product", "raseed", "bill",
    "ریفنڈ", "وارنٹی", "آن لائن خریداری", "ناقص مصنوعات", "ناقص اشیاء", "نقلی", "فیک", "رسید", "بل",
    "replacement", "defective", "fake", "misleading", "consumer", "invoice", "overcharging"
  ],
  "Constitutional Laws": [
    "fundamental rights", "constitutional rights", "government", "freedom", "speech", "privacy", "sarkari", "idara",
    "بنیادی حقوق", "آئینی حقوق", "آئین", "دستور", "حکومت", "آزادی", "تقریر", "اظهار رائے", "پرائیویسی",
    "constitutional", "constitution", "freedom of speech", "writ petition", "judicial review", "article 199"
  ]
};

function classifyQuery(text) {
  const textLower = text.toLowerCase();
  const scores = {};
  
  for (const [category, keywords] of Object.entries(CLASSIFICATION_RULES)) {
    scores[category] = 0;
    const combinedKeywords = Array.from(new Set([...keywords, ...(CLASSIFICATION_TRIGGERS[category] || [])]));
    for (const kw of combinedKeywords) {
      const regex = new RegExp('(?<![\\p{L}\\p{N}_])' + kw.replace(/[\\^$*+?.()|[\]{}]/g, '\\$&') + '(?![\\p{L}\\p{N}_])', 'iu');
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
  return { category: bestCategory, score: maxScore };
}

console.log("Classification result for 'shohar kharcha nahi deta':");
console.log(classifyQuery("shohar kharcha nahi deta"));
