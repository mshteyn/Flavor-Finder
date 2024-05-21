#!/bin/bash
echo "downloading reviews" 

curl -o reviews_kcore.json https://datarepo.eng.ucsd.edu/mcauley_group/gdrive/googlelocal/review-California_10.json.gz

echo "review download complete; downloading metadata"

curl -o metadata_kcore.csv https://datarepo.eng.ucsd.edu/mcauley_group/gdrive/googlelocal/rating-California.csv.gz

echo "metadata download complete" 
