import pdb
import torch
import os
import constants
from langchain import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig, pipeline
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

import warnings
warnings.filterwarnings("ignore")


MODEL_NAME = "TheBloke/Llama-2-7B-GGML"
#MODEL_NAME = "TheBloke/Llama-2-13b-Chat-GPTQ"


if torch.cuda.is_available():     
    MODEL_NAME = "TheBloke/Llama-2-13b-Chat-GPTQ"

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)

    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.float16, trust_remote_code=True, device_map="auto")
    device = torch.device("cuda")
    print('Cuda is Available. Model is: ', MODEL_NAME)
else:

    #MODEL_NAME = "TheBloke/Llama-2-7B-GGML"
    pdb.set_trace()    
    device = torch.device("cpu")    
    MODEL_NAME = "HirCoir/TinyLlama-1.1B-Chat-v1.0-GGUF" 
    from ctransformers import AutoModelForCausalLM
    llm = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
 
 
 
generation_config = GenerationConfig.from_pretrained(MODEL_NAME)
generation_config.max_new_tokens = 1024
generation_config.temperature = 0.0001
generation_config.top_p = 0.95
generation_config.do_sample = True
generation_config.repetition_penalty = 1.15
 
text_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    generation_config=generation_config,
)
 
llm = HuggingFacePipeline(pipeline=text_pipeline, model_kwargs={"temperature": 0})



from langchain import PromptTemplate

query = input("\n\n\nWhat kind of food recommendation would you like?:  ")
 
#pdb.set_trace()
# EMBEDDING MODEL
model_name  = 'Alibaba-NLP/gte-large-en-v1.5'
embedding_function = HuggingFaceEmbeddings(model_name=model_name, model_kwargs = {'trust_remote_code':True, 'device': device})


#if you want to do RAG
def chroma_search(chroma_dir):
        #pdb.set_trace()
        db = Chroma(persist_directory=chroma_dir, embedding_function=embedding_function)

        docs = db.similarity_search(query, k=10)
        context = ''

        print('\nThe most relevant reviews are: \n')
        for i, doc in enumerate(docs):
                print('Review #', i+1, doc.page_content)
                context += 'Reviewer ' + str(i+1) + ' says: ' +  doc.page_content + '. '
        return context

def pinecone_search(db_dir):
    from pinecone import Pinecone
    from langchain_pinecone import PineconeVectorStore  
    pinecone_api_key = os.environ['PINECONE_API_KEY']
    pc = Pinecone(api_key=pinecone_api_key)      
    index = pc.Index(db_dir)
    vectorstore = PineconeVectorStore( index, embedding=embedding_function)
    docs = vectorstore.similarity_search(query, k=5)
    context = ''
    print('\nThe most relevant reviews are: \n')
    for i, doc in enumerate(docs):
            print('Review #', i+1, doc.page_content)
            context += 'Reviewer ' + str(i+1) + ' says: ' +  doc.page_content + '. '    
    return context


#load Vector DB
#db_select = input('\nWould you like a recommendation based on a database of user reviews? Type: \n"Named", for the named database, \n"Unnamed" for the unnamed database, \n"Raw" for the raw database, and \n"Skip" to ignore RAG: ')

db_select = input('\nWould you like a recommendation based on user reviews? Type: \n"Yes", or "Y" to consult our curated review database, \n"Raw" or "R" for an uncurated review database, or \n"Skip" to ignore user reviews: ')

db_select = db_select.upper()

# chroma DB
#search_db = chroma_search
# pinecone DB
search_db = pinecone_search

if db_select[0] == 'Y':
#    chroma_dir = './OH_200c_named_db'
    chroma_dir = './PA_200c_named_db'    
#    chroma_dir = './PA_100c_named_db'    
    pc_dir = 'pa-db'
    db_dir = pc_dir
    context = search_db(db_dir)
elif db_select[0] == 'R':
    chroma_dir = './test_PA_db'
    db_dir = chroma_dir
    context = search_db(db_dir)
else:
    context = ''

extra_instruction = ". (Answer in just two sentences, maximum, and please  se the following context in generating your answer:)"

template = """<s>[INST] <<SYS>>"""+query+extra_instruction+"""<</SYS>>{text} [/INST]"""

 
prompt = PromptTemplate(
    input_variables=["text"],
    template=template,
)


#context = input("What other reviewers are saying: ")
#text = "Give me a recommendation for light dish at Apteka"


out = llm(prompt.format(text=context))

print('\n'+out.split('[/INST]  ')[1])

pdb.set_trace()

#from langchain.chains import LLMChain
#chain = LLMChain(llm=llm, prompt=prompt)
#result = chain.run(text)
#print(result)


