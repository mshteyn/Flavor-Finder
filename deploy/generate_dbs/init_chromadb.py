#generate a vect:orstore in chroma
from langchain_chroma import Chroma
from langchain_community.document_loaders import JSONLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
import torch
import pdb
import sys
import gc
import datetime


import os
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:10000"

#file_name = '../data/test2.json'
#file_name = '../data/NamedRestaurants_PA.json'
#file_name = '../data/UnnamedRestaurants_PA.json'
#file_name = '../data/NamedRestaurants_PA.json'
#file_name = '../data/200chrestReviews_PA.json'
#file_name = '../data/100chrestReviews_PA.json'
file_name = '../data/200chrestReviews_OH.json'


#loader = JSONLoader(file_path=file_name, jq_schema='.[].text', text_content=False, json_lines=False)# for test2.json
loader = JSONLoader(file_path=file_name, jq_schema='.text', text_content=False, json_lines=True) # for everything else
data = loader.load()


#to GPU if available
if torch.cuda.is_available():
        device = torch.device("cuda")
#        device = torch.device("cpu")

else:
        device = torch.device("cpu")

torch.cuda.empty_cache() 
gc.collect()
model_name  = 'Alibaba-NLP/gte-large-en-v1.5'
embedding_function = HuggingFaceEmbeddings(model_name=model_name, model_kwargs = {'trust_remote_code':True, 'device': device})

raw_documents = data
#raw_documents = data[:100000]
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.split_documents(raw_documents)

# upsert docs and save DB in memory
del data #free some space
step_size = 10000
#steps = torch.arange(0,len(documents), 20000)
steps = torch.arange(0,len(documents), step_size)


#these are UNCLEAN raw jsons - first 1M reviews only (10% of dataset)
#chroma_dir = './test_PA_db'
#chroma_dir  = './test_PA_db_GPU'

#these are CLEAN jsons ~800k reviews w/ mentions of food
#chroma_dir = './PA_Full_named_db'
#chroma_dir = './PA_Full_unnamed_db'
chroma_dir = './PA_200c_named_db'
#chroma_dir = './PA_100c_named_db'
#chroma_dir = './OH_200c_named_db'


for chunk in range(len(steps))[1:]:
	docs = documents[steps[chunk-1]:steps[chunk]] 
	db = Chroma.from_documents(docs, embedding_function, persist_directory= chroma_dir)
	print('Chunk',str(chunk), ' complete:, ', str(datetime.datetime.now().time()))
	#sys.stdout.write('Chunk complete: '+str(chunk))
	gc.collect()


#Load DB if saved exists
#db3 = Chroma(persist_directory=chroma_dir, embedding_function=embedding_function)
#print(str(len(db3.get()['documents'])), 'saved documents loaded from ./chroma_db')

#test
query = "What's best to eat at Sheetz?"
docs = db.similarity_search(query)
#for doc in docs:
#	print(doc.page_content)

