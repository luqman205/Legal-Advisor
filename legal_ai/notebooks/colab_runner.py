# ==============================================================================
#                      GOOGLE COLAB COMPATIBLE RUNNER SCRIPT
# ==============================================================================
# This script contains the exact copy-paste friendly python cells for Google Colab
# to run the Pakistani Legal Advisor RAG system.
# ==============================================================================

"""
# CELL 1: Install Dependencies
!pip install fastapi uvicorn pydantic sentence-transformers faiss-cpu transformers torch pandas python-multipart

# CELL 2: Clone/Write Backend files or run training pipeline
# You can copy the code from:
# - legal-ai/backend/utils.py
# - legal-ai/backend/dataset_generator.py
# - legal-ai/backend/embeddings.py
# - legal-ai/backend/vector_store.py
# - legal-ai/backend/category_classifier.py
# - legal-ai/backend/rag_pipeline.py
# - legal-ai/backend/train_pipeline.py

# CELL 3: Let's run the complete Pipeline programmatically in Google Colab!
"""

import sys
import os

# Define Colab-grounded single execution pipeline
def run_colab_demo():
    print("--- [Colab] Initializing Pakistan Legal AI pipeline ---")
    
    # 1. We mock the imports as if the files were inside standard folders
    from backend.utils import get_config
    from backend.dataset_generator import DatasetGenerator
    from backend.train_pipeline import run_training_pipeline
    from backend.rag_pipeline import RAGPipeline
    
    # 2. Run automated dataset generation & FAISS builder
    print("\n--- [Colab Step 1] Synthesizing 10,000+ Legal Q/As & FAISS index ---")
    run_training_pipeline()
    
    # 3. Instantiate the conversational RAG agent
    print("\n--- [Colab Step 2] Initializing RAG Pipeline ---")
    rag = RAGPipeline()
    
    # 4. Test Query
    test_query = "What is the penalty for online harassment under PECA?"
    print(f"\n--- [Colab Step 3] Testing AI Consultation Query: '{test_query}' ---")
    
    result = rag.run(test_query)
    
    print("\n--- [RAG Response Outputs] ---")
    print(f"Detected Category: {result['category']}")
    print(f"Legal Advice:\n{result['reply']}")
    print(f"Sources: {result['sources']}")
    print(f"Disclaimer: {result['disclaimer']}")

if __name__ == "__main__":
    # If running directly, suggest how to invoke
    print("Google Colab Runner active. copy this namespace folder inside your Google Drive mount or run directly on Colab!")
