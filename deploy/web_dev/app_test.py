from flask import Flask, render_template, request, jsonify
from langchain import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig, pipeline
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import torch
from langchain import PromptTemplate
import pdb
#import constants

#if a==1:    
if torch.cuda.is_available():    
    MODEL_NAME = "TheBloke/Llama-2-13b-Chat-GPTQ" # original working model
    #MODEL_NAME = "TechxGenus/Meta-Llama-3-8B-GPTQ" # Llama 3 8B?
    #MODEL_NAME = "togethercomputer/Llama-2-7B-32K-Instruct"
    
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.float16, trust_remote_code=True, device_map="cuda")
    device = torch.device("cuda") 
    print('Cuda is Available. Model is: ', MODEL_NAME)
else:
    #MODEL_NAME = "microsoft/DialoGPT-medium" # mixed reponses
    #MODEL_NAME = "TheBloke/Llama-2-7B-GGUF" # can't get this to load (MRS 5/29)
    MODEL_NAME = "togethercomputer/Llama-2-7B-32K-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    device = torch.device("cpu")


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

#if you want to do RAG with local DB
def chroma_search(query, chroma_dir):
        #pdb.set_trace()
        db = Chroma(persist_directory=chroma_dir, embedding_function=embedding_function)

        docs = db.similarity_search(query, k=5)
        context = ''

        print('\nThe most relevant reviews are: \n')
        for i, doc in enumerate(docs):
                print('Review #', i+1, doc.page_content)
                #context += '' +  doc.page_content + '. '            
                context += 'Reviewer ' + str(i+1) + ' says: ' +  doc.page_content + '. '
        print(context)
        return context
#if you want to do RAG with cloud DB
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
        if i == 0:
            #print('Review #', i+1, doc.page_content)
            #context += 'One reviewer says: ' +  doc.page_content + '. ' #depracated 5/28
            print('Review #', i+1, doc.page_content)
            context += '' +  doc.page_content + '. '            
        else:
            context += '' +  doc.page_content + '. '
            
    return context

app = Flask(__name__)

#restaurant input
@app.route("/")
def index_1st_stp():
    return render_template('index.html')


# @app.route("/get_restaurant", methods=["GET", "POST"])
# def restaurant_chat():
#     input = request.form["msg"]
#     return 'Please enter dish query'


# def send_restaurant(text):
#     #send to pipeline for selection of reviews on restaurant
#     pdb.set_trace()
#     return 'Please enter dish query'
    
#request input

@app.route("/get_request", methods=["GET", "POST"])
def request_agin():
    input = request.form["msg"]
    return get_Request_response(input)


@app.route("/get_restaurant", methods=["GET", "POST"])
def request_chat():
    input = request.form["msg"]
    return get_Request_response(input)


def get_Request_response(text):
    query = text # user query
    #db_select = input('\nWould you like a recommendation based on user reviews? Type: \n"Yes" to consult our curated review database, or \n"No" to ignore user reviews: ')
    #db_select = request.form['msg']
    db_select = 'Y'    # Always use the databse for your recommendation
    db_select = db_select.upper()
    search_db = chroma_search # if you want to use the chromadb (local)
    # search_db = pinecone_search #if you want to use the pineconedb (cloud)

    if db_select[0] == 'Y': # context desired
         chroma_dir = '../scripts/PA_200c_named_db'
         pc_dir = 'pa-db'
         db_dir = pc_dir
         db_dir = chroma_dir
         context = search_db(query, db_dir)
    else:
        context = ''

    extra_instruction = ". (Answer in just two sentences, maximum. Avoid answering if the question is not food-related. And please summarize the following reviews to guide your answer:)"

    template = """<s>[INST] <<SYS>>"""+query+extra_instruction+"""<</SYS>>{text} [/INST]"""


    prompt = PromptTemplate(
            input_variables=["text"],
            template=template,
        )
    #pdb.set_trace()
    out = llm(prompt.format(text=context))
    return '\n'+out.split('[/INST]  ')[1]

@app.route("/reset", methods=["POST"])
def reset():
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port=8123)
