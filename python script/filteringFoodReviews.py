#!pip install huggingface-hub
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import pandas as pd

tokenizer = AutoTokenizer.from_pretrained("Dizex/InstaFoodRoBERTa-NER")
model = AutoModelForTokenClassification.from_pretrained("Dizex/InstaFoodRoBERTa-NER")

# Initialize the NER pipeline
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer)

def contains_food_item(text):
    """
    Function to check if a text contains any food item.
    """
    # Get the NER results
    ner_results = ner_pipeline(text)

    # Check if any of the entities is a food item
    for entity in ner_results:
        if "FOOD" in entity['entity']:
            return True
    return False


## Example usage
#texts = [
#    "I had a great time at the restaurant.",
#    "We enjoyed a delicious pizza for dinner.",
#    "The best meal ever.",
#    "They baked a wonderful chocolate cake."
#]

## Identify strings containing food items
#food_texts = [text for text in texts if contains_food_item(text)]

#print("Texts containing food items:")
#for text in food_texts:
#    print(text)

reviews_path = '/Users/andres/Documents/Flavor Finder data/restReviews.json'

#This takes a lot of time. 
chunk_size = 5000

#List of chunks, to be join as one data frame after processing 
chunks = []

#i = 0

## Iterate over the JSON file in chunks
for chunk in pd.read_json(reviews_path, lines=True, chunksize=chunk_size):
    #i = i+1
        
    #filtering reviews with no food mentions
    mask = chunk['text'].apply(lambda x: contains_food_item(x))
    chunk = chunk[mask]
    
    chunks.append(chunk)
    #print(i)

reviewsDF = pd.concat(chunks, ignore_index=True)
reviewsDF.to_json('/Users/andres/Documents/Flavor Finder data/cleanRestReviews.json', orient='records', lines=True)