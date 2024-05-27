# FLAVOR FINDER

# Flavor Finder: A Restaurant-Based Dish Recomendation System

Flavor Finder provides query-specific menu item recommendations from local restaurants. Flavor Finder's recommendations are driven by curated summaries of user-submitted Google reviews.

## Introduction

Determing what to order in an unfamiliar restaurant is a challenge. Restaurant reviews can be a good guide. However, reviews are effortful to summarize and difficult to search through when user needs are specific. A recommendation system can help.

Recommendation systems enhance user satisfaction and facilitate exploration. Flavor Finder is a recommendation system that leverages Retrieval-Augmented 
Generation (RAG), based on a comprehensive database of Google user reviews, to deliver tailored restaurant-specific suggestions. For instance, this system can provide specific advice such as recommending a spicy yet gluten-free dish at Taj Mahal Indian Restaurant based on user-specific preferences.


## Stakeholders

Flavor Finder has two kinds of stakeholders. The primary stakeholders are dining customers seeking specific 
dishes from restaurants that cater to their unique preferences and dietary requirements. 
Leveraging user reviews allows the system to provide personalized recommendations, 
enhancing the dining experience by suggesting dishes that align with individual tastes 
and restrictions. By utilizing the collective insights from numerous reviews of experienced eaters, the system can offer 
reliable recommendations, benefiting users by saving time, 
reducing decision fatigue, and increasing satisfaction with their dining choices.

Flavor Finder benefits businesses by streamlining time-costly service worker responsibilities. Flavor Finder's automated recommendation system enables service workers to redistribute effort and resources toward competing demands in high stress and fast-paced restaurant environments.


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





