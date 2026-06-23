import fs from "fs";
import path from "path";

export const dynamic = "force-dynamic";

async function testQuery(message: string, categoryFocus: string | null = null) {
  try {
    const response = await fetch('http://localhost:3000/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, category: categoryFocus })
    });
    
    if (!response.ok) {
      return { query: message, status: response.status, error: await response.text() };
    }
    
    return { query: message, data: await response.json() };
  } catch (error: any) {
    return { query: message, error: error.message };
  }
}

export default async function TestPage() {
  const results: any[] = [];
  
  results.push(await testQuery("طلاق دینے کا قانونی طریقہ کیا ہے؟"));
  results.push(await testQuery("نکاح کے لیے قانونی عمر کیا ہے؟"));
  results.push(await testQuery("nikah ki qanooni umar kya hai?"));
  results.push(await testQuery("shohar kharcha nahi deta"));
  
  const outputPath = path.join(process.cwd(), "family_law_details.txt");
  fs.writeFileSync(outputPath, JSON.stringify(results, null, 2), "utf8");

  return (
    <div style={{ padding: 20, fontFamily: "monospace", color: "white", backgroundColor: "black" }}>
      <h1>Verification results written to family_law_details.txt</h1>
      <pre>{JSON.stringify(results, null, 2)}</pre>
    </div>
  );
}
