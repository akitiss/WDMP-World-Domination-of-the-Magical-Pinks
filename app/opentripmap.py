import requests

'''
can get hotel picture from: https://opentripmap.io/docs#/Objects%20list/getListOfPlacesByRadius gives link smwr
also can get wikipedia link
'''
try:
    with open("keys/key_opentripmap.txt") as file:
        key = file.read()
except FileNotFoundError:
    print("No 'key_opentripmap.txt' file found in keys dir")
    key = None

#image, name, location, wikpedia link, description 
def get_place(city, radius, kind, limit): 

    city_info = f"https://api.opentripmap.com/0.1/en/places/geoname?name={city}&apikey={key}"
    city_json = requests.get(city_info)
    city_format = city_json.json()
    coords = { 'lon': city_format['lon'], 'lat' : city_format['lat']}

    places_info = f"https://api.opentripmap.com/0.1/en/places/radius?radius={radius}&lon={coords['lon']}&lat={coords['lat']}&kinds={kind}&format=GeoJSON&limit={limit}&apikey={key}"
    places_json = requests.get(places_info)
    places = places_json.json()
    places_list =[]
    for dictionary in places:
        places_list.append( (dictionary['name'], dictionary['xid']) )
    # places_dict = {}

    master_place_details = {}
    for place in places_list:
        place_details_url = f"https://api.opentripmap.com/0.1/en/places/xid/{place[1]}?apikey={key}"
        place_json = requests.get(place_details_url)
        place_dict = place_json.json() #very specific for one place
        
        
        lat,lon = place_dict['point']['lat'], place_dict['point']['lon']
        deets= {'xid': place[1], 'lat': lat, 'lon': lon}
        if 'url' in place_dict:
            url = place_dict['url']
            deets['url'] = url
        else:
            url = place_dict['otm']
            deets['url'] = url
        
        if 'image' in place_dict:
            img = place_dict['image']
            deets['img'] = img

        if 'wikipedia_extracts' in place_dict:
            wiki_extract = place_dict['wikipedia_extracts']['text']
            deets['wiki_extract'] = wiki_extract
        

        master_place_details[place[0]] = deets

    # print(master_place_details)
    # print(places_list)
    return master_place_details

# GONNA CHANGE A BIT, so the loop keeps going until to reaches the limit, eg. if the user chooses 10 places and 7 categories, they get 10 places with some repeats instead of 7
# def get_places(city, radius, categories, limit ):
#     places_max = int(limit / len(categories)) 
#     details_master = {}
#     for category in categories:
#         details_master.update(get_place(city, 5000, category, places_max))
#     return details_master

def get_places(city, radius, categories, limit ):
    base_limit = int(limit / len(categories))
    over = limit - (len(categories) * base_limit) # add extra places lost by the base_lim calculation
    places = []
    for category in categories:
        LIM = base_limit
        if(over > 0):
            LIM+=1
            over-=1
        list = (get_place(city, radius, category, 25))
        for place_name in list: # will skip if no entry
            if(LIM > 0):
                if(place_name != ""): # will skip if there is no name
                    entry = {
                        place_name: list[place_name]
                    }
                    places.append(entry)
                    LIM-=1
    return places

def get_hotels(city, limit):
    return get_place(city, 5000, "other_hotels", limit)

def get_(city, limit):
    return get_places(city, 5000, "other_hotels", limit)

def get_naughty(city, limit):
    return get_place(city, 5000, "adult", limit)

#places_dict = get_places("LONDON", 5000, ['natural', 'hot_springs', 'volcanoes', 'museums', 'art_galleries'], 10) 
#print(places_dict)
# y = get_place("LONDON", 5000, 'beaches', 15)
# print(y)
# x = get_places('Athens', 5000, ['natural', 'hot_springs', 'volcanoes', 'beaches'], 10)
# print(x)

Endpoints = ['natural', 'hot_springs', 'volcanoes', 'beaches', 'museums', 'art_galleries', 'adult', 'circuses', 'historical_places', 'castles', 'churches', 'architecture', 'amusements', 'sport', 'casino', 'malls', 'foods']
#x = get_naughty('Paris', 10)
