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
    console.log(`Reply: ${result.reply}`);
  } catch (error) {
    console.error(`Fetch Error: ${error.message}`);
  }
}

async function runTests() {
  console.log("Running API tests...");
  
  // Test Case 1: Urdu script query matching Property trigger
  await testQuery("میری زمین پر قبضہ ہو گیا ہے");
  
  // Test Case 2: Roman Urdu query matching Family trigger
  await testQuery("shohar kharcha nahi deta");
  
  // Test Case 2b: Roman Urdu query matching Family trigger under Constitutional Laws focus (Category Lock test)
  await testQuery("shohar kharcha nahi deta", "Constitutional Laws");
  
  // Test Case 3: Low confidence query under Family Laws focus
  await testQuery("I want help in Lahore", "Family Laws");
  
  // Test Case 4: Low confidence query under Property Laws focus
  await testQuery("I want help in Lahore", "Property Laws");
  
  // Test Case 5: Irrelevant query
  await testQuery("how to bake a cake");
}

runTests();
