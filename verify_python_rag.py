import sys
import os

# Add current directory to python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from legal_ai.backend.rag_pipeline import RAGPipeline
from legal_ai.backend.category_classifier import CategoryClassifier

def test_rag():
    print("=== RUNNING PYTHON RAG PIPELINE VERIFICATION ===")
    
    # 1. Test classifier
    classifier = CategoryClassifier()
    test_queries = [
        ("consumer court legal notice template", "Consumer Protection Laws"),
        ("defective online product refund", "Consumer Protection Laws"),
        ("what is the price limit for consumer court", "Consumer Protection Laws"),
        ("negligent service provider dry cleaner tailor", "Consumer Protection Laws")
    ]
    
    print("\n--- Testing Classifier ---")
    classifier_passed = True
    for query, expected in test_queries:
        result = classifier.classify(query)
        print(f"Query: '{query}' -> Classified: '{result}' (Expected: '{expected}')")
        if result != expected:
            print("❌ FAILED")
            classifier_passed = False
        else:
            print("✅ SUCCESS")
            
    # 2. Test RAGPipeline
    print("\n--- Testing RAG Pipeline Retrieval ---")
    pipeline = RAGPipeline()
    
    rag_queries = [
        "consumer court legal notice template",
        "defective online product refund",
        "warranty card guarantee honor shop",
        "price gouging retail price overcharge"
    ]
    
    rag_passed = True
    for query in rag_queries:
        print(f"\nQuery: '{query}'")
        try:
            res = pipeline.run(query)
            print(f"Classified Category: {res.get('category')}")
            reply = res.get('reply', '')
            print(f"Response snippet: {reply[:120]}...")
            print(f"Sources: {res.get('sources')}")
            if res.get('category') != "Consumer Protection Laws":
                print("❌ FAILED: Incorrect category classification in RAG run")
                rag_passed = False
            else:
                print("✅ SUCCESS")
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            rag_passed = False
            
    if classifier_passed and rag_passed:
        print("\n🎉 ALL PYTHON BACKEND RAG TESTS PASSED SUCCESSFULLY!")
        sys.exit(0)
    else:
        print("\n⚠️ SOME PYTHON BACKEND RAG TESTS FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    test_rag()
