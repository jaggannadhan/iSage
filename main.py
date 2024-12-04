from retriever import *
from load_RAG import LoadRAG

def main():
    rag_model = LoadRAG()
    # Handle multiple queries
    while True:
        query = input("\nEnter your query (or type 'exit' to quit): ").strip()
        if query.lower() == 'exit':
            print("Exiting. Goodbye!")
            break
        
        top_chunks = retrieve_top_k_chunks(
            query, 
            rag_model.embedding_model, 
            rag_model.index, 
            rag_model.chunks, 
            k=5
        )
        answer = generate_answer(query, top_chunks)
        print(f"\nMain Answer:\n{answer}")

if __name__ == "__main__":
    main()