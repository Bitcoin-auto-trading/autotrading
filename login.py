import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
import webbrowser
import pyupbit
from vol import *
import datetime
import time

# thread 정의
class VolatilityWorker(QThread):
    tradingSent = pyqtSignal(str, str, str)

    def __init__(self, ticker, upbit):
        super().__init__()
        self.ticker = ticker
        self.upbit = upbit
        self.alive = True

    def run(self):
        # 현재시간
        now = datetime.datetime.now()
        # 다음날 오전 9시
        mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
        ma5 = get_yesterday_ma5(self.ticker)
        target_price = get_target_price(self.ticker)
        wait_flag = False

        while self.alive:
            try:
                now = datetime.datetime.now()
                # 다음날 오전 9시가 되면 target_price, 다음날 9시와 이동평균을 갱신하고 가진을 코인을 전부 시장가 매도
                if mid < now < mid + datetime.delta(seconds=10):
                    target_price = get_target_price(self.ticker)
                    mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
                    ma5 = get_yesterday_ma5(self.ticker)
                    desc  = sell_crypto_currency(self.upbit, self.ticker)

                    result = self.upbit.get_order(desc['uuid'])
                    timestamp = result['created_at']
                    self.tradingSent.emit(timestamp, "매도", result['volume'])
                    wait_flag = False

                if wait_flag == False:
                    current_price = pyupbit.get_current_price(self.ticker)

                    # 목표가격이 현재가보다 크고 이동평균이 현재가보다 작으면
                    if (current_price > target_price) and (current_price > ma5):
                        # 시장가 매수
                        desc = buy_crypto_currency(self.upbit, self.ticker)
                        result = self.upbit.get_order(desc['uuid'])
                        timestamp = result['created_at']
                        self.tradingSent.emit(timestamp, "매수", result['volume'])
                        wait_flag = True
            except: pass

            time.sleep(1)


    def close(self):
        self.alive = False


class MainWidget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 로그인 창
        self.ui = uic.loadUi("source/login.ui", self)
        self.ui.show()
    
    def slot_linked_browser(self):
        url = "https://upbit.com/service_center/open_api_guide"
        webbrowser.open_new(url)

    # # 종료 이벤트(메시지)
    # def closeEvent(self, event):
    #     reply = QMessageBox.question(self, '종료 확인', '종료하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    #     if reply == QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()

    def slot_window_change(self):
        access = self.ui.lineEdit.text()
        secret = self.ui.lineEdit_2.text()

        with open('api.txt', 'w') as f:
            f.write(access)
            f.write("\n"+ secret)

        upbit = pyupbit.Upbit(access,secret)
        mybtc = upbit.get_balances("KRW-ETH")
        # print(type(mybtc[0]))

        # 연결 성공시 로그인창 닫고 메인창 열기
        if  type(mybtc[0]) is list:
            QMessageBox.information(self, "연결 확인", "연결 성공!")
            self.ui.close()
            self.ui = uic.loadUi("source/new_main2.ui", self)
            self.ui.show()

        # 연결 실패시 실패 메시지 출력
        elif type(mybtc[0]) is dict :
            QMessageBox.information(self, "연결 확인", "연결 실패!")
        

    def slot_clickStart(self):
        f = open("api.txt")
        lines = f.readlines() # 모든 라인 읽어오기
        access = lines[0].strip()
        secret = lines[1].strip()
        f.close()
        
        self.upbit = pyupbit.Upbit(access, secret)
        self.ticker = "KRW-ETH"
        start_now = datetime.datetime.now()
        start_now = start_now.strftime("%Y/%m/%d %H:%M:%S")
        self.textEdit.append(f"{start_now} 자동매매를 시작합니다.")
        self.vw = VolatilityWorker(self.ticker, self.upbit)
        self.vw.tradingSent.connect(self.slot_tradingSignal)
        self.vw.start()

    def slot_clickStop(self):
        self.vw.close()
        stop_now = datetime.datetime.now()
        stop_now = stop_now.strftime("%Y/%m/%d %H:%M:%S")
        self.textEdit.append(f"{stop_now} 자동매매를 종료합니다.")
    
    def slot_tradingSignal(self, time, type, amount):
        self.textEdit.append(f"[{time}] {type} : {amount}")

    # def closeEvent(self, event):
    #     self.close()

if __name__ == "__main__":
    # 프로그램 실행 코드
    app = QApplication(sys.argv)
    ow = MainWidget()
    sys.exit(app.exec_())
