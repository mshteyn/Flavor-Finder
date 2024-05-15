import pdb
import torch
from langchain import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig, pipeline
 
MODEL_NAME = "TheBloke/Llama-2-7B-GGML"
#MODEL_NAME = "TheBloke/Llama-2-13b-Chat-GPTQ"


if torch.cuda.is_available(): 	
	MODEL_NAME = "TheBloke/Llama-2-13b-Chat-GPTQ"

	tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)

	model = AutoModelForCausalLM.from_pretrained(

	    MODEL_NAME, torch_dtype=torch.float16, trust_remote_code=True, device_map="auto")

	print('Cuda is Available. Model is: ', MODEL_NAME)
else:

	MODEL_NAME = "TheBloke/Llama-2-7B-GGML"
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
 
template = """
<s>[INST] <<SYS>>
Act as a Server giving specific and concise restaurant recommendations
<</SYS>>
 
{text} [/INST]
"""
 
prompt = PromptTemplate(
    input_variables=["text"],
    template=template,
)

text = "Give me a recommendation for light dish at Apteka"
print(prompt.format(text=text))

from langchain.chains import LLMChain
chain = LLMChain(llm=llm, prompt=prompt)
result = chain.run(text)
print(result)











pdb.set_trace()
