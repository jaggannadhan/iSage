import os
from google.cloud import datastore
from google.cloud.datastore.query import PropertyFilter
from datetime import datetime
import traceback

CLOUD_PROJECT_ID =  os.getenv("CLOUD_PROJECT_ID")
FAQ_CLIENT = datastore.Client(CLOUD_PROJECT_ID)

class FAQ:
    kind = "FAQ"
    
    @classmethod
    def get_query(cls, question, _getdict=True):
        print(f"Retrieving query: {question} ...")
        try:
            query = FAQ_CLIENT.query(kind=cls.kind)
            query.add_filter(filter=PropertyFilter("query", "=", question))
            entity = list(query.fetch())

            entity = (dict(entity[0]) if _getdict else entity[0]) if entity else None
            return entity, f"Successully retrieved query: {question}"
        except Exception:
            print(traceback.format_exc())
            return False, f"Unable to retrieve query: {question}!"
        
    @classmethod
    def get_all_queries(cls):
        print(f"Retrieving all queries...")
        try:
            query = FAQ_CLIENT.query(kind=cls.kind)
            query.order = ["-votes"]
            entity_list = list(query.fetch())

            query_list = [ entity["query"] for entity in entity_list ]
            return query_list, f"Successully retrieved all queries"
        except Exception:
            print(traceback.format_exc())
            return False, f"Unable to retrieve query!"
        

    @classmethod
    def add_query(cls, query, blob_url):
        print(f"Adding query: {query} to FAQ")
        try:
            entity, msg = cls.get_query(query)
            if entity:
                return entity, f"Query: {query} already exists"

            new_entity = datastore.Entity(FAQ_CLIENT.key(cls.kind))
            new_entity["query"] = query
            new_entity["votes"] = 1
            new_entity["blob_url"] = blob_url
            new_entity["created"] = datetime.now()
            new_entity["updated"] = datetime.now()
        
            FAQ_CLIENT.put(new_entity)
            return dict(new_entity), f"Successully created enitiy in FAQ!"
        except Exception:
            print(traceback.format_exc())
            return False, f"Unable to add query to FAQ"
    
        
    @classmethod
    def increment_vote_for_query(cls, query):
        print(f"Updating query: {query} in FAQ")
        try:
            entity, msg = cls.get_query(query, _getdict=False)
            if not entity:
                raise Exception
            print("\n\nEntity in update:\n", entity, msg)

            entity["votes"] = entity["votes"] + 1
            entity["updated"] = datetime.now()

            FAQ_CLIENT.put(entity)

            return dict(entity), f"Successully updated votes!"
        except Exception:
            print(traceback.format_exc())
            return False, f"Unable to update votes"


    @classmethod
    def delete_query(cls, query):
        print(f"Deleting query: {query}")
        try:

            entity = cls.get_query(query, _getdict=False)
            if not entity:
                raise Exception
            FAQ_CLIENT.delete(entity.key)
        
            # FAQ_CLIENT.delete_multi(keys)

            return True, f"Successfully deleted user: {query}"
        except Exception:
            print(traceback.format_exc())
            return False, f"Unable to delete user: {query}!"
        
    