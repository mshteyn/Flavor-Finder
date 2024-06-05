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


#MODEL_NAME = "TheBloke/Llama-2-7B-GGML"
#MODEL_NAME = "TheBloke/Llama-2-13b-Chat-GPTQ"


if torch.cuda.is_available():     
    MODEL_NAME = "TheBloke/Llama-2-13b-Chat-GPTQ"
    #MODEL_NAME =  "togethercomputer/Llama-2-7B-32K-Instruct" # Really long to load
    #MODEL_NAME ="TechxGenus/Meta-Llama-3-8B-GPTQ"    # This model works but talks to itself
    #MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"
    #MODEL_NAME = "TechxGenus/Meta-Llama-3-8B-GPTQ" 
    #MODEL_NAME = "Maykeye/TinyLLama-v0"    
    #tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True, token='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')
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)

    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.float16, trust_remote_code=True, device_map="cuda")
    device = torch.device("cuda")
    print('Cuda is Available. Model is: ', MODEL_NAME.split('/')[1])
else:

    #MODEL_NAME = "TheBloke/Llama-2-7B-GGML"
    #pdb.set_trace()    
    #MODEL_NAME = "Maykeye/TinyLLama-v0" # this works / Tiny&Fast implementation -- Terrible Output
    MODEL_NAME = "togethercomputer/Llama-2-7B-32K-Instruct" 
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.float16, trust_remote_code=True)
    print('CPU only. Model is: ', MODEL_NAME.split('/')[1])
 
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
 
# GENERATIVE LLM
llm = HuggingFacePipeline(pipeline=text_pipeline, model_kwargs={"temperature": 0})

 
# EMBEDDING MODEL
model_name  = 'Alibaba-NLP/gte-large-en-v1.5'
embedding_function = HuggingFaceEmbeddings(model_name=model_name, model_kwargs = {'trust_remote_code':True, 'device': device})


#if you want to do RAG
def chroma_search(query, chroma_dir):
        #pdb.set_trace()
        db = Chroma(persist_directory=chroma_dir, embedding_function=embedding_function)

        docs = db.similarity_search(query, k=5)
        context = ''

        print('\nThe most relevant reviews are: \n')
        for i, doc in enumerate(docs):
                print('Review #', i+1, doc.page_content)
                context += 'Reviewer ' + str(i+1) + ' says: ' +  doc.page_content + '. '
        return context

def pinecone_search(query, db_dir):
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
#db_select = input('\nWould you like a recommendation based on user reviews? Type: \n"Yes", or "Y" to consult our curated review database, \n"Raw" or "R" for an uncurated review database, or \n"Skip" to ignore user reviews: ')


from langchain import PromptTemplate

def take_query():

    query = input("\n\n\nWhat kind of food recommendation would you like?:  ")

    db_select = input('\nWould you like a recommendation based on user reviews? Type: \n"Yes" to consult our curated review database, or \n"No" to ignore user reviews: ')


    db_select = db_select.upper()

    # chroma DB
    search_db = chroma_search
    # pinecone DB
    #search_db = pinecone_search

    if db_select[0] == 'Y':
    #    chroma_dir = './OH_200c_named_db'
        chroma_dir = './PA_200c_named_db'    
    #    chroma_dir = './PA_100c_named_db'    
        pc_dir = 'pa-db'
        db_dir = pc_dir
        db_dir = chroma_dir
        context = search_db(query, db_dir)
    elif db_select[0] == 'R':
        chroma_dir = './test_PA_db'
        db_dir = chroma_dir
        context = search_db(db_dir)
    else:
        context = ''
    extra_instruction = ". If the question is not food-related, avoid answering. If the question is food related, answer in just two sentences maximum, using the following context in generating your answer, without mentioning the reviewer identity:"
 #   extra_instruction = ".  (Answer in just two sentences maximum, using the following context in generating your answer, without mentioning the reviewer identity:)"

    template = """<s>[INST] <<SYS>>"""+query+extra_instruction+"""<</SYS>>{text} [/INST]"""

     
    prompt = PromptTemplate(
        input_variables=["text"],
        template=template,
    )

    #context = input("What other reviewers are saying: ")
    #text = "Give me a recommendation for light dish at Apteka"

    out = llm(prompt.format(text=context))
    pdb.set_trace()
    print('\n'+out.split('[/INST]  ')[1])



exit = 0
while (exit ==0):
    take_query()

pdb.set_trace()




#from langchain.chains import LLMChain
#chain = LLMChain(llm=llm, prompt=prompt)
#result = chain.run(text)
#print(result)


