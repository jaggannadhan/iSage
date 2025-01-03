import traceback, requests, json
from services.query_matching import SemanticSearch

class CloudCacheService:

    def __init__(self):
        self.FAQ_BUCKET = "isage-faq"
        self.BACKEND_URL = "https://cache-dot-isage2024.uc.r.appspot.com"
        self.FAQ = {}
        self.semantic_search = SemanticSearch()
        
    def get_FAQ(self):
        try:
            return self.FAQ
        except Exception:
            print(traceback.format_exc())
            return None
        
    def set_FAQ(self, FAQ):
        try:
            if not FAQ:
                self.FAQ = {}
                return
            
            for enitiy in FAQ:
                query = enitiy.get("query")
                self.FAQ[query] = enitiy

        except Exception:
            print("Error in set_FAQ")
            print(traceback.format_exc())

    def update_FAQ(self, entity):
        try:
            if not entity:
                print("Nothing to update")
                return self.FAQ
            
            query = entity.get("query", None)
            votes = entity.get("votes")

            if to_update := self.FAQ.get(query, None):
                to_update["votes"] = votes + 1
                self.FAQ[query] = to_update
            else:
                self.FAQ[query] = entity

            return self.FAQ
        except Exception:
            print("Error in update_FAQ")
            print(traceback.format_exc())
            return self.FAQ
    
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
            entity = data.get("success")
            self.update_FAQ(entity)

            return entity
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

            matched_query = self.semantic_search.find_matching_query(query, query_list)
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
            self.update_FAQ(matched_enitity)
            return answer
    
        return False


def cache_management(service):
    def wrapper(*args, **kwargs):
        instance = args[0]
        cache_service = instance.cache_service
        print(kwargs, args)
        query = kwargs.get("query", None)

        if not query:
            return "Query cannot be empty."
    
        try:
            answer = cache_service.check_query_exists(query)
            if answer:
                return answer
        except Exception:
            print(">>>>>>>>>>>>Error in CACHE RETRIEVAL<<<<<<<<<<<")
            print(traceback.format_exc())
            print(">>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<")
        

        answer = service(*args, **kwargs)

        try:
            cache_service.add_query(query, answer)
        except Exception:
            print(">>>>>>>>>Error in caching LLM Response<<<<<<<<<")
            print(traceback.format_exc())
            print(">>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<")

        return answer
    return wrapper