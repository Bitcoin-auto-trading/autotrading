# 업비트 암호화폐 자동매매
### upbit 거래소에서 암호화폐 자동매매 HTS

### python ver 3.9

### 파일 구성
- main.py : HTS실행
- mybalances.py : 거래한 암호화폐와 원화의 잔고를 표시
- chart.py : 지정한 암호화폐의 호가를 틱단위로 표시
- orderbook.py : 암호화폐의 호가창을 표시
- overview.py : 암호화폐의 OHLCV(시가, 고가, 저가, 종가, 거래량)를 표시
- volatility2.py : 변동성에 따른 매매전략
- kakao_code.json : 매매시 카카오톡 알림을 위한 json 파일
- requirements.txt : 파일 실행시 필요한 패키지 목록 
  
  
### 설치 및 사용 방법
- $ pip install -r requirements.txt 
- 업비트에서 발급받은 Open API의 Access Key와 Secret Key를 
  upbit.txt의 첫번째 줄과 두번째 줄에 각각 입력.
  https://www.upbit.com/service_center/open_api_guide
  ![image](https://user-images.githubusercontent.com/81648520/143369200-3f690315-f828-474b-96bb-c995ecdbe2c1.png)



- main.py를 통해 HTS실행
 ![KakaoTalk_20211125_105622378](https://user-images.githubusercontent.com/81648520/143364750-f29bd9a2-0194-4c66-b36e-43e2b180ee7e.png)
- 원하는 매매 기법과 암호화폐를 선택하여 매매

