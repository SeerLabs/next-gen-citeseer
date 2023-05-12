from tqdm import tqdm
import torch
import requests
import json
from elasticsearch import Elasticsearch


es = Elasticsearch()

def get_embeddings(text_batch):
    url = "http://localhost:5050/embeddings"
    headers = {"Content-Type": "application/json"}
    data = json.dumps({"text": text_batch})
    
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        embeddings = response.json()
        return embeddings
    else:
        print(f"Error: {response.status_code}")
        return None

def get_es_results(index_name, search_text, K):
    query = {
        "query": {
            "bool": {
                "should": [
                    {
                        "match": {
                            "title": {
                                "query": search_text,
                                "boost": 3
                            }
                        }
                    },
                    {
                        "match": {
                            "abstract": {
                                "query": search_text,
                                "boost": 2
                            }
                        }
                    },
                    {
                        "range": {
                            "year": {
                                "gte": "now-5y",
                                "boost": 1
                            }
                        }
                    }
                ]
            }
        },
        "_source": ["_id", "_score"]
    }

    results = es.search(index=index_name, body=query, size=K)
    es_results = [{"_id": hit["_id"], "_score": hit["_score"]} for hit in results["hits"]["hits"]]
    return es_results

def get_knn_results(index_name, query_embedding, K):
    query = {
        "query": {
            "script_score": {
                "query": {
                    "match_all": {}
                },
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                    "params": {
                        "query_vector": query_embedding[0]
                    }
                }
            }
        },
        "_source": ["_id", "_score"]
    }

    results = es.search(index=index_name, body=query, size=K)
    knn_results = [{"_id": hit["_id"], "_score": hit["_score"]} for hit in results["hits"]["hits"]]
    return knn_results


def generate_embeddings(model, tokenizer, list_text, batch_size: int = 8):
    # Initialize an empty list to store the embeddings
    all_embeddings = []

    # Process the papers in smaller batches
    for i in tqdm(range(0, len(list_text), batch_size)):
        batch_papers = list_text[i:i + batch_size]

        # concatenate title and abstract
        text_batch = batch_papers

        # preprocess the input
        inputs = tokenizer(text_batch, padding=True, truncation=True,
                                        return_tensors="pt", return_token_type_ids=False, max_length=512)

        # Move inputs to the GPU if available
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        inputs = {key: value.to(device) for key, value in inputs.items()}

        # Get the embeddings
        output = model(**inputs)
        embeddings = output.last_hidden_state[:, 0, :]

        # Move embeddings back to CPU and convert to numpy
        embeddings = embeddings.cpu().detach().numpy()

        # Extend the list of embeddings
        all_embeddings.extend(embeddings)

        # Free GPU memory
        del inputs, output, embeddings
        torch.cuda.empty_cache()

    return all_embeddings

def reciprocal_rank_fusion(list_a, list_b):
    # Normalize the scores in list_a
    max_score_a = max(item['_score'] for item in list_a)
    for item in list_a:
        item['_score_normalized'] = item['_score'] / max_score_a

    # Normalize the scores in list_b
    max_score_b = max(item['_score'] for item in list_b)
    for item in list_b:
        item['_score_normalized'] = item['_score'] / max_score_b

    # Merge the lists
    merged_list = list_a + list_b

    # Combine items with the same ID and sum their normalized scores
    combined_list = {}
    for item in merged_list:
        if item['_id'] not in combined_list:
            combined_list[item['_id']] = item
        else:
            combined_list[item['_id']]['_score_normalized'] += item['_score_normalized']

    # Convert the combined dictionary back to a list and sort by normalized score
    sorted_list = sorted(combined_list.values(), key=lambda x: x['_score_normalized'], reverse=True)

    return sorted_list

# retrieve documents from elasticsearch based on a list of ids
def retrieve_docs(es, index_name, list_ids, k):
    docs = []
    for id in list_ids[:k]:
        doc = es.get(index=index_name, id=id['_id'])
        docs.append(doc)
    return docs
