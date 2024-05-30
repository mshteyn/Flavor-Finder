#file by Will to examine the dataset and manipulate it

import pandas as pd 





if __name__ == "__main__":
    
    reviews_path  = "reviews_kcore_json"
    metadata_path = "metadata_kcore_csv"

    df_metadata = pd.read_csv(metadata_path)
    print(df_metadata.head(10))
    #reviews = pd.read_json(reviews_kcore_json)







