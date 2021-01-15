from models.schemas.user import User
from elasticsearch_dsl import Document, Text, Keyword, Nested, InnerDoc, Object

class Collection(InnerDoc):
    collection_name = Keyword(multi=True)
    paper_id_list = Keyword(multi=True)

class UserInDB(Document):
    email = Keyword()
    full_name = Text()
    organization = Text()
    department = Text()
    web_page = Text()
    country = Text()
    state = Text()
    collections = Nested(Collection)
    monitered_papers = Keyword(multi=True)
    liked_papers = Keyword(multi=True)
    salt = Keyword()
    hashed_password = Keyword()
    is_activated = Keyword() 

    class Index:
        name = 'user_next'

    def create_collection(self, collection_name):
        if not collection_name:
            collection_name = "New Collection"
        if not self.__contains__("collections"):
            self.__setitem__("collections", [Collection(collection_name=collection_name, paper_id_list=[])])
            return 0
        for collection in self.collections:
            if collection.collection_name == collection_name:
                return -1
        self.collections.append(Collection(collection_name=collection_name, paper_id_list=[]))
        return 0

    def delete_collection(self, collection_name):
        if not self.__contains__("collections"):
            return -1
        for collection in self.collections:
            if collection.collection_name == collection_name:
                self.collections.remove(collection)
                return 0
        return -1
    def add_collection_paper(self, collection_name, pid):
        if not collection_name:
            collection_name = "New Collection"
        if not self.__contains__("collections"):
            return -1
        for collection in self.collections:
            if collection.collection_name == collection_name:
                if not collection.__contains__("paper_id_list"):
                    collection.__setitem__("paper_id_list", [pid])
                elif pid not in collection.paper_id_list:
                    collection.paper_id_list.append(pid)
                else:
                    return -1
                return 0
        return -1
    def rename_collection(self, curr_collection_name, new_collection_name):
        for collection in self.collections:
            if collection.collection_name == curr_collection_name:
                collection.collection_name = new_collection_name
                return 0
        return -1

    def delete_collection_paper(self, collection_name, pid): 
        if not self.__contains__("collections"):
            return -1
        for collection in self.collections:
            if collection.collection_name == collection_name:
                if pid in collection.paper_id_list:
                    collection.paper_id_list.remove(pid)
                    return 0
                else:
                    return -1
            return -1
