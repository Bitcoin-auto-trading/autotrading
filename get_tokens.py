import schedule
import requests
import json

url = "https://kauth.kakao.com/oauth/token"

data = {
    "grant_type" : "authorization_code",
    "client_id" : "9fe6eedbb07dcabc2528454a986e5a8e",
    "redirect_url" : "https://localhost:3000",
    "code" : "hpQ6hu5tQ9vIFKaJ4QdJpwcRarGM7eFOaYMGJazUjnrZ2ya1xSDioJlBgdkdOK6HgtRxlAo9dVoAAAF9Phbmdg"
}

response = requests.post(url, data=data)

tokens = response.json()
print(tokens)

with open("kakao_token.json", "w") as fp:
    json.dump(tokens, fp)
