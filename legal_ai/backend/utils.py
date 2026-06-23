import os
import sys
import logging
from typing import Dict, Any

# Setup Logging
def setup_logger(name: str = "LegalAI") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File Handler (Optional)
        log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
        os.makedirs(log_dir, exist_ok=True)
        file_handler = logging.FileHandler(os.path.join(log_dir, "app.log"))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger

logger = setup_logger()

# Config parameters
CONFIG: Dict[str, Any] = {
    "embedding_model": "BAAI/bge-small-en-v1.5",
    "llm_model": "meta-llama/Meta-Llama-3-8B-Instruct", # Local Llama 3
    "faiss_index_path": os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
        "vector_db", 
        "faiss_index.bin"
    ),
    "dataset_json_path": os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
        "dataset", 
        "legal_dataset.json"
    ),
    "dataset_csv_path": os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
        "dataset", 
        "legal_dataset.csv"
    ),
    "top_k": 3,
    "categories": [
        "Family Laws",
        "Criminal Laws",
        "Civil Laws",
        "Property Laws",
        "Labour Laws",
        "Tax Laws",
        "Consumer Protection Laws",
        "Constitutional Laws"
    ],
    "disclaimer": "This AI system provides informational legal guidance only and is not a substitute for professional legal advice."
}

def get_config() -> Dict[str, Any]:
    return CONFIG
