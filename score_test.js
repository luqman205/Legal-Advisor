const fs = require('fs');
const path = require('path');

// Ported cleanText and BM25 from route.ts
function cleanText(text) {
  if (!text) return "";
  return text.replace(/[^\p{L}\p{N}\s\.,\?\-–]/gu, ' ').replace(/\s+/g, ' ').trim();
}

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
    const stopWords = new Set([
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
    return text.toLowerCase()
      .replace(/[^\p{L}\p{N}\s]/gu, ' ')
      .split(/\s+/)
      .filter(w => w && !stopWords.has(w));
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

// Load dataset
const filePath = '/Users/mac/Documents/legal advisor/legal_ai/dataset/legal_dataset.json';
if (!fs.existsSync(filePath)) {
  console.error("Dataset not found at " + filePath);
  process.exit(1);
}

const dataset = JSON.parse(fs.readFileSync(filePath, 'utf8'));
console.log(`Loaded dataset of size: ${dataset.length}`);

const searchQuery = "Can a man legally contract a second marriage in Pakistan?";
const cleanedSearchQuery = cleanText(searchQuery);

// Filter family law records
const subRecords = dataset.filter(r => r.category === "Family Laws");
console.log(`Filtered sub-records in Family Laws: ${subRecords.length}`);

const corpusTexts = dataset.map(r => {
  const qText = r.question || '';
  const kwText = r.keywords ? (Array.isArray(r.keywords) ? r.keywords.join(' ') : String(r.keywords)) : '';
  return cleanText(`${r.title || ''} ${r.statute || ''} ${qText} ${kwText} ${r.answer || ''}`);
});

const bm25 = new BM25(corpusTexts);
const queryTokens = bm25.tokenize(cleanedSearchQuery);
console.log("Query tokens:", queryTokens);

const scoredRecords = subRecords.map((record) => {
  const globalIdx = dataset.findIndex(r => r.id === record.id);
  const score = globalIdx !== -1 ? bm25.getScore(queryTokens, globalIdx) : 0.0;
  return { record, score };
});

scoredRecords.sort((a, b) => b.score - a.score);

console.log("\nTop 5 matches:");
scoredRecords.slice(0, 5).forEach((item, idx) => {
  console.log(`\n--- Match #${idx + 1} (Score: ${item.score.toFixed(4)}) ---`);
  console.log(`ID: ${item.record.id}`);
  console.log(`Title: ${item.record.title}`);
  console.log(`Question: ${item.record.question}`);
});
