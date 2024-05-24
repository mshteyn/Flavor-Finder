import pandas as pd
import pdb
import re
### Variables that you might want to modify:

#local path for California's Google reviews and metadata downloaded from
# https://datarepo.eng.ucsd.edu/mcauley_group/gdrive/googlelocal/#files
#reviews_path = '/Users/andres/Documents/Flavor Finder data/California Google Local Reviews.json'
#metadata_path = '/Users/andres/Documents/Flavor Finder data/California Local Reviews.json'

#reviews_path = '../data/review-Pennsylvania_10.json'#PA
#metadata_path = '../data/meta-Pennsylvania.json'#PA

reviews_path = '../data/review-California.json'
metadata_path = '../data/meta-California.json'

#local folder path where you want your clean data to be saved\
#FFreviews_path = '/Users/andres/Documents/Flavor Finder data/'
#FFmetadata_path = '/Users/andres/Documents/Flavor Finder data/'

FFreviews_path = '../data/'
FFmetadata_path = '../data/'

# number of reviews to read at a time, you might want it smaller if your computer doesn't have lots of RAM\
chunk_size = 10000

#min review rating to consider\
min_rating = 3

#Lists of columns to be dropped on each database\
#Original colums are\
    # reviews: ['user_id', 'name', 'time', 'rating', 'text', 'pics', 'resp', 'gmap_id']\
    # metadata ['name', 'address', 'gmap_id', 'description', 'latitude', 'longitude',\
           #'category', 'avg_rating', 'num_of_reviews', 'price', 'hours', 'MISC',\
           #'state', 'relative_results', 'url']\
ReviewColumnsToDrop = ['time','pics', 'resp']
MetadataColumnsToDrop = ['price', 'hours', 'MISC','state', 'relative_results', 'url']

#---------------------------------------------------------------------------------------------------------\

metadataDF = pd.read_json(metadata_path,lines=True)

##dropping metada rows that do not correspond to restaurants\

category_to_check = 'restaurant'
metadataDF = metadataDF.dropna(subset=['category'])
mask = metadataDF['category'].apply(lambda x: any(category_to_check in item for item in x)  )
metadataDF= metadataDF[mask]
metadataDF.drop(columns = MetadataColumnsToDrop, inplace = True)


##Reading and cleaning reviews in chunks\

#List of chunks, to be join as one data frame after processing \
chunks = []

# Iterate over the JSON file in chunks\
for chunk in pd.read_json(reviews_path, lines=True, chunksize=chunk_size):
    
    #dropping columns that won't be used\
    chunk.drop(columns = ReviewColumnsToDrop, inplace = True)
    
    #dropping reviews with rating < min_rating\
    mask = chunk.rating >= min_rating
    chunk = chunk[mask]

    #dropping reviews with no text\
    chunk['text'] = chunk['text'].str.replace('[^A-Za-z0-9]', ' ', flags=re.UNICODE)
    chunk = chunk.dropna(subset=['text'])
    chunk = chunk[chunk['text'].str.len()>=100] #keep reviews > 100 characters
    #pdb.set_trace()
    #filtering reviews of restaurants\
    chunk = chunk[chunk['gmap_id'].isin(metadataDF['gmap_id'])]
    
    #adding the cleaned data to the list of chunks\
    chunks.append(chunk)
    

reviewsDF = pd.concat(chunks, ignore_index=True)
metadataDF.to_json(FFreviews_path + 'datarestMetadata_CA.json', orient='records', lines=True)
reviewsDF.to_json(FFreviews_path + 'datarestReviews_CA.json', orient='records', lines=True)
