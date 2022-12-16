import requests
from pprint import pprint
import random
# try:
#     with open("keys/key_pexels.txt") as file:
#         api_key=file.read()
# except FileNotFoundError:
#     print("No 'key_pexels.txt' file found in keys dir")
#     api_key = None


'''
Returns the key in the specified file in string format
'''
def get_key(file_name: str):
    path = f'keys/{file_name}'

    with open(path) as key:
        return key.read().strip('\n')

    
def get_city_img(name): 

    api_url = "https://api.pexels.com/v1/search?"
    file_name = "key_cityimg.txt"

    params = {
        "query":{name},
        "per_page":{1}
    }

    response = requests.get(api_url,params=params,headers={"Authorization":get_key(file_name)})

    # parsing the response
    data = response.json()
    img_url = data['photos'][0]['src']['original']
    site_url = data['photos'][0]['url']
    print("this is the site picture: " + site_url)
    return img_url



def get_rand_city():

    # documentation: http://geodb-cities-api.wirefreethought.com/demo

    api_url = "http://geodb-free-service.wirefreethought.com/v1/geo/cities?"

    params = {
        "minPopulation":1000000,
        "limit":1,
        "offset":random.randint(0,1530)
    }

    response = requests.get(api_url,params=params)
    
    # parsing of response
    data = response.json()
    city_name = data['data'][0]['city']
    country = data['data'][0]['country']
    region = data['data'][0]['region']
    # print({'city':city_name,'country':country,"region":region})

    return {'city':city_name,'country':country,"region":region}





# get_city_img("Lexinton")
resp = get_rand_city()
print("city of " + resp['city'] + " " + resp['region'] + " " + resp['country'])
print (get_city_img("city of " + resp['city'] + " " + resp['country']))