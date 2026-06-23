import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from legal_ai.backend.rag_pipeline import RAGPipeline

def run_tests():
    pipeline = RAGPipeline()
    
    queries = [
        "نکاح کے لیے قانونی عمر کیا ہے؟",
        "nikah ki qanooni umar kya hai?",
        "legal age of marriage"
    ]
    
    for q in queries:
        print(f"\nQuery: '{q}'")
        try:
            res = pipeline.run(q)
            print(f"Category: {res.get('category')}")
            print(f"Sources: {res.get('sources')}")
            print(f"Reply Title: {res.get('reply').splitlines()[2] if len(res.get('reply').splitlines()) > 2 else ''}")
            print(f"Reply snippet: {res.get('reply')[:200]}...")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run_tests()
