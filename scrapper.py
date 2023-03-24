import http.client
import os
from seleniumwire import webdriver
import time


def get_api_token():
    options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2,
             "disk-cache-size": 4096}
    options.add_argument("log-level=3")
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--headless")
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(os.getenv("ChromeDriver"), options=options)
    driver.get("https://www.pinnacle.com/")
    time.sleep(5)

    for request in driver.requests:
        if request.response:
            token = request.headers.get("X-API-KEY")
            if token:
                print(token)
                return token

def get_info(item):
    conn.request("GET", item, headers=headers)
    res = conn.getresponse()
    return res.read()

def get_odds(game_id):
     endpoint = f"/0.1/matchups/{game_id}/markets/related/straight"
     data = get_info(endpoint)
     return data.decode("utf-8")

def save_info():
    endpoints = {"live_games" : "/0.1/sports/29/matchups/live?withSpecials=false&brandId=0",
                 "highlighted_games" : "/0.1/sports/29/matchups/highlighted?brandId=0"}
    

    for key, endpoint in endpoints.items():
            print("Pegando info do endpoit: ", endpoint)
            data = get_info(endpoint)
            
            with open(f"{key}.json", "w") as f:
                f.write(data.decode("utf-8"))

token = get_api_token()
conn = http.client.HTTPSConnection("guest.api.arcadia.pinnacle.com")
headers = { 'x-api-key': token }
save_info()