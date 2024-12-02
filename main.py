from split_chunks import *
from vectorize import * 
from retriever import *

def main():

    user_choice = None
    rag_model = {
        "Fitness": {
            "index_file": "Fitness/fitness_document_index.faiss",
            "chunks_file": "Fitness/fitness_chunks.txt",
            "folder_path": "Fitness/Fitness_KB_Clean"
        },
        "USCIS": {
            "index_file": "USCIS/USCIS_document_index.faiss",
            "chunks_file": "USCIS/USCIS_chunks.txt",
            "folder_path": "USCIS/USCIS_KB_Clean"
        },
    }

    while True:
        query = input("Choose RAG Model (Enter the number)\n1. Fitness\n2. USCIS\nYour choice:")
        try:
            user_choice = int(query)
            if not user_choice in range(1, 3):
                raise Exception
            else: break
        except Exception:
            print("Invalid choice, select 1 or 2")
        
    models = list(rag_model.keys())
    print(f"User selected {models[user_choice - 1]}")
    

    # Check if an index already exists
    user_choice_model = rag_model.get(models[user_choice - 1])
    index_file = user_choice_model.get("index_file")
    chunks_file = user_choice_model.get("chunks_file")
    folder_path = user_choice_model.get("folder_path")

    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

    if os.path.exists(index_file) and os.path.exists(chunks_file):
        print("Loading existing FAISS index and chunks...")
        index = load_faiss_index(index_file)
        with open(chunks_file, 'r', encoding='utf-8') as f:
            chunks = f.read().split('\n')
    else:
        parsed_files = parse_cleaned_data(folder_path=folder_path)
        all_chunks = process_parsed_files(parsed_files)

        # Flatten all chunks for indexing (if needed)
        chunks = [_chunk for _chunks in all_chunks.values() for _chunk in _chunks]
        # Save chunks for reuse
        with open(chunks_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(chunks))

        embeddings = generate_embeddings(chunks)
        index = create_faiss_index(embeddings)
        save_faiss_index(index, index_file)
        print(f"FAISS index created and saved with {index.ntotal} entries.")

    
    # Handle multiple queries
    while True:
        query = input("\nEnter your query (or type 'exit' to quit): ").strip()
        if query.lower() == 'exit':
            print("Exiting. Goodbye!")
            break
        
        top_chunks = retrieve_top_k_chunks(query, embedding_model, index, chunks, k=5)
        answer = generate_answer(query, top_chunks)
        print(f"\nMain Answer:\n{answer}")

if __name__ == "__main__":
    main()