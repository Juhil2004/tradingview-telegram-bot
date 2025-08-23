import requests

url = "https://napi.kotaksecurities.com/oauth2/token"
payload = {
    "grant_type": "authorization_code",
    "client_id": "TfwIXS7YwcTHuD9foRcXUfuPfr0a",
    "client_secret": "wE2UjQdCJaJf2XwCjfuL9dNTN5wa",
    "code": "03845ca9-bb52-3009-ab55-eb394c256314", 
    "redirect_uri": "https://127.0.0.1/"
}

res = requests.post(url, data=payload)
print(res.json())
print(res.status_code)