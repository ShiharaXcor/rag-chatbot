import os
from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from services.safety_filter import is_document_safe

def load_and_chunk_pdf(file_path: str, filename: str) -> List[Dict]:
    """Load a PDF and split into chunks with metadata."""
    loader = PyPDFLoader(file_path)
    pages = loader.load()

    # Safety check on full document text
    full_text = " ".join([p.page_content for p in pages])
    safety = is_document_safe(full_text)
    if not safety["safe"]:
        raise ValueError(safety["reason"])

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = []
    for page in pages:
        page_chunks = splitter.split_text(page.page_content)
        for i, chunk_text in enumerate(page_chunks):
            if len(chunk_text.strip()) < 30:
                continue
            chunks.append({
                "text": chunk_text.strip(),
                "metadata": {
                    "source": filename,
                    "page": page.metadata.get("page", 0) + 1,
                    "chunk_index": i,
                }
            })

    return chunks