Web development for Chatbot: https://shwinda.medium.com/build-a-full-stack-llm-application-with-openai-flask-react-and-pinecone-part-1-f3844429a5ef 

Flask: Chatbot Flask web deployment
 ![Flowchart](image-1.png)
1.	Web scraping (an example case where user want to ask info of website) and call OpenAI's Embeddings API to create embeddings from the website's text.
2.	It also stores these embeddings in the vector database (Pinecone) and retrieves relevant text to help the LLM answer the user's question.


Project structure: replace embedding from openAI with ours embedding; and sent it to our vector databases;

![tools](image-2.png)
Resources:
1.	Flask documentation:
https://flask.palletsprojects.com/en/3.0.x/ 
Flask web framework example:
https://colab.research.google.com/drive/1JW21xBkM6ELVAH3TtMHVBkUyte-WT5kP#scrollTo=5Ou19wfS9PDe 


Updates:
1.	Flask installed;
2.	Linked Flask route with html templates;
3.  Blueprint register routes;
4.  How to let other people access the flask web deployment; 


Codes practice reference:
1.	https://medium.com/@mailsushmita.m/create-an-generative-ai-chatbot-using-python-and-flask-a-step-by-step-guide-ea39439cf9ed 


