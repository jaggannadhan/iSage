import traceback, requests, json
from services.query_matching import find_matching_query

class CloudCacheService:

    def __init__(self):
        self.FAQ_BUCKET = "isage-faq"
        self.BACKEND_URL = "https://cache-dot-isage2024.uc.r.appspot.com"
        self.FAQ = {}
        self.FAQ_embeddings = None
        
    def get_FAQ(self):
        try:
            return self.FAQ
        except Exception:
            print(traceback.format_exc())
            return None
        
    def set_FAQ(self, FAQ):
        try:
            if not FAQ:
                self.FAQ = []
                return
            
            for enitiy in FAQ:
                query = enitiy.get("query")
                self.FAQ[query] = enitiy

        except Exception:
            print("Error in set_FAQ")
            print(traceback.format_exc())
    
    def get_top_queries(self, k=20):
        try:
            response = requests.get(
                f"{self.BACKEND_URL}/get-top-queries",
                params={"k": k}
            )
            if response.status_code == 200:
                data = response.json()
                print(f"FAQ from cloud cache: {data}")
                query_list = data["query_list"]
                
                self.set_FAQ(query_list)
                
                return self.FAQ
            else:
                return None
        except Exception:
            print("Error in get_top_queries")
            print(traceback.format_exc())
            return None


    def add_query(self, query, answer):
        try:
            print("Adding query to cache...")
            response = requests.post(
                f"{self.BACKEND_URL}/cache-response", 
                data=json.dumps({"query": query, "answer": answer}))
            
            if response.status_code != 200:
                print("Request failed!")
                return False
            
            data = response.json()
            print(data)
            return data.get("success")
        except Exception:
            print("Error in add_query to cache")
            print(traceback.format_exc())
            return False
        
    def increment_vote_for_query(self, matched_enitity):
        try:
            print("Incrementing vote for query")
            response = requests.post(
                f"{self.BACKEND_URL}/increment-vote", 
                data=json.dumps({"query": matched_enitity.get("query")}))
            
            if response.status_code != 200:
                print("Request failed!")
                return False
            
            data = response.json()
            print(data)
            return data.get("success")
        except Exception:
            print("Error in increment_vote_for_query")
            print(traceback.format_exc())
            return False


    def get_answer_for_query(self, matched_enitity):
        try:
            print("Getting answer for query...")

            blob_url = matched_enitity.get("blob_url")
            response = requests.get(blob_url)
            answer = response.text.strip()

            print(answer)
            return answer
        except Exception:
            print("Error in get_answer_for_query")
            print(traceback.format_exc())
            return None

    def match_query(self, query):
        try:
            query_list=list(self.FAQ.keys())
            # print(f">>>>>>FAQ: {query_list}")

            matched_query = find_matching_query(query, query_list)
            if not matched_query:
                print("Query NOT-FOUND in cache!")
                return None

            matched_enitity = self.FAQ.get(matched_query)
            return matched_enitity
        except Exception:
            print("Error in match_query")
            print(traceback.format_exc())
            return False
    
    
    def check_query_exists(self, query):
        formatted_query = query.lower().strip()
        matched_enitity = self.match_query(formatted_query)

        if matched_enitity:
            answer = self.get_answer_for_query(matched_enitity)
            self.increment_vote_for_query(matched_enitity)
            return answer
    
        return False
