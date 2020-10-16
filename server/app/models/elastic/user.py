from models.schemas.user import User
from elasticsearch_dsl import Document, Text, Keyword, Nested, InnerDoc, Object

class Collections(InnerDoc):
    default_collection: Keyword(multi=True)

class UserInDB(Document):
    username: Keyword()
    email: Keyword()
    full_name: Text()
    organization: Text()
    department: Text()
    web_page: Text()
    country: Text()
    state: Text()
    collections: Nested(Collections)
    monitered_papers: Keyword(multi=True)
    liked_papers: Keyword(multi=True)
    salt: Keyword()
    hashed_password: Keyword()
    
    class Index:
        name = 'user'
