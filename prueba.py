import requests
r = requests.get("https://api.bluelytics.com.ar/v2/evolution.json?days=10")
print(r.json()[0])