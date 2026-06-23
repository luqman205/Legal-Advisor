const fs = require('fs');
const path = require('path');

function copyDir(src, dest) {
  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }
  const entries = fs.readdirSync(src, { withFileTypes: true });
  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.name === '__pycache__' || entry.name === 'node_modules' || entry.name === '.git') {
      continue;
    }
    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

try {
  copyDir('./legal_ai/backend', '/Users/mac/.gemini/antigravity-ide/scratch/legal_ai/backend');
  fs.copyFileSync('./verify_python_rag.py', '/Users/mac/.gemini/antigravity-ide/scratch/verify_python_rag.py');
  
  const vdbDir = '/Users/mac/.gemini/antigravity-ide/scratch/legal_ai/vector_db';
  if (!fs.existsSync(vdbDir)) {
    fs.mkdirSync(vdbDir, { recursive: true });
  }
  fs.copyFileSync('/Users/mac/.gemini/antigravity-ide/scratch/faiss_index.bin.npy', path.join(vdbDir, 'faiss_index.bin.npy'));
  fs.copyFileSync('/Users/mac/.gemini/antigravity-ide/scratch/faiss_index.bin.meta', path.join(vdbDir, 'faiss_index.bin.meta'));
  
  console.log("SUCCESSFULLY COPIED ALL UPDATED FILES TO SCRATCH!");
} catch (e) {
  console.error("Copy failed:", e);
}
