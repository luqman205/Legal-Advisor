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
  ]
};

const CLARIFYING_QUESTIONS = {
  "Family Laws": {
    ur: "کیا آپ کا نکاح نامہ رجسٹرڈ ہے؟ اور کیا آپ نان و نفقہ (خرچہ)، خلع، یا بچوں کی کسٹڈی کے بارے میں پوچھ رہے ہیں؟",
    roman: "Kya aap ka Nikahnama registered hai? Aur kya aap maintenance (kharcha), Khula, ya child custody ke baare mein pooch rahe hain?",
    en: "Is the marriage registered with a Nikahnama? Are you seeking maintenance, Khula, child custody, or divorce?"
  }
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

const getMockAIResponse = (userQuery, category) => {
  const q = userQuery.toLowerCase();
  
  // Detect Language
  const isUrduScript = /[\u0600-\u06FF]/.test(userQuery);
  const romanUrduWords = [
    "hai", "hain", "aur", "ko", "se", "ka", "ki", "ke", "mein", "me", "kya", "kiya", "nahi", "nahin", 
    "hota", "hote", "hoti", "hoga", "hogi", "hogay", "tha", "thi", "the", "par", "pe", "per", "ya", 
    "agar", "ho", "krna", "karna", "kr", "kar", "rha", "raha", "rahi", "rhe", "rahe", "hun", "hoon", 
    "he", "sath", "saath", "liye", "liya", "diya", "de", "do", "ek", "aik", "puchna", "bolna", 
    "smjh", "samajh", "chahiye", "kuch", "kuchh", "bare", "barey", "karta", "kartay", 
    "karti", "khatam", "shuru", "nikaah", "nikah", "shadi", "talaq", "khula", "masla", "qanoon", 
    "kanoon", "adalat", "mujhe", "mujh", "mera", "meri", "mere", "tum", "tumhara", "aap", "aapka", 
    "apka", "apki", "aapki", "bhai", "behan", "abbu", "ammi", "walid", "walida", "bacha", "bache", 
    "larki", "larka", "aurat", "mard", "khawateen", "shohar", "biwi", "talaaq", "zameen", "ghar", "bhi"
  ];
  const words = q.split(/\s+/);
  const romanMatches = words.filter(w => romanUrduWords.includes(w)).length;
  const isRomanUrdu = romanMatches > 1 || (words.length <= 4 && romanMatches >= 1);
  
  const lang = isUrduScript ? "ur" : (isRomanUrdu ? "roman" : "en");
  
  const validCategories = [
    "Constitutional Laws", "Family Laws", "Criminal Laws", "Civil Laws",
    "Property Laws", "Labour Laws", "Tax Laws", "Consumer Protection Laws"
  ];

  const classified = classifyQuery(userQuery);
  
  if (category && validCategories.includes(category) && classified.category !== category && classified.score > 0) {
    if (lang === "ur") {
      return `**Category (زمرہ)**: ${classified.category}
**Warning (انتباہ)**:
یہ سوال کسی اور قانونی زمرے سے تعلق رکھتا ہے۔ درست جواب حاصل کرنے کے لیے براہ کرم مناسب زمرے میں جائیں۔`;
    } else if (lang === "roman") {
      return `**Category (زمرہ)**: ${classified.category}
**Warning (انتباہ)**:
Yeh sawal kisi doosri qanooni category se talluq rakhta hai. Sahi jawab ke liye baraye meherbani mutalliga category select karein.`;
    } else {
      return `**Category (زمرہ)**: ${classified.category}
**Warning (انتباہ)**:
This question belongs to another legal category. Please switch to the appropriate category to receive an accurate answer.`;
    }
  }

  return "Standard response details...";
};

console.log("Mock Response result:");
console.log(getMockAIResponse("shohar kharcha nahi deta", "Constitutional Laws"));
