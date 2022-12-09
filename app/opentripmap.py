import requests

'''
can get hotel picture from: https://opentripmap.io/docs#/Objects%20list/getListOfPlacesByRadius gives link smwr
also can get wikipedia link
'''
key = "5ae2e3f221c38a28845f05b6f33412d1f6da84b5fd8eccc6b2a3fb05"

def get_places(city, radius, kind): 
    limit = 10

    city_info = f"https://api.opentripmap.com/0.1/en/places/geoname?name={city}&apikey={key}"
    city_json = requests.get(city_info)
    city_format = city_json.json()
    coords = { 'lon': city_format['lon'], 'lat' : city_format['lat']}

    places_info = f"https://api.opentripmap.com/0.1/en/places/radius?radius={radius}&lon={coords['lon']}&lat={coords['lat']}&kinds={kind}&format=GeoJSON&limit={limit}&apikey={key}"
    places_json = requests.get(places_info)
    places = places_json.json()
    # print(places)
    places_dict = {}
    for dic in places:
        print(dic)
        name = dic['name']
        places_dict[name] = ( dic['wikipedia_extracts']['text'], dic['image'] , dic['url'])


    print(places_dict) #returns arr of genre of places in city, using radius in an arr with max len limit


def get_hotels(city):
    get_places(city, 5000, "other_hotels")


get_hotels('Paris')