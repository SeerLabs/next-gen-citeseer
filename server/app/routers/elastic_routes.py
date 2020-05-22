from fastapi import APIRouter
from services.elastic_service import Elastic

router = APIRouter()
ES = Elastic()

@router.get('/search')
def perform_search(q: str = ""):
    result = ES.refined_search('citeseerx', q, ['title', 'text'])
    return result

@router.get('/paper_info')
def paper_info(paperID: str = ""):
    result = ES.get_paper_info(paperID)
    return result

@router.get('/citations')
def citations(paperID: str = ""):
    result = ES.get_citations(paperID)
    return result

@router.get('/similar')
def similar_papers(paperID: str = ""):
    result = ES.get_clustered_papers(paperID)
    return result
