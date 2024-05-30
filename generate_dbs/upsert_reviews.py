import json
import os
import numpy as np
import re
import pdb

# load data
file_name = '../data/test2.json'
json_data = open(file_name)
data = json.load(json_data)

#initialize pinecone
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
#use_serverless = os.environ.get("USE_SERVERLESS", "False").lower() == 'true'

api_key = os.environ.get('PINECONE_API_KEY')
pc = Pinecone(api_key = api_key)

# run serverless
from pinecone import ServerlessSpec, PodSpec
spec = ServerlessSpec(cloud = 'aws', region='us-east-1')

dims = 1024 # number of vector dims - relative to choice of embedding model

index_name = 'test-df'# name of remote vector database collection

if index_name not in pc.list_indexes().names():
	pc.create_index(name =index_name, dimension = dims, metric = 'cosine', spec=spec)

index = pc.Index(index_name)


#import embedding model
model_name = 'Alibaba-NLP/gte-large-en-v1.5'
model = SentenceTransformer(model_name, trust_remote_code=True)

#data = data[:1000] # subselection of data to test
#upsert the data
for review in data:
	if (review['text'] is not None) and (len(review['text'])>5) and (len(review['text'].split()) < dims):
		ascii_text = re.sub(r'[^\x00-\x7f]',r' ', review['text']) # enforce ASCII encoding for indices - but other index encoding is preferred
		vecs = [{'id': ascii_text), 'values' : model.encode(ascii_text).astype(np.float64)}]	
		try:
			index.upsert(vectors = vecs)
		except:
			#trouble shooting upsert errors
			pdb.set_trace()


