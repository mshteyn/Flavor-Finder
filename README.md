# FLAVOR FINDER

# Flavor Finder: A Restaurant-Based Dish Recomendation System

Flavor Finder provides query-specific menu item recommendations from local restaurants. Flavor Finder's recommendations are driven by curated summaries of user-submitted Google reviews.

## Introduction

Determing what to order in an unfamiliar restaurant is a challenge. Reviews can be a good guide. However, restaurant reviews are effortful to summarize and difficult to search through when user needs are specific. A recommendation system can help.

Recommendation systems enhance user satisfaction and facilitate exploration. Flavor Finder is a recommendation system that leverages Retrieval-Augmented 
Generation (RAG), based on a comprehensive database of Google user reviews, to deliver tailored restaurant-specific suggestions. For instance, this system can provide specific advice such as recommending a spicy yet gluten-free dish at Taj Mahal Indian Restaurant based on user-specific preferences, or a vegetarian appetizer at Noodlehead.


## Stakeholders

Flavor Finder's primary stakeholders are dining customers seeking specific 
dishes from restaurants that cater to their unique preferences and dietary requirements. 
Leveraging user reviews allows the system to provide personalized recommendations, 
enhancing the dining experience by suggesting dishes that align with individual tastes 
and restrictions. By utilizing the collective insights from numerous reviews of experienced eaters, the system can offer 
reliable recommendations, benefiting users by saving time, 
reducing decision fatigue, and increasing satisfaction with their dining choices.

Flavor Finder benefits businesses by streamlining time-costly service worker responsibilities. Flavor Finder's automated recommendation system enables service workers to redistribute effort and resources toward competing demands in high stress and fast-paced restaurant environments.


## Data Collection 
Restaurant reviews were retreived from Google Local and aggregated by Tianyang Zhang and Jiacheng Li at the University of California, San Diego for use in the following publication:

Personalized Showcases: Generating Multi-Modal Explanations for Recommendations
An Yan, Zhankui He, Jiacheng Li, Tianyang Zhang, Julian Mcauley
The 46th International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR), 2023

These data are made public at https://datarepo.eng.ucsd.edu/mcauley_group/gdrive/googlelocal/.

### Data Cleaning and Preprocessing

Reviews were filtered based on high ratings, considering only reviews rated at 3 stars out of 5 or better. Reviews fewer than 200 characters in length were removed. 

### Focus on Food-Related Mentions

To increase the signal-to-noise ratio, reviews that specifically mention food items were 
selected. A Named Entity Recognition (NER) model (InstaFoodRoBERTa-NER) was used to 
identify and filter reviews containing specific mention of food items. 


## Exploratory Data Analysis



## Modeling Approach

Text reviews were embedded as 1024 dimensional vectors using Alibaba's sentence transformer model (GTE-Large v1.5) and stored in a Pinecone vector database. User queries were embedded in the same way and compared to stored embeddings with cosine similarity. The top 5 closest reviews to the user query were retreived from the database and provided the context with which Llama 2 (13B Instruction-tuned) was prompted before generating a response to the user query.

## Challenges

Significant GPU resources are required to load the necessary components of the model.

Running some of the models on personal devices took too long to process 100,000 reviews, 
indicating the need for more powerful computational resources or distributed processing 
among multiple machines.


## Conclusion



## Future Directions



## Repository Description





