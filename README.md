# Trippin by WDMP-World-Domination-of-the-Magical-Pinks
April Li, Aahan Mehta, Joshua Liu, Yuki Feng

## Roles
- April Li: HTML/Bootstrap
- Aahan Mehta: Flask/API
- Joshua Liu: Flask/API/data
- Yuki Feng: HTML/Bootstrap

## About Trippin
Based on user selection, app will help plan a trip. User gets to select a multitude of inputs ranging from location to what type of activities they want to do. After selecting those inputs, the app will automatically select various activities for user to do on each day. User is free to edit the activites as they please after. After the trip is completed, trip will be saved in user database where user is free to edit and view.  

## API and their cards
- [Weather API](https://github.com/stuy-softdev/notes-and-code/blob/main/api_kb/411_on_weatherbit.md)
- [Amadeus](https://github.com/stuy-softdev/notes-and-code/blob/main/api_kb/411_on_Amadeus.md)
- [OpenTripMap](https://github.com/stuy-softdev/notes-and-code/blob/main/api_kb/411_on_OpenTripMap.md)
- [Embed Maps](https://github.com/stuy-softdev/notes-and-code/blob/main/api_kb/411_on_Maps-Embed.md)

### API Keys:     
- Sign Up for these apis here to get your keys:  
[WeatherBit](https://www.weatherbit.io/account/create) [OpenTripMap](https://opentripmap.io/docs) [Amadeus](https://developers.amadeus.com/register) [Google Maps](https://console.cloud.google.com/google/maps-apis/overview?project=reliable-proton-370822)
- For Google Maps API you will need to provide some billing info, but the API we are using from their platform is free so there should not be any costs.
  - You will have to create a 'project' on google maps and amadeus to generate a key. In the google maps project you can specify which apis you want to restrict the project to by going to [credentials](https://console.cloud.google.com/apis/credentials?) and clicking on the actions>edit api key>restrict key to maps embed api.
- Keys should be placed in these places with no extra lines:  
app/keys/key_amadeus_secret.txt
app/keys/key_amadeus.txt
app/keys/key_google_maps.txt
app/keys/key_opentripmap.txt
app/keys/key_weatherbit.txt

## Launch Codes
#### 1) Clone the project
```
git clone git@github.com:akitiss/WDMP-World-Domination-of-the-Magical-Pinks.git
```

#### 2) Navigate to root directory
``` 
cd WDMP-World-Domination-of-the-Magical-Pinks/app
```

#### 3) Create the virtual environment
```
python3 -m venv venv
```

#### 4) Activate the virtual environment
```
. venv/bin/activate
```

#### 5) Install requirements
```
pip install -r requirements.txt
```

#### 6) Run the program

``` 
python3 __init__.py
```

#### 7) Open the following link in any web browser
```
http://127.0.0.1:5000
```
