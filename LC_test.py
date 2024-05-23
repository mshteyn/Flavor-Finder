import pdb
import torch
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

	model = AutoModelForCausalLM.from_pretrained(

	    MODEL_NAME, torch_dtype=torch.float16, trust_remote_code=True, device_map="auto")
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

query = input("\nWhat kind of food recommendation would you like?:  ")
 

# EMBEDDING MODEL
model_name  = 'Alibaba-NLP/gte-large-en-v1.5'
embedding_function = HuggingFaceEmbeddings(model_name=model_name, model_kwargs = {'trust_remote_code':True, 'device': device})
#load Vector DB
chroma_dir = './PA_Full_named_db'#once its ready..
chroma_dir = './test_PA_db' #for now
db = Chroma(persist_directory=chroma_dir, embedding_function=embedding_function)

docs = db.similarity_search(query, k=5)
context = ''

print('\nThe most relevant reviews are: \n')
for i, doc in enumerate(docs):
	print('Review #', i+1, doc.page_content)
	context += 'Reviewer ' + str(i+1) + ' says: ' +  doc.page_content + '. '


extra_instruction = ". Answer in just two sentences, maximum. Use the following context in generating your answer:"

template = """<s>[INST] <<SYS>>"""+query+extra_instruction+"""<</SYS>>{text} [/INST]"""

 
prompt = PromptTemplate(
    input_variables=["text"],
    template=template,
)


#context = input("What other reviewers are saying: ")
#text = "Give me a recommendation for light dish at Apteka"


print(llm(prompt.format(text=context)))

pdb.set_trace()

#from langchain.chains import LLMChain
#chain = LLMChain(llm=llm, prompt=prompt)
#result = chain.run(text)
#print(result)


