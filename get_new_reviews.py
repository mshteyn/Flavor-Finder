#This is a script to scrape fresh reviews from the google places API by using the find-nearby functionality


import os 
import requests 
import jsonlines 
import time 

assert type(os.environ.get("GOOGLE_PLACES_KEY")) != None, "Must set shell environment variable called GOOGLE_PLACES_KEY"

#You can hardcode your google places key if you must; but DO NOT share this document via github 
GOOGLE_PLACES_KEY = os.environ.get("GOOGLE_PLACES_KEY")
PLACES_URL_TEMPLATE= "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=LAT,LONG&radius=RADIUS&type=TYPE&maxResultCount=MAXCOUNT&key=YOUR_API_KEY"
REVIEW_URL_TEMPLATE = "https://maps.googleapis.com/maps/api/place/details/json?place_id=PLACE_ID&key=YOUR_API_KEY"


def make_places_url(latlong:tuple,radius:str,max_results=int(20)) -> str:
    """
    Using Google-Places Nearby Search: https://developers.google.com/maps/documentation/places/web-service/nearby-search

    Parameters
    ---
    latlong: <tuple> 
        tuple containing (latitude,longitude) of user 
    radius: <str> 
        search radius in meters  
    max_results: <int>
         max number of places to display 

    Returns
    ------
    
    url: <str> 
        exact url to pass requests to in order to get restaurants within radius

    """
    lat,long= latlong
    url = PLACES_URL_TEMPLATE.replace("LAT,LONG",str(lat)+","+str(long),1)
    url = url.replace("TYPE","restaurant",1)
    url = url.replace("RADIUS",str(radius),1)
    url = url.replace("MAXCOUNT",str(max_results),1)
    url = url.replace("YOUR_API_KEY",GOOGLE_PLACES_KEY,1)
    return url 

def make_reviews_url(place_id:str) -> str:
    """
    Using Google-Places Place Details: https://developers.google.com/maps/documentation/places/web-service/place-details

    Parameters
    ---------

    place_id: <str>
        unique place id taken from google places; this can be gotten from the 

    Returns
    ------

    url: <str> 
        exact url to pass requests to in order to get restaurants within radius
    """

    url = REVIEW_URL_TEMPLATE.replace("PLACE_ID",place_id,1)
    url = url.replace("YOUR_API_KEY",GOOGLE_PLACES_KEY,1)
    #url = url.replace("KEYWORD","",1)
    return url 

# ad = '1101 E FLORENCE AVE, LOS ANGELES, CALIFORNIA 90001' # this address does not work
# ad = '3400 san pablo ave, oakland, ca 946084234' # this address works
# address = ad.replace(' ', '%20') #make sure there are no blank spaces for the URL

def get_nearby_places(latlong:tuple[str],radius:str,max_places=int(10)) -> list[dict]: 
    """

    Using Google-Places Nearby Search: https://developers.google.com/maps/documentation/places/web-service/nearby-search

    Parameters
    --- 
    latlong: <tuple> 
        (latitude,longitude) cast as strings
    radius: <str>
        search radius around the latlong coordinates in meters (cast as a string)
    max-places: <int>
        max number of places to grab 

    Returns
    ---
    place_ids: <list>
        list containing dictionaries of places and names 
    """

    nearby_places_url = make_places_url(latlong,radius) 

    try: 
        response = requests.get(nearby_places_url,timeout= int(60))
        assert response.status_code == int(200), "status code was {}".format(response.status_code)
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as err_msg:
            print(err_msg)

    response = response.json() 
    places = list()

    #Form the json of nearby requested places 
    if len(response['results']) > 0:
      for result in response['results']: #Iterate over returned restaurants from the url 
          places.append({"place_id":result["place_id"],"name":result["name"],"avg_rating":result["rating"],"num_of_reviews":result["user_ratings_total"],\
                         "rough_address":result["vicinity"]})
    else:
        raise ValueError('Zero Restaurants Founds Within Radius')
    
    print("places found",places)
    return places
  
def get_reviews(places:list[dict])-> list[dict]:
    """
    Using Google-Places Place Details Function: https://developers.google.com/maps/documentation/places/web-service/place-details

    Parameters
    ----------
    places: <list> 
        - A list of dictionary objects containing at least a valid "place_id"

    Returns
    ------
    review_collection: <list>[dictionary]
        - A list containing dictionaries; each dictionary is a review with a 
        place_id, as well as text, an author name, and a rating.  
    """
    
    review_collection = list()

    for place in places: 
        place_id = place["place_id"]
        try:
            response = requests.get(make_reviews_url(place_id),timeout = 60)
            assert response.status_code == int(200), "status code was {}".format(response.status_code)
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
            print("Request Error")

        response = response.json() 
        
        all_reviews = response["result"]["reviews"]

        for review in all_reviews: #iterate over all reviews for the place with place_id; append to review_collection 
            short_review = dict()
            short_review["place_id"] = place["place_id"]
            short_review["rating"] = review["rating"]
            short_review["text"] = review["text"]
            short_review["relative_time_description"] = review["relative_time_description"]

            review_collection.append(short_review)

        time.sleep(1) #wait 1 second before calling google places api again 
    #print("reviews collected",review_collection)
    return review_collection


def write_reviews_json(review_collection:list[dict],filename:str = "new_reviews.jsonl",written_ids=None) -> None:
    """
    Writes collected reviews to a json-lines file (each line is its own json record).
    The default location is the current working directory. 
    
    Parameters
    -----------
    review_collection: <list> 
        list of dictionaries, each of which is a record 
    filename: <str> 
        filepath to where jsonl file will be written 

    Returns
    ------
    None
    """ 
    assert len(review_collection) > 0, "review collection must be nonempty list"
    assert type(review_collection[0]) == dict, "review collection be list of dictionary objects"

    with jsonlines.open(filename,'w') as writer:
        writer.write_all(review_collection) 
    
    return None 

def write_metadata_json(places:list[dict],filename="new_metadata.jsonl",written_ids = None) -> None:
    """
    Writes collected place metadata to json with name filename;
    default location is is current working directory

    Parameters
    ---------
    places: <list>
        - list of dictionaries containing the metadata associated to each unique place 
    filename: <str> 
        - filepath to where jsonl file will be written 

    Returns
    -----
    None
    """ 
    assert len(places) > 0, "place metadata collection must be nonempty list"
    assert type(places[0]) == dict, "place metadata must be list of dictionary objects"

    with jsonlines.open(filename,mode = 'w') as writer:
        writer.write_all(places) 

    return None 


if __name__ == "__main__":

    lat_example = str(33.9164023)  #lat and long example was taken from a restaurant in cali metadata 
    long_example = str(-118.01085499999999)
    radius_example = str(10) #radius in meters 
    MAX_PLACES = int(20)

    places = get_nearby_places((lat_example,long_example),radius_example)
    reviews = get_reviews(places)
    write_metadata_json(places)
    write_reviews_json(reviews)
