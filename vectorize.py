from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def generate_embeddings(chunks):
    """
    Generate embeddings for text chunks using Sentence-BERT.
    
    Args:
        chunks (list): List of text chunks.
        
    Returns:
        list: List of embeddings.
    """
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(chunks)
    return embeddings


def create_faiss_index(embeddings):
    """
    Create and populate a FAISS index with embeddings.
    
    Args:
        embeddings (list): List of embeddings.
        
    Returns:
        faiss.IndexFlatL2: FAISS index containing the embeddings.
    """
    dimension = len(embeddings[0])
    index = faiss.IndexFlatL2(dimension)
    np_embeddings = np.array(embeddings, dtype=np.float32)
    index.add(np_embeddings)
    return index


def save_faiss_index(index, file_path):
    """
    Save a FAISS index to a file.
    
    Args:
        index (faiss.IndexFlatL2): FAISS index.
        file_path (str): Path to save the index.
    """
    faiss.write_index(index, file_path)

def load_faiss_index(file_path):
    """
    Load a FAISS index from a file.
    
    Args:
        file_path (str): Path to the FAISS index file.
        
    Returns:
        faiss.IndexFlatL2: Loaded FAISS index.
    """
    return faiss.read_index(file_path)
