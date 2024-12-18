from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
import time
import traceback


class SemanticSearch:

    @classmethod
    def find_matching_query(cls, user_query, cached_query_list):
        """
        Find a semantically matching query from cached_query_list for the given user_query.
        Uses BERT-based sentence embeddings for semantic similarity matching.
        
        Args:
            user_query (str): The input query to match
            cached_query_list (list): List of previously cached queries to match against
            
        Returns:
            str: Matching query from cache, or None if no good match is found
        """
        # Load model and tokenizer
        try:
            print(f"Finding query: {user_query} in cache...")
            model_name = "sentence-transformers/all-MiniLM-L6-v2"
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModel.from_pretrained(model_name)
            
            def get_embedding(text):
                # Tokenize and get model outputs
                inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
                outputs = model(**inputs)
                
                # Mean pooling
                attention_mask = inputs['attention_mask']
                token_embeddings = outputs.last_hidden_state
                input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
                sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
                sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
                return (sum_embeddings / sum_mask).squeeze()
            
            # Calculate embeddings
            with torch.no_grad():  # Add this for inference
                user_embedding = get_embedding(user_query)
                cached_embeddings = torch.stack([get_embedding(query) for query in cached_query_list])
            
                # Normalize embeddings
                user_embedding = F.normalize(user_embedding, p=2, dim=0)
                cached_embeddings = F.normalize(cached_embeddings, p=2, dim=1)
                
                # Calculate cosine similarities
                similarities = torch.matmul(user_embedding.unsqueeze(0), cached_embeddings.t()).squeeze()
                
                # Find best match
                best_match_idx = torch.argmax(similarities)
                best_match_score = similarities[best_match_idx].item()
            
            # Return match if similarity is high enough, otherwise None
            if best_match_score > 0.8:  # Threshold can be adjusted
                return cached_query_list[best_match_idx]
            return None
        except Exception:
            print("Error in find_matching_query")
            print(traceback.format_exc())
            return None


if __name__ == "__main__":
    # Example usage
    start = time.time()
    cached_queries = [
        "What is the purpose of Form I-130?",
        "How does an F-1 student maintain their status?",
        "What are some common cultural misunderstandings experienced by international students?",
        "What is the H-1B cap?",
        "What are the eligibility criteria for EB-1 extraordinary ability?",
        "What are the requirements for an O-1 visa in the arts?",
        "What business structures are best for immigrant entrepreneurs?",
        "What travel documents are needed for a green card holder?",
        "How long is STEM OPT extension valid for?",
        "What is the process for adjusting status to a green card?",
        "What is the function of Form I-485?",
        "How can an F-1 student obtain work authorization?",
        "What resources are available to help international students adjust to US culture?",
        "What is the prevailing wage for H-1B positions?",
        "What is the National Interest Waiver (NIW)?",
        "Can an O-1 holder bring dependents to the US?",
        "What funding options are available for immigrant-owned businesses?",
        "Can a green card holder travel to Cuba?",
        "What are the reporting requirements for OPT?",
        "What are the different categories of green cards?",
        "What is the purpose of Form I-765?",
        "What are the restrictions on F-1 student employment?",
        "How does homesickness affect international students?",
        "What is the H-1B lottery?",
        "What is the difference between EB-2 and EB-3?",
        "How does the O-1 visa differ from the H-1B visa?",
        "What are some legal considerations for immigrant entrepreneurs?",
        "What are the consequences of abandoning permanent resident status?",
        "What is the unemployment rule for OPT?",
        "How can a family member sponsor a green card?",
        "What is a Request for Evidence (RFE)?",
        "Can an F-1 student start a business?",
        "How do international students navigate US social customs?",
        "What are the requirements for H-1B portability?",
        "What is the PERM labor certification process?",
        "Can an O-1 visa be extended?",
        "What are incubators and accelerators for immigrant startups?",
        "What are the rules for re-entry permits for green card holders?",
        "What is the 24-month bar for STEM OPT?",
        "What is the Diversity Visa Lottery?",
        "What is a Notice of Action (NOA)?",
        "What is Curricular Practical Training (CPT)?",
        "How do international students manage culture shock related to food?",
        "What are the requirements for an H-1B transfer?",
        "What are the advantages of the EB-1 category?",
        "What are the criteria for O-1 visa in business?",
        "How can immigrants access small business loans?",
        "What are the implications of having a criminal record on international travel as a green card holder?",
        "What is the role of the DSO in OPT?",
        "What are the grounds for green card revocation?",
    ]

    # Test the function
    sematic_search = SemanticSearch()
    user_input = "What is the H-1B cap?\n\n"
    result = sematic_search.find_matching_query(user_input, cached_queries)
    end = time.time()

    time_taken = end-start
    print(f"Total time taken: {time_taken}")
    if result:
        print(f"Matching query found: {result}")
    else: 
        print("No Matching query found")