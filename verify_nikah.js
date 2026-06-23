async function testQuery(message, categoryFocus = null) {
  console.log(`\n----------------------------------------`);
  console.log(`Query: "${message}"${categoryFocus ? ` (Category Focus: ${categoryFocus})` : ''}`);
  
  try {
    const response = await fetch('http://127.0.0.1:3000/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, category: categoryFocus })
    });
    
    if (!response.ok) {
      console.error(`Status Error: ${response.status}`);
      const text = await response.text();
      console.error(text);
      return;
    }
    
    const result = await response.json();
    console.log(`Category: ${result.category}`);
    console.log(`Sources: ${JSON.stringify(result.sources)}`);
    console.log(`Reply (first 300 chars): \n${result.reply.substring(0, 300)}...`);
  } catch (error) {
    console.error(`Fetch Error: ${error.message}`);
  }
}

async function run() {
  await testQuery("نکاح کے لیے قانونی عمر کیا ہے؟");
  await testQuery("nikah ki qanooni umar kya hai?");
  await testQuery("legal age of marriage");
}

run();
