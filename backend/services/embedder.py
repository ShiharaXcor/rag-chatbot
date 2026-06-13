from langchain_huggingface import HuggingFaceEmbeddings
from config import EMBEDDING_MODEL

# We store the embedder in a module-level variable
# so it loads ONCE when the server starts
# and reuses the same model for every request
# (loading a model takes ~3 seconds — we do it only once)
_embedder = None

def get_embedder():
    """
    Load the HuggingFace embedding model.
    Returns the same instance every time (singleton pattern).
    Model: sentence-transformers/all-MiniLM-L6-v2
    Output: 384-dimensional vector for any input text
    """
    global _embedder

    if _embedder is None:
        # First call → download and load the model
        _embedder = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},   # use CPU (no GPU needed)
            encode_kwargs={"normalize_embeddings": True},  # normalize for cosine similarity
        )
        print(f"Embedding model loaded: {EMBEDDING_MODEL}")

    # Second+ calls → return already-loaded model instantly
    return _embedder