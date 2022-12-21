import requests
# API KEY
try:
    with open("keys/key_amadeus.txt") as file:
        api_key = file.read()
except FileNotFoundError:
    print("No 'key_amadeus.txt' file found in keys dir")
    api_key = None
# SECRET KEY
try:
    with open("keys/key_amadeus_secret.txt") as file:
        secret_key = file.read()
except FileNotFoundError:
    print("No 'key_amadeus_secret.txt' file found in keys dir")
    secret_key = None
    
def get_token(): # returns the token used in requests. Should be called before every request.
    if( api_key == None):
        print("ERROR: api_key is not set")
        return ""
    if( secret_key == None):
        print("ERROR: secret_key is not set")
        return ""
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    header = {"Content-Type": "application/x-www-form-urlencoded"}
    body = {
        "grant_type": "client_credentials",
        "client_id": api_key,
        "client_secret": secret_key,
    }
    request = requests.post(url, headers=header, data=body)
    if (request.status_code != 200):
        print("ERROR on token call: status code != 200")
        return None
    json_file = request.json()
    return json_file["access_token"]

def get_city(keyword):
    base_url = "https://test.api.amadeus.com/v1/reference-data/locations?"
    params = {
        "subType": "CITY",
        "keyword": keyword,
    }
    url = base_url + construct_url(params)
    token = get_token()
    header = {"Authorization" : "Bearer " + token}
    request = requests.get(url, headers=header)
    if (request.status_code != 200):
        print("ERROR on getting flight data: status code != 200")
        return None
    data = request.json()
    return data["data"] # ------unparsed data------

def get_cities_dict(keyword): # RETURNS a dict with {CITY_NAME : IATA_CODE} pairs, the iata code is used to query flight data.
    print("KEYWORD: " + keyword)
    data = get_city(keyword)
    if(data == None): # IF the query fails
        return None
    result = {}
    for x in data:
        result[x["name"]] = x["iataCode"]
    return result

    #origin, destination, date, time(start and end), flight company
def get_flight_data(origin, destination, start_date, end_date, number_of_passengers): # (date is in yyyy-mm-dd) RETURNS None if request fails
    base_url = "https://test.api.amadeus.com/v2/shopping/flight-offers?"
    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": start_date,
        "adults": number_of_passengers,
        "currencyCode": "USD",
        "returnDate": end_date,
        # "nonStop": "true",
        "max": "21"  #      ----------------ONLY GIVES THIS MANY ENTRIES----------------
    }
    url = base_url + construct_url(params)
    token = get_token()
    header = {"Authorization" : "Bearer " + token}
    request = requests.get(url, headers=header)
    if (request.status_code != 200):
        print("ERROR on getting flight data: status code != 200")
        return None
    data = request.json()
    return data # ------unparsed data------

def get_flight_dict(origin, destination, start_date, end_date, number_of_passengers): # Returns None if the query fails. 
    result = []

    get_data = get_flight_data(origin, destination, start_date, end_date, number_of_passengers)
    if( get_data == None ):
        return result
    if (not "data" in get_data):
        print("OOPS No 'data' in the json of flight data call")
        return []
    if (not "dictionaries" in get_data):
        print("OOPS No 'dictionaries' in the json of flight data call")
        return []
    data = get_data["data"]
    codes = get_data["dictionaries"]

    for flight in data:
        # get company:
        company_code = flight["validatingAirlineCodes"][0]
        company = codes["carriers"][company_code]
        # make the dictionary:
        flight_data = {
            "start-time": flight["itineraries"][0]["segments"][0]["departure"]["at"],
            "end-time": flight["itineraries"][1]["segments"][-1]["arrival"]["at"],
            "price": flight["price"]["total"],
            "company": company,
        }
        result.append(flight_data)

    return result 
    # Will return an array of dictionaries. 
    # Each dictionary will have: start-time: "yyyy-mm-dd", end-time: "yyyy-mm-dd", price: "total_price", company: "company",

def construct_url(dict): # turns dict key=value pairs into parameters to pass thru the url of the request
    params = ""
    for x in dict:
        url_part = x + "=" + dict[x] + "&"
        params = params + url_part
    return params[:-1]

#print(get_flight_dict("SYD", "JFK", "2022-12-17", "2022-12-21", "2"))