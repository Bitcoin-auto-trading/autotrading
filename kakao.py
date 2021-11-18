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
if __name__ == "__main__":
    import pyupbit

    access_key = "Uc7gjRjwxKWtqi3CzE8eBa0GBxKEuvxstqy4VBux"
    secret_key = "BuXKRKaxcPdhL8Htpl1cGsVbqGh0zd10DHVLLxWB"
    upbit = pyupbit.Upbit(access_key, secret_key)

    kakao = Kakao()
    ticker = 'krw-btc'

    orderbook = pyupbit.get_orderbook(ticker)
    bids_asks = orderbook[0]['orderbook_units']
    bid_price = bids_asks[0]['bid_price']

    sellprice = bid_price
    balance = round(float(upbit.get_balances()[0]['balance']), 2)
    ror = 0.98999948
    message = f'{ticker}를 {sellprice}에 \n전량매도 했습니다.\n\n매도 체결 후 잔액:\n{balance}원\n\n현재 수익률: {round((ror-1)*100, 2)}%'
    kakao.send_message2me(message)
