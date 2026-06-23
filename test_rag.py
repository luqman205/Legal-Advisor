import sys
import os

from legal_ai.backend.rag_pipeline import RAGPipeline

def main():
    print("Initializing RAGPipeline...")
    pipeline = RAGPipeline()
    
    query = "Malik Makan Ne Mujhe Ghar Se Nikal Diya Hai To Mere rights kya hai?"
    print(f"\nRunning query: '{query}'")
    
    response = pipeline.run(query)
    print("\nResponse Category:", response.get("category"))
    print("\nResponse Reply:\n", response.get("reply"))

if __name__ == "__main__":
    main()
