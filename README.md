# Flavor-Finder

# TEAM FLAVOR FINDER: Recommending Restaurant Dishes

Flavor Finder helps you Find your Favorite Flavor

Our main goal is the implementation of RAG informed by a database of user reviews 
to create a restaurant-specific recommendation system.


## Introduction

Traditionally, recommendation systems have been employed not only to drive commercial 
success but also to enhance user satisfaction and facilitate exploration in various 
fields. With the rise of sophisticated data analysis techniques in the 1990s, researchers 
began utilizing algorithms to analyze user data, creating personalized recommendations 
based on attributes like preferences, behavior, and feedback. The proliferation of 
accessible data and advancements in deep learning have transformed recommendation systems 
into a dynamic and rapidly evolving area of interest among data scientists. In this 
context, we have developed a recommendation system leveraging RAG (Retrieval-Augmented 
Generation), informed by a comprehensive database of user reviews, to deliver tailored 
restaurant-specific suggestions. For instance, this system can provide specific advice 
such as recommending a spicy yet gluten-free dish at Taj Mahal Indian Restaurant based on user-specific preferences.


## Stakeholders

The primary stakeholders of this recommendation system are users seeking specific 
dishes from restaurants that cater to their unique preferences and dietary requirements. 
Leveraging user reviews allows the system to provide personalized recommendations, 
enhancing the dining experience by suggesting dishes that align with individual tastes 
and restrictions. For instance, users can receive tailored advice on dishes that are 
spicy yet gluten-free, ensuring they enjoy meals that meet their expectations and health 
needs. By utilizing the collective insights from numerous reviews, the system can offer 
more accurate and reliable recommendations, ultimately benefiting users by saving time, 
reducing decision fatigue, and increasing satisfaction with their dining choices.


## Data Collection & Cleaning



### Filter Restaurant Reviews

Reviews were filtered based on high ratings, specifically considering only 4 or 5-star 
reviews to reduce noise. The original review database was processed in chunks to prevent 
RAM issues. The current database (~3.5GB) contains approximately 12 million reviews from 
around 70,000 restaurants.

### Remove Irrelevant Reviews

Short and excessively long reviews were considered for removal to maintain consistency 
and relevance.

### Focus on Food-Related Mentions

To increase the signal-to-noise ratio, reviews that specifically mention food items were 
selected. A Named Entity Recognition (NER) model (InstaFoodRoBERTa-NER) was employed to 
identify and filter reviews mentioning food items. This model performed well but was 
computationally intensive.


## Exploratory Data Analysis



## Modeling Approach



## Challenges

Running some of the models on personal devices took too long to process 100,000 reviews, 
indicating the need for more powerful computational resources or distributed processing 
among multiple machines.


## Conclusion



## Future Directions



## Repository Description





