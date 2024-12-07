from sentence_transformers import SentenceTransformer
import os
from vectorize import * 
from split_chunks import *
from llm_service import LLMService

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from lightrag import LightRAG, QueryParam
from lightrag.llm import gpt_4o_mini_complete, gpt_4o_complete
from dotenv import load_dotenv

load_dotenv()


class LOAD_RAG_MODEL:
    def __init__(self):
        print(">>>>>>>>>>>>Initializing RAG Models<<<<<<<<<<<<<\n\n")
        self.rag_faiss = RAG_MOD_BASIC()
        self.rag_sklearn = RAG_MOD_SKLEARN()
        self.rag_lightRAG = RAG_MOD_LIGHTRAG()

        self.model_types = {
            "FAISS": self.rag_faiss,
            "SKLearn": self.rag_sklearn,
            "LightRAG": self.rag_lightRAG
        }
        print(">>>>>>>>>>>>>>>>RAG Models Loaded<<<<<<<<<<<<<<<<\n\n")

    def get_model(self, model="FAISS"):
        return self.model_types.get(model, self.model_types.get("FAISS"))


class RAG_MOD_BASIC:

    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.LLMService = LLMService()

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

    def retrieve_top_k_chunks(self, query, k=3):
        query_embedding = self.embedding_model.encode([query])
        query_embedding = np.array(query_embedding, dtype=np.float32)
        distances, indices = self.index.search(query_embedding, k)
        
        relevant_chunks = [self.chunks[i] for i in indices[0]]
        return relevant_chunks
    
    def generate_answer(self, query, retrieved_chunks):
        context = " ".join(retrieved_chunks)
        answer = self.LLMService.answer_chain(context, query)

        return answer
    
    def truncate_context(self, context, max_tokens):
        words = context.split()
        print(f">>>>>>>>>>>>>Length of context: {len(words)}<<<<<<<<<<<<<<<<<<<<<\n\n")
        if len(words) > max_tokens:
            context = " ".join(words[:max_tokens])
        return context


class RAG_MOD_SKLEARN:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.LLMService = LLMService()
        
        self.documents = None
        self.tdidf_matrix = None
        
        self.run()

    def run(self):
        parsed_files = parse_cleaned_data(folder_path="USCIS/USCIS_KB_Clean")
        all_chunks = process_parsed_files(parsed_files)
        # Flatten all chunks for indexing (if needed)
        
        self.documents = [_chunk for _chunks in all_chunks.values() for _chunk in _chunks]
        self.tdidf_matrix = self.vectorizer.fit_transform(self.documents)

    
    def retrieve_top_k_chunks(self, query, k=2):
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.tdidf_matrix).flatten()
        print(similarities.shape)  

        top_k_indices = np.argsort(similarities)[-k:]
        context = [ self.documents[i] for i in top_k_indices ]
        
        # [
        #     { "document": self.documents[i], "relevance": float(similarities[i]) }
        #     for i in top_k_indices
        # ]
        return context
    
    def generate_answer(self, query, retrieved_chunks):
        context = " ".join(retrieved_chunks)
        answer = self.LLMService.answer_chain(context, query)

        return answer
    

class RAG_MOD_LIGHTRAG:
    def __init__(self):
        self.working_dir = "USCIS/LightRAG"
        self.folder_path = "USCIS/USCIS_KB_Clean"
        self.rag_model = LightRAG(
            working_dir=self.working_dir,
            llm_model_func=gpt_4o_mini_complete  
        )
        
        self.run()

    def run(self):
        if not os.path.exists(self.working_dir):
            os.mkdir(self.working_dir)
            
        for filename in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, filename)
            if os.path.isfile(file_path):
                with open(file_path) as doc:
                    self.rag_model.insert(doc.read())

    def generate_answer(self, query, mode="hybrid"):
        answer = self.rag_model.query(query, param=QueryParam(mode=mode))
        return answer


RAG_BAG = LOAD_RAG_MODEL()