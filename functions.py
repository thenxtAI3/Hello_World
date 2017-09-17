# functions for each feature

import requests
import json
from pprint import pprint

def picture(pathway):
    import io
    import os
    from google.cloud import vision
    vision_client = vision.Client()
    file_name = os.path.join(
        os.path.dirname(__file__),'static/imaging/' + pathway)
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
        image = vision_client.image(
        content=content)
    texts = image.detect_text()
    print texts[0].locale
    print texts[0].description
    output = {'lang' : texts[0].locale, 'words' : texts[0].description}
    return output
def translate(source, target, user_input):
    my_key = 'AIzaSyA1Ox-CnVRe2684Lxqf_oXDjV0imAY1wx4'
    payload = {
        'key': my_key,
        'q': user_input,
        'source': source,
        'target': target,
        'format': 'text'
      }
    r = requests.get('https://translation.googleapis.com/language/translate/v2', params=payload)
    length = len(r.text)
    return (r.text[71:length - 22])
def search_places(query_search, places):
    from googleplaces import GooglePlaces
    YOUR_API_KEY = 'AIzaSyA1Ox-CnVRe2684Lxqf_oXDjV0imAY1wx4'
    google_places = GooglePlaces(YOUR_API_KEY)

    # You may prefer to use the text_search API, instead.
    query_result = google_places.text_search(
        query = query_search, radius = 200000)
    
    for i in range(10):
        places[i]["name"] = ""
        places[i]["rating"] = ""
        places[i]["address"] = ""
        places[i]["wesbite"] = ""
        places[i]["number"] = ""
    
    
    entry = 0    
    for place in query_result.places:
        # Returned places from a query are place summaries.
        place.get_details()
        places[entry]["name"] = str(place.name)
        rate = str(place.rating)
        places[entry]["rating"] = rate + u"\u2b50"
        places[entry]["address"] = str(place.formatted_address)
        places[entry]["wesbite"] = str(place.website)
        places[entry]["number"] = str(place.local_phone_number)
        entry += 1
        if (entry > 9): break
        print places
