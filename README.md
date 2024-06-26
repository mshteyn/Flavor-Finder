# FLAVOR FINDER

# Flavor Finder: A Restaurant-Based Dish Recomendation System
![FF_gif_crop3](https://github.com/mshteyn/Flavor-Finder/assets/5659756/558df18a-002f-4898-802e-c6df198492aa)



Flavor Finder provides query-specific menu item recommendations from local restaurants. Flavor Finder's recommendations are driven by curated summaries of user-submitted Google reviews.

## Introduction

Determing what to order in an unfamiliar restaurant is a challenge. Though restaurant reviews can be a good guide, they are effortful to summarize and difficult to search through when user needs are specific. A recommendation system can help.

Flavor Finder is a chat-based recommendation system that leverages Retrieval-Augmented Generation (RAG), based on a comprehensive database of Google user reviews, to deliver tailored restaurant-specific suggestions. For instance, Flavor Finder can provide a natural language based recommendation for a vegetarian appetizer at Noodlehead or a chicken-based entree at Sichuan Gourmet.


## Stakeholders

Flavor Finder's primary stakeholders are dining customers seeking specific 
dishes from restaurants that cater to their unique preferences and dietary requirements. 
Leveraging user reviews allows the system to provide personalized recommendations, 
enhancing the dining experience by suggesting dishes that align with individual tastes 
and restrictions. By utilizing the collective insights from numerous reviews of experienced eaters, the system can offer 
reliable recommendations, benefiting users by saving time, 
reducing decision fatigue, and increasing satisfaction with their dining choices.

Flavor Finder benefits businesses by reducing burden on service staff. Flavor Finder's automated recommendation system enables service workers to redistribute effort and resources toward competing demands in high stress and fast-paced restaurant environments.


## Data Collection 
Restaurant reviews were retreived from Google Local and aggregated by Tianyang Zhang and Jiacheng Li at the University of California, San Diego for use in the following publication:

Personalized Showcases: Generating Multi-Modal Explanations for Recommendations
An Yan, Zhankui He, Jiacheng Li, Tianyang Zhang, Julian Mcauley
The 46th International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR), 2023

These data are made public at https://datarepo.eng.ucsd.edu/mcauley_group/gdrive/googlelocal/.

### Data Cleaning and Preprocessing

The raw database consisted of over 13 million reviews from over 800,000 businesses in the Common Wealth of Pennsylvania.


Reviews were first filtered based on high ratings, considering only reviews rated at 4 stars out of 5 or better to highlight positive dining experiences. We only considered reviews with at least 200 characters in length and with no more than 1000 characters to reduce noise from reviews that might otherwise focus on aspects such as ambiance or service. 


### Focus on Food-Related Mentions

To increase the signal-to-noise ratio of our recommendation system, reviews that specifically mention food items were 
selected. A Named Entity Recognition (NER) model (InstaFoodRoBERTa-NER) was used to 
identify and filter reviews containing specific mention of food items. 

Our final database consisted of 190,000 restaurant reviews from over 20,000 independent restaurants.

## Exploratory Data Analysis
<p align="center"><img width="595" alt="image" src="https://github.com/mshteyn/Flavor-Finder/assets/5659756/b81f3412-1321-4985-a996-16e6005904f4"></p>

Visualization of restaurants in the Philadelphia area sorted by how many times they have been reviewed by users through the Google Local API.

<p align="center"><img width="595" alt="image" src="https://github.com/mshteyn/Flavor-Finder/assets/5659756/68757978-b769-4d33-b440-606f6d24fff3"></p>

Histogram depicts the lenghts of reviews stored in our vector database.

## Modeling Approach

Text reviews were embedded as 1024 dimensional vectors using Alibaba's sentence transformer model (GTE-Large v1.5) and stored in a Pinecone vector database. User queries were embedded at runtime and compared to stored embeddings with cosine similarity. The top 5 closest reviews to the user query were retreived from the database and provided the context with which Llama 2 (13B Instruction-tuned) was prompted before generating a response to the user query.

<p align="center"><img width="795" alt="image" src="https://github.com/mshteyn/Flavor-Finder/assets/5659756/db1b84ab-03ac-4e76-bce6-560095833834"></p>

Worflow.

## Model Evaluation

<p align="center"><img width="595" alt="image" src="https://github.com/mshteyn/Flavor-Finder/assets/5659756/1f94619f-a02e-4a08-a662-10c69de33312"></p>

A reduced-dimensional representation of a sample query embedding, stored embeddings that share metadata with the target restaurant, and stored embeddings that are not relevant to the user query. Embeddings representing 10% of the total vector database are depicted.

<p align="center"><img width="595" alt="image" src="https://github.com/mshteyn/Flavor-Finder/blob/main/evals/Evaluation.png?raw=true"></p>

We evaluated 20 local restaurants representing a variety of cuisines, including Italian, Maxican, Chinese, and more. each with >100 reviews. For each restaurant, customized questions were posed to assess dish recommendations. Example questions include:
- "If I want the best sandwich, what should I get at Central Diner & Grille?"
- "I don't like mushrooms, what dish do you recommend at Vedge?"

Three reviewers manually graded responses generated by three models: (1) standard pre-trained Llama 2; (2) Flavor-Finder; (3) GPT-4. Scores range from 0 to 4, based on whether the recommended dish is a real menu item from the specific restaurant and whether the recommendation was relevant to the user's question. 

Flavor-Finder achieved an average score of 3.1 out of 4, outperforming the original Llama 2 model, which scored 2.6 out of 4. 


## Challenges

GPU resources are required to perform inference efficient.

Updating the vector database requires access to subscription-based Google API keys which were beyond our budget. We've developed a tool that enables live scrapping of the Google Local API to perform database updates which we have updated within the limits of free use. As a result, our vector database is necessarily dated by the age of the dataset we had access to, containing reviews through 2020.



## Future Directions

We are in the process of deploying the model for user testing and integrating live API calls to both update our vector store and enhance retreival.


## Repository Description





