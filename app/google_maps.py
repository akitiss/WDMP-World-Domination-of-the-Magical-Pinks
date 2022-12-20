import requests

try:
    with open("keys/key_google_maps.txt") as file:
        key = file.read()
except FileNotFoundError:
    print("No 'key_opentripmap.txt' file found in keys dir")
    key = None

def get_img_link(lat, lon):
    return f"https://www.google.com/maps/embed/v1/place?key={key}&q={lat},{lon}"
    
print(get_img_link(37.98805618286133,23.738889694213867))

'''
<iframe

  src="get_img_link(lat,lon)"
  allowfullscreen>
</iframe>'''