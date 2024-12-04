from sentence_transformers import SentenceTransformer
import os
from vectorize import * 
from split_chunks import *

class LoadRAG():

    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.chunks = None
        self.model_file_path = {
            "index_file": "USCIS/USCIS_document_index.faiss",
            "chunks_file": "USCIS/USCIS_chunks.txt",
            "folder_path": "USCIS/USCIS_KB_Clean"
        }

        self.run()
        
    def run(self):
        index_file = self.model_file_path.get("index_file")
        chunks_file = self.model_file_path.get("chunks_file")
        folder_path = self.model_file_path.get("folder_path")

        if os.path.exists(index_file) and os.path.exists(chunks_file):
            print("Loading existing FAISS index and chunks...")
            self.index = load_faiss_index(index_file)
            with open(chunks_file, 'r', encoding='utf-8') as f:
                self.chunks = f.read().split('\n')
        else:
            parsed_files = parse_cleaned_data(folder_path=folder_path)
            all_chunks = process_parsed_files(parsed_files)

            # Flatten all chunks for indexing (if needed)
            self.chunks = [_chunk for _chunks in all_chunks.values() for _chunk in _chunks]
            # Save chunks for reuse
            with open(chunks_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(self.chunks))

            embeddings = generate_embeddings(self.chunks)
            self.index = create_faiss_index(embeddings)
            save_faiss_index(self.index, index_file)
            print(f"FAISS index created and saved with {self.index.ntotal} entries.")
