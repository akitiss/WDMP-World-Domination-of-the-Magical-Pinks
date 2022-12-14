import requests
try:
    with open("keys/key_weatherbit.txt") as file:
        key = file.read()
except FileNotFoundError:
    print("No 'key_weatherbit.txt' file found in keys dir")
    key = None

def get_weather(city_name, *country_name): #returns temp of city/country
    if country_name in locals():
        weather_link = f"https://api.weatherbit.io/v2.0/current?&city={city_name}&country={country_name}&key={key}"
    else:
        weather_link = f"https://api.weatherbit.io/v2.0/current?&city={city_name}&&key={key}"
    json_thing = requests.get(weather_link)
    city_dict = json_thing.json()
    # print(city_dict)
    print(city_dict['data'][0]['temp']) #we like degwees Celcius!


get_weather("Athens", "Greece")