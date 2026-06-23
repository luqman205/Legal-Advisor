const fs = require('fs');
const path = require('path');

const scratchDir = '/Users/mac/.gemini/antigravity-ide/scratch';

function splitFile(filename, chunkSize = 1024 * 1024) { // 1MB chunks
  const filepath = path.join(scratchDir, filename);
  if (!fs.existsSync(filepath)) {
    console.log(`File does not exist: ${filepath}`);
    return;
  }
  const content = fs.readFileSync(filepath, 'utf8');
  const totalLength = content.length;
  let offset = 0;
  let chunkIdx = 0;
  
  while (offset < totalLength) {
    const chunk = content.substring(offset, offset + chunkSize);
    const chunkPath = path.join(scratchDir, `${filename}.chunk_${chunkIdx}`);
    fs.writeFileSync(chunkPath, chunk, 'utf8');
    console.log(`Wrote chunk ${chunkIdx} of size ${chunk.length} to ${chunkPath}`);
    offset += chunkSize;
    chunkIdx++;
  }
  console.log(`Splitting of ${filename} complete. Total chunks: ${chunkIdx}`);
}

splitFile('legal_dataset.json');
splitFile('legal_dataset.csv');
