# import requests

# url = "https://napi.kotaksecurities.com/oauth2/token"
# payload = {
#     "grant_type": "authorization_code",
#     "client_id": "TfwIXS7YwcTHuD9foRcXUfuPfr0a",
#     "client_secret": "wE2UjQdCJaJf2XwCjfuL9dNTN5wa",
#     "code": "03845ca9-bb52-3009-ab55-eb394c256314", 
#     "redirect_uri": "https://127.0.0.1/"
# }

# res = requests.post(url, data=payload)
# print(res.json())
# print(res.status_code)

# import requests

# url = "https://gw-napi.kotaksecurities.com/Session/1.0/session"
# payload = {
#     "userid": "YWCBT",
#     "password": "Tanay*1patel",
#     "pan": "GXIPP5828L"
#     # "dob": "2004-04-12"
# }
# headers = {"Content-Type": "application/json"}

# response = requests.post(url, json=payload, headers=headers)

# print(response.json())   # this will show sid, Auth, tokens

import requests
import json

url = "https://napi.kotaksecurities.com/Session/1.0/session"

payload = {
    "userid": "YWCBT",
    "password": "Tanay*1patel",
    "pan": "GXIPP5828L"   # or use "dob": "YYYY-MM-DD"
}

headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "x-kotak-client-id": "TfwIXS7YwcTHuD9foRcXUfuPfr0a"

}

res = requests.post(url, data=json.dumps(payload), headers=headers)

print("Status Code:", res.status_code)
print("Response:", res.text)
