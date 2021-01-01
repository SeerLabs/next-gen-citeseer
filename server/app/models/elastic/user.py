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

    def add_collection_paper(self, collection_name, pid):
        if not collection_name:
            collection_name = "untitled_collection"
        if not self.__contains__("collections"):
            self.__setitem__("collections", [Collection(collection_name=collection_name, paper_id_list=[pid])])
            return
        for collection in self.collections:
            if collection.collection_name == collection_name:
                if pid not in collection.paper_id_list:
                    collection.paper_id_list.append(pid)
                return
        self.collections.append(Collection(collection_name=collection_name, paper_id_list=[pid]))
    def rename_collection(self, curr_collection_name, new_collection_name):
        for collection in self.collections:
            if collection.collection_name == curr_collection_name:
                collection.collection_name = new_collection_name
                return
    def delete_collection_paper(self, collection_name, pid): 
        if not self.__contains__("collections"):
            return
        for collection in self.collections:
            if collection.collection_name == collection_name:
                if pid in collection.paper_id_list:
                    collection.paper_id_list.remove(pid)
                if len(collection.paper_id_list) == 0:
                    self.collections.remove(collection)
                return
