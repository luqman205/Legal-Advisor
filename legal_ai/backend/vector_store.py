import os
import pickle
import numpy as np
from typing import List, Dict, Any, Tuple
from .utils import logger, get_config

try:
    import faiss
    HAS_FAISS = True
except ImportError:
    HAS_FAISS = False

class VectorStoreManager:
    def __init__(self, index_path: str = None):
        config = get_config()
        self.index_path = index_path or config["faiss_index_path"]
        self.index = None
        self.raw_embeddings = None
        self.metadata: List[Dict[str, Any]] = []

    def build_index(self, embeddings: np.ndarray, metadata: List[Dict[str, Any]]):
        """
        Build a FAISS L2 distance flat index and store matching metadata.
        """
        try:
            self.metadata = metadata
            self.raw_embeddings = embeddings.astype('float32')
            
            if HAS_FAISS:
                logger.info("Initializing FAISS L2 flat vector index...")
                dimension = embeddings.shape[1]
                self.index = faiss.IndexFlatL2(dimension)
                self.index.add(self.raw_embeddings)
                logger.info(f"FAISS index built successfully with {self.index.ntotal} vectors.")
            else:
                logger.info("FAISS is missing. Initializing standard NumPy flat vector index...")
                logger.info(f"NumPy vector index built successfully with {len(self.raw_embeddings)} vectors.")
                
            self.save_index()
        except Exception as e:
            logger.error(f"Failed to build index: {str(e)}")
            raise e

    def save_index(self):
        """
        Save the index and metadata pickle file.
        """
        try:
            os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
            
            if HAS_FAISS and self.index is not None:
                faiss.write_index(self.index, self.index_path)
            
            # Save raw embeddings as backup/fallback
            np.save(self.index_path + ".npy", self.raw_embeddings)
            
            # Write metadata file alongside the index
            meta_path = self.index_path + ".meta"
            with open(meta_path, "wb") as f:
                pickle.dump(self.metadata, f)
                
            logger.info(f"Saved vector database files to {self.index_path}")
        except Exception as e:
            logger.error(f"Failed to save index: {str(e)}")
            raise e

    def load_index(self) -> bool:
        """
        Load the index and metadata. Returns True if successful.
        """
        if not os.path.exists(self.index_path + ".meta"):
            logger.warning(f"Vector store files not found at: {self.index_path}.meta")
            return False

        try:
            if HAS_FAISS and os.path.exists(self.index_path):
                self.index = faiss.read_index(self.index_path)
            
            npy_path = self.index_path + ".npy"
            if os.path.exists(npy_path):
                self.raw_embeddings = np.load(npy_path)
            
            meta_path = self.index_path + ".meta"
            if os.path.exists(meta_path):
                with open(meta_path, "rb") as f:
                    self.metadata = pickle.load(f)
            else:
                self.metadata = []
                
            logger.info(f"Loaded vector store with {len(self.metadata)} records.")
            return True
        except Exception as e:
            logger.error(f"Failed to load vector store: {str(e)}")
            return False

    def search(self, query_embedding: np.ndarray, k: int = 3, category: str = None) -> List[Tuple[Dict[str, Any], float]]:
        """
        Search vector space and return nearest neighbors with metadata and distance scores, optionally filtered by category.
        """
        if (HAS_FAISS and self.index is None) or (not HAS_FAISS and self.raw_embeddings is None):
            if not self.load_index():
                raise ValueError("Vector store index is not built or loaded.")

        try:
            # Query embedding shape must be (1, dimension)
            query_vector = query_embedding.astype('float32')
            if len(query_vector.shape) == 1:
                query_vector = np.expand_dims(query_vector, axis=0)

            if HAS_FAISS and self.index is not None:
                # If category is provided, search for more items and filter
                search_k = min(len(self.metadata), k * 20 if category else k)
                distances, indices = self.index.search(query_vector, search_k)
                
                results = []
                for i, idx in enumerate(indices[0]):
                    if idx == -1 or idx >= len(self.metadata):
                        continue
                    meta = self.metadata[idx]
                    if category and meta.get("category") != category:
                        continue
                    results.append((meta, float(distances[0][i])))
                    if len(results) >= k:
                        break
                return results
            else:
                # Failsafe NumPy Cosine/Euclidean Distance (L2) search
                # If category is provided, pre-filter raw embeddings and metadata
                if category:
                    filtered_indices = [idx for idx, meta in enumerate(self.metadata) if meta.get("category") == category]
                    if not filtered_indices:
                        return []
                    sub_embeddings = self.raw_embeddings[filtered_indices]
                    diff = sub_embeddings - query_vector
                    distances = np.sum(diff ** 2, axis=1)
                    sorted_sub_indices = np.argsort(distances)[:k]
                    
                    results = []
                    for s_idx in sorted_sub_indices:
                        orig_idx = filtered_indices[s_idx]
                        results.append((self.metadata[orig_idx], float(distances[s_idx])))
                    return results
                else:
                    diff = self.raw_embeddings - query_vector
                    distances = np.sum(diff ** 2, axis=1)
                    indices = np.argsort(distances)[:k]
                    results = []
                    for idx in indices:
                        if idx >= len(self.metadata):
                            continue
                        results.append((self.metadata[idx], float(distances[idx])))
                    return results
        except Exception as e:
            logger.error(f"Error executing vector search: {str(e)}")
            raise e
