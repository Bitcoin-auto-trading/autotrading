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
import json
import requests

url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

# 사용자 토큰
headers = {
    "Authorization": "Bearer _8VIS8eQDVTImFIspnOW2n8T7ue2qKlOJcv3TQo9dZwAAAF9PiGfRA"
}


data = {
    "template_object" : json.dumps({ "object_type" : "text",
                                     "text" : "Lil bapy",
                                     "link" : {
                                                 "web_url" : "www.naver.com"
                                              }
    })
}

response = requests.post(url, headers=headers, data=data)
print(response.status_code)
if response.json().get('result_code') == 0:
    print('메시지를 성공적으로 보냈습니다.')
else:
    print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))

schedule.every(3).hours.do(job)
    
   
def job():
    url = "https://kauth.kakao.com/oauth/token"
    data = {
    "grant_type": "refresh_token",
    "client_id": "9fe6eedbb07dcabc2528454a986e5a8e",
    "refresh_token": "_eR7dCU5CFUylxS65DWE1fbEs9O9tx2K7NvpRwo9dZwAAAF9PiGfQw"
}
    response = requests.post(url, data=data)
    tokens = response.json()

# kakao_code.json 파일 저장
    with open("kakao_code.json", "w") as fp:
        json.dump(tokens, fp)#액세스토큰갱신
