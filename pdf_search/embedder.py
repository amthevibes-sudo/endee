"""Text embedding generation using sentence-transformers."""
import numpy as np
from typing import List, Union
from sentence_transformers import SentenceTransformer
from config import Config


class Embedder:
    """Generate embeddings for text using sentence-transformers."""
    
    def __init__(self, model_name: str = None):
        """Initialize embedder.
        
        Args:
            model_name: Name of sentence-transformer model
        """
        self.model_name = model_name or Config.EMBEDDING_MODEL
        print(f"Loading embedding model: {self.model_name}")
        self.model = SentenceTransformer(self.model_name)
        print(f"Model loaded. Embedding dimension: {self.model.get_sentence_embedding_dimension()}")
    
    def embed_text(self, text: str) -> np.ndarray:
        """Generate embedding for a single text.
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector
        """
        return self.model.encode(text, convert_to_numpy=True)
    
    def embed_batch(
        self,
        texts: List[str],
        batch_size: int = 32,
        show_progress: bool = True
    ) -> np.ndarray:
        """Generate embeddings for multiple texts.
        
        Args:
            texts: List of input texts
            batch_size: Batch size for encoding
            show_progress: Show progress bar
            
        Returns:
            Array of embeddings (N x D)
        """
        return self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=show_progress,
            convert_to_numpy=True
        )
    
    def get_dimension(self) -> int:
        """Get embedding dimension.
        
        Returns:
            Embedding dimension
        """
        return self.model.get_sentence_embedding_dimension()
