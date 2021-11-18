import json
import requests


class Kakao:
    def __init__(self):
        with open("kakao_code.json", "r") as fp:
            tokens = json.load(fp)

        auth_url = "https://kauth.kakao.com/oauth/token"
        data = {
            "grant_type": "refresh_token",
            "client_id": "6bea89b579e0495940a0b8989903b22f",
            "refresh_token": tokens["refresh_token"]
        }
        response = requests.post(auth_url, data=data)
        tokens = response.json()

        url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

        headers = {
            "Authorization": "Bearer " + tokens['access_token']
        }

        self.url = url
        self.headers = headers


    def send_message2me(self, message):
        data = {
            "template_object": json.dumps({
                "object_type": "text",
                "text": message,
                "link": {
                    "web_url": "www.naver.com"
                }
            })
        }

        requests.post(self.url, headers=self.headers, data=data)
