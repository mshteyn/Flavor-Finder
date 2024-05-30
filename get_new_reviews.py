
"""
Will Porteous, 05/29/24 
#This is a script to scrape fresh restaurant reviews from the google places API by using the find-nearby functionality
"""

import os 
import requests 
import jsonlines 
import time 
from outscraper import ApiClient 

assert type(os.environ.get("GOOGLE_PLACES_KEY")) != None, "Must assign environment variable called GOOGLE_PLACES_KEY"

#It is possible, though very bad practice, to hardcode your google places key here 

GOOGLE_PLACES_KEY = os.environ.get("GOOGLE_PLACES_KEY")
OUTSCRAPER_API_KEY = os.environ.get("OUTSCRAPER_API_KEY")

PLACES_URL_TEMPLATE= "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=LAT,LONG&radius=RADIUS&type=TYPE&maxResultCount=MAXCOUNT&key=YOUR_API_KEY"
REVIEW_URL_TEMPLATE = "https://maps.googleapis.com/maps/api/place/details/json?place_id=PLACE_ID&key=YOUR_API_KEY"
PLACE_TYPES = ["restaurant","bar","cafe"]

def make_places_url(latlong:tuple,radius:str,type="restaurant",max_results=int(20)) -> str:
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
    type: <str>
        must be supported option from 
        https://developers.google.com/maps/documentation/places/web-service/supported_types

    Returns
    ------
    
    url: <str> 
        
        exact url to pass requests to in order to get restaurants within radius

    """
    assert type in PLACE_TYPES, "invalid type choice: <type> must be one of {}".format(PLACE_TYPES)

    lat,long= latlong
    url = PLACES_URL_TEMPLATE.replace("LAT,LONG",str(lat)+","+str(long),1)
    url = url.replace("TYPE",type,1)
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

def get_nearby_places(latlong:tuple[str],radius:str,max_places=int(20),expanded = False) -> list[dict]: 
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
    expanded: <bool>
        increase number of types of places from restaurant to all types in PLACE_TYPES

    Returns
    ---
    place_ids: <list>
        list containing dictionaries of places and names 
    """

    types_to_use = ["restaurant"]
    places = list()
    num_calls = int(0)

    if expanded: 
        types_to_use = PLACE_TYPES.copy() #iterate over PLACE_TYPES 

    for place_type in types_to_use: 

        nearby_places_url = make_places_url(latlong,radius,type = place_type) 

        try: 
            response = requests.get(nearby_places_url,timeout= int(60))
            assert response.status_code == int(200), "status code was {}".format(response.status_code)
            num_calls += 1 
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as err_msg:
                print(err_msg)

        response = response.json() 
    
        #Form the json of nearby requested places 
        if len(response['results']) > 0:
            for result in response['results']: #Iterate over returned places from the url 
                places.append({"place_id":result["place_id"],"name":result["name"],"avg_rating":result["rating"],"num_of_reviews":result["user_ratings_total"],\
                                "types":result["types"],"rough_address":result["vicinity"]})
        else:
            pass 

    assert len(places) > 0, "list of places fails len(places) > 0"

    # while "next_page_token" in response: 
    #     next_page_token = response["next_page_token"]

    return places, num_calls 

  
def get_reviews(places:list[dict],limit = int(100))-> list[dict]:
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
    api_client = ApiClient(api_key=OUTSCRAPER_API_KEY)
    review_collection = list()
    num_calls = int(0)

    for place in places: 
        place_id = place["place_id"]
        #try:
        should = input('Use outscraper to grab reviews? [y]/n')
        if 'y' in should:
            scrape = True 
        else:
            scrape = False 
    
        if scrape: 
            results = api_client.google_maps_reviews(place_id, reviews_limit=limit)
            num_calls += 1 

            all_reviews = results[0]["reviews_data"] 
        #response = requests.get(make_reviews_url(place_id),timeout = 60)
        #assert response.status_code == int(200), "status code was {}".format(response.status_code)
        num_calls += 1 
       # except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
        #    print("Request Error")

        #response = response.json() 
        
        #all_reviews = response["result"]["reviews"]

        #print("Length of reviews grabbed",len(all_reviews))

        for review in all_reviews: #iterate over all reviews for the place with place_id
            short_review = dict()   #short review is the dict containing only relevant information 
            short_review["place_id"] = place["place_id"]
            short_review["rating"] = review["review_rating"]
            short_review["text"] = review["review_text"]
            #short_review["relative_time_description"] = review["relative_time_description"]

            review_collection.append(short_review) #add short review to the collection 

        time.sleep(1) #wait 1 second before calling google places api again 

    return review_collection, num_calls 


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

def locationCoordinates():
    """
    Parameters
    ---------- 
    None 

    Returns
    ------

    """
    try:
        response = requests.get('https://ipinfo.io') #just grab your ip info from website rather than access PC info 
        data = response.json()
        loc = data['loc'].split(',')
        lat, long = float(loc[0]), float(loc[1])
        city = data.get('city', 'Unknown')
        state = data.get('region', 'Unknown')
        return lat, long, city, state
        #return lat, long
    except:
        print("Internet Not avialable")
        exit()
        return Falses


if __name__ == "__main__":

    #lat,long,_,__ = locationCoordintes() 

    lat_example = str(40.4659334342321)  #lat and long example was taken from Apteka restaurant 
    long_example = str(-79.94937925548174)
    radius_example = str(20) #radius in meters 
    MAX_PLACES = int(20)
    review_limit = int(1500)
    places,num_nearby_calls = get_nearby_places((lat_example,long_example),radius_example,max_places = MAX_PLACES,expanded = True)
    reviews,num_details_calls = get_reviews(places,review_limit)

    print("{} Places Gathered in {} Calls to Nearby Search".format(len(places),num_nearby_calls))

    print("{} Reviews Gathered in {} Calls to Place Details".format(len(reviews),num_details_calls))

    #print("Reviews Obtained",reviews)

    write_metadata_json(places,"metadata_near_apteka.jsonl")
    write_reviews_json(reviews,"reviews_near_apteka.jsonl")

    #Add restaurant one-off via keyword; maybe make separate place_id functionality
    
    """
    List of restaurants to search: 
    list of restaurants: ['The Dandelion', 'Shady Maple Smorgasbord', 
    'Parc', 'Federal Galley', 'Gaucho Parrilla Argentina', 'Sienna Mercato', 
    "Gracie's On West Main", "Del Frisco's Double Eagle Steakhouse", 'The Bayou Southern Kitchen and Bar', 
    'NaBrasa Brazilian Steakhouse', 'Salem Halal Market & Grill', "Nifty Fifty's (Northeast Philadelphia)",
    'Frankford Hall', 'Zahav', 'Central Diner & Grille', 'Suraya Restaurant', 'Noodlehead', "Dalessandro's Steaks", 
    'Terakawa Ramen', "Monk's Cafe", "Cooper's Seafood House", 'Founding Farmers King of Prussia', 'El Vez', 'Dim Sum Garden',"Pat's King of Steaks"] 
    """