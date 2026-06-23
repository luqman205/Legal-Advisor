import os
import json
import numpy as np
from .utils import logger, get_config
from .dataset_generator import DatasetGenerator
from .embeddings import EmbeddingsManager
from .vector_store import VectorStoreManager

def run_training_pipeline():
    logger.info("==============================================")
    logger.info("Starting Enterprise Pakistani Legal AI Trainer")
    logger.info("==============================================")
    
    config = get_config()
    
    # 1. Generate Dataset
    if not os.path.exists(config["dataset_json_path"]):
        logger.info("Dataset JSON not found. Running programmatic generation pipeline...")
        generator = DatasetGenerator()
        generator.run()
    else:
        logger.info(f"Existing dataset detected at: {config['dataset_json_path']}. Re-using dataset.")

    # 2. Load Dataset
    with open(config["dataset_json_path"], "r", encoding="utf-8") as f:
        dataset = json.load(f)
    
    logger.info(f"Loaded {len(dataset)} legal records for vector indexing.")
    
    # 3. Create Chunk Texts & Metadata
    chunks = []
    metadata = []
    
    for record in dataset:
        chunk_text = f"Category: {record['category']}\nQuestion: {record['question']}\nAnswer: {record['answer']}"
        chunks.append(chunk_text)
        
        # Keep detailed record for context injection
        metadata.append({
            "id": record["id"],
            "category": record["category"],
            "question": record["question"],
            "answer": record["answer"],
            "source": record["source"]
        })

    # 4. Generate Embeddings
    embeddings_mgr = EmbeddingsManager()
    logger.info("Encoding legal chunks into high-dimensional vector space...")
    embeddings = embeddings_mgr.encode(chunks)
    logger.info(f"Generated embeddings shape: {embeddings.shape}")
    
    # 5. Build and Save FAISS Index
    vector_store = VectorStoreManager()
    vector_store.build_index(embeddings, metadata)
    
    logger.info("==============================================")
    logger.info("Pakistani Legal AI Trainer Completed Successfully!")
    logger.info("==============================================")

if __name__ == "__main__":
    run_training_pipeline()
