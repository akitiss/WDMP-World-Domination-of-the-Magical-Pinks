import requests
api_key = "cPv7RF0CHqprPA8fkKdvGG0xgAG8CDdh"
secret_key = "TkhorZu5bprkv7Vd"

def get_token(): # returns the token used in requests. Should be called before every request.
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    header = {"Content-Type": "application/x-www-form-urlencoded"}
    body = {
        "grant_type": "client_credentials",
        "client_id": api_key,
        "client_secret": secret_key,
    }
    json_file = requests.post(url, headers=header, data=body).json()
    return json_file["access_token"]

def get_flight_data(origin, destination, date, number_of_passengers): # date is in yyyy-mm-dd
    base_url = "https://test.api.amadeus.com/v2/shopping/flight-offers?"
    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": date,
        "adults": number_of_passengers,
    }
    url = base_url + construct_url(params)
    token = get_token()
    header = {"Authorization" : "Bearer " + token}
    data = requests.get(url, headers=header).json()
    return data # ------unparsed data------

def construct_url(dict): # turns dict key=value pairs into parameters to pass thru the url of the request
    params = ""
    for x in dict:
        url_part = x + "=" + dict[x] + "&"
        params = params + url_part
    return params[:-1]
print(get_flight_data("SYD", "BOS", "2022-12-11", "2"))