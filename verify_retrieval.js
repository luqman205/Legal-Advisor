const fs = require('fs');

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
  constructor(corpus, k1 = 1.5, b = 0.75) {
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

  tokenize(text) {
    return text.toLowerCase()
      .replace(/[^\p{L}\p{N}\s]/gu, ' ')
      .split(/\s+/)
      .filter(w => w && !BM25_STOP_WORDS.has(w));
  }

  getScore(queryTokens, docIdx) {
    let score = 0.0;
    const docTokens = this.corpus[docIdx];
    const docLen = this.docLengths[docIdx];
    
    const wordCounts = {};
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

function cleanText(text) {
  if (!text) return "";
  return text.replace(/[^\p{L}\p{N}\s\.,\?\-–⚖️]/gu, ' ').replace(/\s+/g, ' ').trim();
}

const LOCAL_DICTIONARY = {
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
  "چوری": "theft stolen"
};

const EXPANSION_RULES = [
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
    triggers: ["khacha", "nafaqa", "maintenance", "expenses", "خرچہ", "نفقہ"], // wait, typo "khacha" in rule? Let's check
    expansions: ["child maintenance", "wife maintenance", "expenses allowance"]
  }
];

function getQueryExpansions(text) {
  const textLower = text.toLowerCase();
  const expansions = [];
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

// Main logic simulation
const dataset = JSON.parse(fs.readFileSync('legal_ai/dataset/legal_dataset.json', 'utf8'));

// Build BM25 index on whole corpus
const corpusTexts = dataset.map(r => {
  const qText = r.question || '';
  const kwText = r.keywords ? (Array.isArray(r.keywords) ? r.keywords.join(' ') : String(r.keywords)) : '';
  return cleanText(`${r.title || ''} ${r.statute || ''} ${qText} ${kwText} ${r.answer || ''}`);
});
const bm25 = new BM25(corpusTexts);

const idToIndex = new Map();
for (let i = 0; i < dataset.length; i++) {
  idToIndex.set(dataset[i].id, i);
}

const message = "طلاق دینے کا قانونی طریقہ کیا ہے؟";
console.log("Original Message:", message);

const cleanedMessage = cleanText(message);
const lang = 'urdu_script'; // Offline scenario where it remains urdu_script

let searchQuery = cleanedMessage; // Simulate translation failure where searchQuery = cleanedMessage
const isTranslationFailed = true;

if (isTranslationFailed) {
  const tokens = cleanedMessage.toLowerCase()
    .replace(/[^\p{L}\p{N}\s]/gu, ' ')
    .split(/\s+/)
    .filter(w => w);
  
  const translatedWords = [];
  for (const token of tokens) {
    if (LOCAL_DICTIONARY[token]) {
      translatedWords.push(LOCAL_DICTIONARY[token]);
    }
  }
  
  if (translatedWords.length > 0) {
    searchQuery += " " + translatedWords.join(" ");
  }
}

console.log("Search Query after Local Dictionary:", searchQuery);

const targetCategory = "Family Laws";
const subRecords = dataset.filter(r => r.category === targetCategory);

const expansions = getQueryExpansions(cleanedMessage + " " + searchQuery);
console.log("Expansions:", expansions);

const searchQueries = [searchQuery];
if (expansions.length > 0) {
  searchQueries.push(searchQuery + " " + expansions.join(" "));
}

console.log("All Search Queries:", searchQueries);

const recordScores = {};
for (const r of subRecords) {
  recordScores[r.id] = { record: r, score: 0.0 };
}

for (const q of searchQueries) {
  const qClean = cleanText(q);
  const queryTokens = bm25.tokenize(qClean);
  console.log(`Query: "${qClean}" -> Tokens:`, queryTokens);

  for (const record of subRecords) {
    const globalIdx = idToIndex.get(record.id);
    const score = (globalIdx !== undefined) ? bm25.getScore(queryTokens, globalIdx) : 0.0;
    if (score > recordScores[record.id].score) {
      recordScores[record.id].score = score;
    }
  }
}

const scoredRecords = Object.values(recordScores);
scoredRecords.sort((a, b) => b.score - a.score);

console.log("\nTop 5 Matched Records:");
for (let i = 0; i < Math.min(5, scoredRecords.length); i++) {
  console.log(`${i+1}. Title: "${scoredRecords[i].record.title}" | Score: ${scoredRecords[i].score.toFixed(4)}`);
}
