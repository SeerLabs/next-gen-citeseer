'''
start this service somewhere, e.g. on a server with a GPU

python query_embedding_service.py
'''

from flask import Flask, request, jsonify
import torch
from transformers import AutoTokenizer, AutoModel
import os
os.environ["CUDA_VISIBLE_DEVICES"]="2"

app = Flask(__name__)
tokenizer = AutoTokenizer.from_pretrained('allenai/specter2' )
#load base model
model = AutoModel.from_pretrained('allenai/specter2', cache_dir="/data/szr207/.cache/torch/transformers")
#load the adapter(s) as per the required task, provide an identifier for the adapter in load_as argument and activate it
model.load_adapter("allenai/specter2_adhoc_query", source="hf", load_as="adhoc_query", set_active=True)
model.cuda()

@app.route('/embeddings', methods=['POST'])
def get_embeddings():
    text_batch = request.json['text']
    
    inputs = tokenizer(text_batch, padding=True, truncation=True,
                       return_tensors="pt", return_token_type_ids=False, max_length=512)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    inputs = {key: value.to(device) for key, value in inputs.items()}

    output = model(**inputs)
    embeddings = output.last_hidden_state[:, 0, :]

    embeddings = embeddings.cpu().detach().numpy()

    return jsonify(embeddings.tolist())

if __name__ == '__main__':
    app.run(port=5050)