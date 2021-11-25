import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import webbrowser
import pyupbit
from pyupbit import Upbit
import datetime
from PyQt5.QtCore import QThread, pyqtSignal
from volatility2 import *
import requests
##import json
##import os.path


class VolatilityWorker(QThread):
    tradingSent = pyqtSignal(str, str, str)

    def __init__(self, ticker, upbit):
        super().__init__()
        self.ticker = ticker
        self.upbit = upbit
        self.alive = True

    def run(self):
        now = datetime.datetime.now()
        mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
        ma5 = get_yesterday_ma5(self.ticker)
        target_price = get_target_price(self.ticker)
        wait_flag = False
        print("target price :", target_price)
        while self.alive:
            try:
                now = datetime.datetime.now()
                if mid < now < mid + datetime.delta(seconds=10):
                    target_price = get_target_price(self.ticker)
                    mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
                    ma5 = get_yesterday_ma5(self.ticker)
                    desc = sell_crypto_currency(self.upbit, self.ticker)

                    result = self.upbit.get_order(desc['uuid'])
                    timestamp = result['created_at']
                    dt = datetime.datetime.fromtimestamp( int(int(timestamp)/1000000) )
                    tstring = dt.strftime("%Y/%m/%d %H:%M:%S")
                    self.tradingSent.emit(tstring, "매도", result['data']['order_qty'])
                    wait_flag = False

                if wait_flag == False:
                    current_price = pyupbit.get_current_price(self.ticker)
                    if (current_price > target_price) and (current_price > ma5):
                        desc = buy_crypto_currency(self.upbit, self.ticker)
                        result = self.upbit.get_order(desc['uuid'])
                        timestamp = result['created_at']
                        dt = datetime.datetime.fromtimestamp( int(int(timestamp)/1000000) )
                        tstring = dt.strftime("%Y/%m/%d %H:%M:%S")
                        self.tradingSent.emit(timestamp, "매수", result['volume'])
                        wait_flag = True
            except:
                pass
            time.sleep(1)

    def close(self):
        self.alive = False

class VolatilityWorker2(QThread):
    tradingSent = pyqtSignal(str, str, str)

    def __init__(self, ticker, upbit):
        super().__init__()
        self.ticker = ticker
        self.upbit = upbit
        self.alive = True

    def run(self):
        now = datetime.datetime.now()
        mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
        ma15 = get_ma15(self.ticker)
        target_price = get_target_price(self.ticker)
        wait_flag = False
        print("target price :", target_price)
        while self.alive:
            try:
                now = datetime.datetime.now()
                if mid < now < mid + datetime.delta(seconds=10):
                    target_price = get_target_price(self.ticker)
                    mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
                    ma15 = get_ma15(self.ticker)
                    desc = sell_crypto_currency(self.upbit, self.ticker)

                    result = self.upbit.get_order(desc['uuid'])
                    timestamp = result['created_at']
                    dt = datetime.datetime.fromtimestamp(int(int(timestamp) / 1000000))
                    tstring = dt.strftime("%Y/%m/%d %H:%M:%S")
                    self.tradingSent.emit(tstring, "매도", result['data']['order_qty'])
                    wait_flag = False

                if wait_flag == False:
                    current_price = pyupbit.get_current_price(self.ticker)
                    if (current_price > target_price) and (current_price > ma15):
                        desc = buy_crypto_currency(self.upbit, self.ticker)
                        result = self.upbit.get_order(desc['uuid'])
                        timestamp = result['created_at']
                        dt = datetime.datetime.fromtimestamp(int(int(timestamp) / 1000000))
                        tstring = dt.strftime("%Y/%m/%d %H:%M:%S")
                        self.tradingSent.emit(timestamp, "매수", result['volume'])
                        wait_flag = True
            except:
                pass
            time.sleep(1)

    def close(self):
        self.alive = False

class VolatilityWorker3(QThread):
    tradingSent = pyqtSignal(str, str, str)

    def __init__(self, ticker, upbit):
        super().__init__()
        self.ticker = ticker
        self.upbit = upbit
        self.alive = True

    def run(self):
        now = datetime.datetime.now()
        mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
        ma30 = get_ma30(self.ticker)
        target_price = get_target_price(self.ticker)
        wait_flag = False
        print("target price :", target_price)
        while self.alive:
            try:
                now = datetime.datetime.now()
                if mid < now < mid + datetime.delta(seconds=10):
                    target_price = get_target_price(self.ticker)
                    mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
                    ma30 = get_ma30(self.ticker)
                    desc = sell_crypto_currency(self.upbit, self.ticker)

                    result = self.upbit.get_order(desc['uuid'])
                    timestamp = result['created_at']
                    dt = datetime.datetime.fromtimestamp( int(int(timestamp)/1000000) )
                    tstring = dt.strftime("%Y/%m/%d %H:%M:%S")
                    self.tradingSent.emit(tstring, "매도", result['data']['order_qty'])
                    wait_flag = False

                if wait_flag == False:
                    current_price = pyupbit.get_current_price(self.ticker)
                    if (current_price > target_price) and (current_price > ma30):
                        desc = buy_crypto_currency(self.upbit, self.ticker)
                        result = self.upbit.get_order(desc['uuid'])
                        timestamp = result['created_at']
                        dt = datetime.datetime.fromtimestamp( int(int(timestamp)/1000000) )
                        tstring = dt.strftime("%Y/%m/%d %H:%M:%S")
                        self.tradingSent.emit(timestamp, "매수", result['volume'])
                        wait_flag = True
            except:
                pass
            time.sleep(1)

    def close(self):
        self.alive = False


form_class = uic.loadUiType("resource/main.ui")[0]

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ticker = tick
        self.button.clicked.connect(self.clickBtn)
        self.button2.clicked.connect(self.clickBtn2)
        self.button3.clicked.connect(self.clickBtn3)
        self.button4.clicked.connect(self.clickBtn4)

        self.setWindowTitle("Home Trading System")

        with open("upbit.txt") as f:
            lines = f.readlines()
            apikey = lines[0].strip()
            seckey = lines[1].strip()
            self.apiKey.setText(apikey)
            self.secKey.setText(seckey)

    def clickBtn(self):
        if self.button.text() == "매매시작":
            apiKey = self.apiKey.text()
            secKey = self.secKey.text()
            if len(apiKey) != 40 or len(secKey) != 40:
                self.textEdit.append("KEY가 올바르지 않습니다.")
                return
            else:
                self.upbit = Upbit(apiKey, secKey)
                self.balance = self.upbit.get_balance(self.ticker)
                if self.balance == None:
                    self.textEdit.append("KEY가 올바르지 않습니다.")
                    return
            QMessageBox.information(self, "매매정보", "자동매매1번입니다.")
            self.button.setText("매매중지")
            self.textEdit.append("------ START ------")
            self.textEdit.append("코인 종목 : {}   매매시작 가격 : {}".format(self.ticker,get_target_price(self.ticker)))
            self.textEdit.append("보유 현금 : {} 원".format(self.upbit.get_balance(ticker="KRW")))

            self.vw = VolatilityWorker(self.ticker, self.upbit)
            self.vw.tradingSent.connect(self.receiveTradingSignal)
            self.vw.start()
        else:
            self.vw.close()
            self.textEdit.append("------- END -------")
            self.button.setText("매매시작")

    def clickBtn2(self):
        if self.button2.text() == "매매시작":
            apiKey = self.apiKey.text()
            secKey = self.secKey.text()
            if len(apiKey) != 40 or len(secKey) != 40:
                self.textEdit.append("KEY가 올바르지 않습니다.")
                return

            else:
                self.upbit = Upbit(apiKey, secKey)
                self.balance = self.upbit.get_balance(self.ticker)
                if self.balance == None:
                    self.textEdit.append("KEY가 올바르지 않습니다.")
                    return
                QMessageBox.information(self, "매매정보", "자동매매2번입니다.")
                self.button2.setText("매매중지")
                self.textEdit.append("------ START ------")
                self.textEdit.append("코인 종목 : {}   매매시작 가격 : {}".format(self.ticker,get_target_price(self.ticker)))
                self.textEdit.append("보유 현금 : {} 원".format(self.upbit.get_balance(ticker="KRW")))

                self.vw = VolatilityWorker2(self.ticker, self.upbit)
                self.vw.tradingSent.connect(self.receiveTradingSignal)
                self.vw.start()
        else:
            self.vw.close()
            self.textEdit.append("------- END -------")
            self.button2.setText("매매시작")

    def clickBtn3(self):
        if self.button3.text() == "매매시작":
            apiKey = self.apiKey.text()
            secKey = self.secKey.text()
            if len(apiKey) != 40 or len(secKey) != 40:
                self.textEdit.append("KEY가 올바르지 않습니다.")
                return

            else:
                self.upbit = Upbit(apiKey, secKey)
                self.balance = self.upbit.get_balance(self.ticker)
                if self.balance == None:
                    self.textEdit.append("KEY가 올바르지 않습니다.")
                    return
                QMessageBox.information(self, "매매정보", "자동매매3번입니다.")
                self.button3.setText("매매중지")
                self.textEdit.append("------ START ------")
                self.textEdit.append("코인 종목 : {}   매매시작 가격 : {}".format(self.ticker,get_target_price(self.ticker)))
                self.textEdit.append("보유 현금 : {} 원".format(self.upbit.get_balance(ticker="KRW")))

                self.vw = VolatilityWorker3(self.ticker, self.upbit)
                self.vw.tradingSent.connect(self.receiveTradingSignal)
                self.vw.start()
        else:
            self.vw.close()
            self.textEdit.append("------- END -------")
            self.button3.setText("매매시작")

    def clickBtn4(self):

        tickerKey = self.tickerKey.text()
        change_ticker(tickerKey)
        self.ticker = change_ticker(tickerKey)
        QMessageBox.information(self, "코인정보", "코인이 {}로 바뀌었습니다.".format(self.ticker))

    def receiveTradingSignal(self, time, type, amount):
        self.textEdit.append(f"[{time}] {type} : {amount}")

    # ----------------- 추 가 ------------------
    def closeEvent(self, event):
        self.vw.close()
        self.widget.closeEvent(event)
        self.widget_2.closeEvent(event)
        self.widget_3.closeEvent(event)
    # ------------------------------------------



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    exit(app.exec_())
