import numpy as np
from typing import List, Union, Any
from .utils import logger, get_config

try:
    from sentence_transformers import SentenceTransformer  # type: ignore
    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False

class EmbeddingsManager:
    def __init__(self, model_name: str = None):
        config = get_config()
        self.model_name = model_name or config["embedding_model"]
        self._model = None
        
        # Extensive high-fidelity legal vocabulary for structural vector mapping fallback
        self.vocab = [
            "divorce", "khula", "talaq", "maintenance", "iddat", "custody", "guardian", "marriage",
            "possession", "illegal", "land", "dispute", "inheritance", "registry", "patwari", "fard",
            "fir", "police", "arrest", "bail", "sho", "complaint", "consumer", "refund", "fake", 
            "salary", "employer", "termination", "tax", "fbr", "audit", "sales", "income",
            "constitution", "article", "writ", "petition", "civil", "specific", "injunction",
            "mischief", "theft", "murder", "contract", "gratuity", "court", "qabza",
            "void", "guarantee", "agency", "surety", "bailment", "pledge", "cpc", "plaint",
            "written", "summons", "decree", "appeal", "review", "revision", "limitation",
            "mortgage", "lease", "partition", "benami", "easement",
            "maternity", "pessi", "sessi", "eobi", "overtime", "safety", "union", "cba",
            "withholding", "wht", "assessment", "surcharge", "atl", "customs", "excise", "provincial", "cgt", "filer", "non-filer",
            "defective", "warranty", "substandard", "negligence", "receipt", "invoice", "overcharging", "misleading", "notice", "frivolous"
        ]

    @property
    def model(self) -> Any:
        if not HAS_SENTENCE_TRANSFORMERS:
            return None
        if self._model is None:
            logger.info(f"Loading SentenceTransformer model: {self.model_name}...")
            self._model = SentenceTransformer(self.model_name)
            logger.info("SentenceTransformer model loaded successfully.")
        return self._model

    def encode(self, texts: Union[str, List[str]]) -> np.ndarray:
        """
        Encode single text or list of texts into embedding vectors.
        """
        if isinstance(texts, str):
            texts = [texts]
            
        if HAS_SENTENCE_TRANSFORMERS:
            try:
                return self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
            except Exception as e:
                logger.warning(f"SentenceTransformer failed: {str(e)}. Falling back to lightweight lexical encoder.")
        
        # Failsafe lightweight Lexical Embedding Encoder (TF-IDF weighted)
        embeddings = []
        for text in texts:
            words = text.lower().split()
            vector = []
            for vocab_word in self.vocab:
                count = words.count(vocab_word)
                vector.append(float(count))
            embeddings.append(vector)
            
        # Convert to numpy array with shape (len(texts), len(vocab))
        arr = np.array(embeddings, dtype=np.float32)
        # Normalize vectors for Cosine Similarity inside FAISS L2 matching
        norms = np.linalg.norm(arr, axis=1, keepdims=True)
        norms[norms == 0] = 1e-10
        return arr / norms
