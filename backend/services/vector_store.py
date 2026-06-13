import os, json
import faiss
import numpy as np
from typing import List, Dict
from services.embedder import get_embedder
from config import VECTORSTORE_DIR

# File paths where FAISS index + chunk metadata are saved
INDEX_FILE  = os.path.join(VECTORSTORE_DIR, "index.faiss")
CHUNKS_FILE = os.path.join(VECTORSTORE_DIR, "chunks.json")

# In-memory state
_chunks: List[Dict] = []
_index = None

def _load_from_disk():
    """Load saved index and chunks from disk into memory."""
    global _chunks, _index
    if os.path.exists(CHUNKS_FILE):
        with open(CHUNKS_FILE, "r") as f:
            _chunks = json.load(f)
    if os.path.exists(INDEX_FILE) and _chunks:
        _index = faiss.read_index(INDEX_FILE)

def _save_to_disk():
    """Save current index and chunks to disk."""
    with open(CHUNKS_FILE, "w") as f:
        json.dump(_chunks, f)
    if _index is not None:
        faiss.write_index(_index, INDEX_FILE)

def add_chunks(new_chunks: List[Dict]):
    """Embed new chunks and add them to FAISS index."""
    global _chunks, _index
    _load_from_disk()

    embedder = get_embedder()
    texts   = [c["text"] for c in new_chunks]
    vectors = np.array(embedder.embed_documents(texts), dtype="float32")

    if _index is None:
        dim    = vectors.shape[1]           # 384 for MiniLM
        _index = faiss.IndexFlatIP(dim)    # IP = Inner Product (cosine similarity)

    _index.add(vectors)
    _chunks.extend(new_chunks)
    _save_to_disk()

def search(query: str, top_k: int = 5) -> List[Dict]:
    """Search for most relevant chunks for a query."""
    global _chunks, _index
    _load_from_disk()

    if _index is None or not _chunks:
        return []

    embedder  = get_embedder()
    query_vec = np.array([embedder.embed_query(query)], dtype="float32")
    scores, indices = _index.search(query_vec, min(top_k, len(_chunks)))

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1: continue
        chunk = _chunks[idx].copy()
        chunk["score"] = round(float(score) * 100, 1)  # as percentage
        results.append(chunk)

    return results

def get_all_documents() -> List[str]:
    """Return list of unique uploaded document names."""
    _load_from_disk()
    return list(set(c["metadata"]["source"] for c in _chunks))

def delete_document(filename: str):
    """Remove all chunks from a specific document and rebuild index."""
    global _chunks, _index
    _load_from_disk()
    _chunks = [c for c in _chunks if c["metadata"]["source"] != filename]
    _index  = None
    if _chunks:
        embedder = get_embedder()
        vectors  = np.array(embedder.embed_documents([c["text"] for c in _chunks]), dtype="float32")
        _index   = faiss.IndexFlatIP(vectors.shape[1])
        _index.add(vectors)
    _save_to_disk()