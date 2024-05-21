#!/bin/bash
echo "downloading reviews" 

curl -o reviews_kcore_json.gz https://datarepo.eng.ucsd.edu/mcauley_group/gdrive/googlelocal/review-California_10.json.gz

echo "review download complete; downloading metadata"

curl -o metadata_kcore_csv.gz https://datarepo.eng.ucsd.edu/mcauley_group/gdrive/googlelocal/rating-California.csv.gz

echo "metadata download complete" 

#Unzip both files 

gunzip metdata_kcore_csv.gz 
gunzip reviews_kcore_json.gz 