import traceback
from services.google_bucket import FileUploadService
from models.FAQModel import FAQ

class CloudCacheService:

    def __init__(self):
        self.FAQ_BUCKET = "isage-faq"
        self.file_service = FileUploadService()
        self.faq_model = FAQ()

    def get_all_queries(self):
        query_list, msg =  self.faq_model.get_all_queries()
        print(msg, query_list)
        return query_list


    def add_query(self, query, answer):
        try:
            print("Adding query to cache...")
            blob_url, msg = self.file_service.write_text_to_file(self.FAQ_BUCKET, query, answer)
            if not blob_url:
                print(msg)
                return False
            
            success, msg = self.faq_model.add_query(query, blob_url)
            print(msg)

            return success
        except Exception:
            print(traceback.format_exc())
            return False


    def get_answer_for_query(self, query):
        try:
            print("Getting answer for query...")
            answer = self.file_service.get_text_from_file(self.FAQ_BUCKET, query)
            self.faq_model.increment_vote_for_query()

            return answer
        except Exception:
            print(traceback.format_exc())
            return False

    def match_query(self, query, query_list):
        if query in query_list:
            print("Query FOUND in cache!")
            return True
        

        print("Query NOT-FOUND in cache!")
        return False
    
    
    def check_query_exists(self, query):
        query_list = self.get_all_queries()
        formatted_query = query.lower().strip()
        match = self.match_query(formatted_query, query_list)

        if match:
            answer = self.get_answer_for_query(query)
            return answer
    
        return False
