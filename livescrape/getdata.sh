#!/bin/bash


echo "downloading reviews" 

curl -o reviews_cali_json.gz https://datarepo.eng.ucsd.edu/mcauley_group/gdrive/googlelocal/review-California.json.gz

echo "review download complete; downloading metadata"

curl -o metadata_cali_json.gz https://datarepo.eng.ucsd.edu/mcauley_group/gdrive/googlelocal/meta-California.json.gz

echo "metadata download complete" 

#Unzip both files 
echo "unzipping metadata"

gunzip metadata_cali_json.gz

echo "unzipping reviews"

gunzip reviews_cali_json.gz 