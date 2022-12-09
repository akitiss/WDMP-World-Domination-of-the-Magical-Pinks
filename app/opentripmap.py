import requests

'''
can get hotel picture from: https://opentripmap.io/docs#/Objects%20list/getListOfPlacesByRadius gives link smwr
also can get wikipedia link
'''
key = "5ae2e3f221c38a28845f05b6f33412d1f6da84b5fd8eccc6b2a3fb05"

def get_hotels(city):
    city_info = f"https://api.opentripmap.com/0.1/en/places/geoname?name={city}&apikey={key}"
    city_json = requests.get(city_info)
    city_format = city_json.json()
    coords = { 'lon': city_format['lon'], 'lat' : city_format['lat']}

    hotel_info = f"https://api.opentripmap.com/0.1/en/places/radius?radius=2000&lon={coords['lon']}&lat={coords['lat']}&kinds=other_hotels&format=json&limit=20&apikey={key}"
    # https://api.opentripmap.com/0.1/en/places/radius?radius=2000&lon={coords['lon']}&lat={coords['lat']}&kinds=other_hotels&format=json&limit=20&apikey={key}
    hotel_json = requests.get(hotel_info)
    hotels = hotel_json.json()
    hotel_arr = []
    for dict in hotels:
        hotel_arr.append(dict['name'])

    print(hotel_arr)
get_hotels('Marseille')