import requests
try:
    with open("keys/key_weatherbit.txt") as file:
        key = file.read()
except FileNotFoundError:
    print("No 'key_weatherbit.txt' file found in keys dir")
    key = None

def get_weather(city_name, *country_name): #returns temp of city/country
    if country_name in locals():
        weather_link = f"https://api.weatherbit.io/v2.0/forecast/daily?&city={city_name}&country={country_name}&key={key}"
    else:
        weather_link = f"https://api.weatherbit.io/v2.0/forecast/daily?&city={city_name}&&key={key}"
    json_thing = requests.get(weather_link)
    city_dict = json_thing.json()
    # print(city_dict)
    result = []
    index = 0
    while(index < len(city_dict['data'])):
        flight_data = {
            "temp": city_dict['data'][index]['temp'],
            "max_temp": city_dict['data'][index]['max_temp'],
            "min_temp": city_dict['data'][index]['min_temp'],
            "description": city_dict['data'][index]['weather']['description'],
            "wind_spd": city_dict['data'][index]['wind_spd'],
            "precip": city_dict['data'][index]['precip'],
        }
        date = city_dict['data'][index]['datetime']
        result.append({date: flight_data})
        index += 1
    return result

#print(get_weather("Athens", "Greece"))