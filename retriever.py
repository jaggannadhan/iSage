import numpy as np
from transformers import pipeline
from llm_service import OpenAIService

class RAGOps:

    def __init__(self):
        self.LLMService = OpenAIService()


    def retrieve_top_k_chunks(self, query, model, index, chunks, k=3):
        """
        Retrieve the top-k most relevant chunks for a given query.
        
        Args:
            query (str): User query.
            model (SentenceTransformer): Embedding model.
            index (faiss.IndexFlatL2): FAISS index.
            chunks (list): List of text chunks.
            k (int): Number of chunks to retrieve.
            
        Returns:
            list: Top-k relevant text chunks.
        """
        query_embedding = model.encode([query])
        query_embedding = np.array(query_embedding, dtype=np.float32)
        distances, indices = index.search(query_embedding, k)
        
        relevant_chunks = [chunks[i] for i in indices[0]]
        return relevant_chunks


    def truncate_context(self, context, max_tokens):
        """
        Truncate the context to fit within the token limit.
        
        Args:
            context (str): Full context text.
            max_tokens (int): Maximum number of tokens to retain.
            
        Returns:
            str: Truncated context.
        """
        words = context.split()
        print(f">>>>>>>>>>>>>Length of context: {len(words)}<<<<<<<<<<<<<<<<<<<<<\n\n")
        if len(words) > max_tokens:
            context = " ".join(words[:max_tokens])
        return context


    def generate_answer(self, query, retrieved_chunks):
        """
        Generate an answer to the user's query using retrieved chunks.
        
        Args:
            query (str): User query.
            retrieved_chunks (list): Top-k relevant text chunks.
            
        Returns:
            str: Generated answer.
        """
        context = " ".join(retrieved_chunks)
        answer = self.LLMService.answer_chain(context, query)

        return answer



