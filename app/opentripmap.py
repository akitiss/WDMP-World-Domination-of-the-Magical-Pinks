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
def get_places(city, radius, kind): 
    limit = 10 #make variable now 

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

def get_hotels(city):
    return get_places(city, 5000, "other_hotels")

def get_naughty(city):
    return get_places(city, 5000, "adult")

#x = get_naughty('Paris')
#print(x)