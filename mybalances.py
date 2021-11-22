import sys
import time
import pyupbit
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt, QThread, pyqtSignal
# from pyupbit.quotation_api import get_current_price


class MybalancesWorker(QThread):
    dataSent = pyqtSignal(dict)

    def __init__(self, ticker):
        super().__init__()
        self.ticker = ticker
        self.alive = True

    def run(self):
        while self.alive:
            f = open("api.txt")
            lines = f.readlines()   # 모든 라인 읽어오기
            access = lines[0].strip()  # 0번째 줄 가져오기 strip()메소드를 사용해 '\n'을 없애기.
            secret = lines[1].strip()
            f.close()

            self.upbit = pyupbit.Upbit(access, secret)
            data  = self.upbit.get_balances()
            time.sleep(0.5)
            if data[0] != None:
                self.dataSent.emit(data[0])

    def close(self):
        self.alive = False

#문제점!! 이더리움으로 계산됨 이걸 내 잔고의 전체 티커 받아오기로 바꿔야함..
class MybalancesWidget(QWidget):
    def __init__(self, parent=None):  
        super().__init__(parent)
        uic.loadUi("resource/mybalances.ui", self)
        self.ticker = "KRW-BTC"
        
        for i in range(self.tableBalances.rowCount()):
            item_0 = QTableWidgetItem(str(""))
            item_0.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableBalances.setItem(i, 0, item_0)

            item_1 = QTableWidgetItem(str(""))
            item_1.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableBalances.setItem(i, 1, item_1)

            item_2 = QTableWidgetItem(str(""))
            item_2.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableBalances.setItem(i, 2, item_2)

            item_3 = QTableWidgetItem(str(""))
            item_3.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableBalances.setItem(i, 3, item_3)

            item_4 = QTableWidgetItem(str(""))
            item_4.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableBalances.setItem(i, 4, item_4)

            item_5 = QTableWidgetItem(str(""))
            item_5.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableBalances.setItem(i, 5, item_5)

            item_6 = QTableWidgetItem(str(""))
            item_6.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableBalances.setItem(i, 6, item_6)


        self.ow = MybalancesWorker(self.ticker)
        self.ow.dataSent.connect(self.updateData)
        self.ow.start()

    def updateData(self, data):
        f = open("api.txt")
        lines = f.readlines()   # 모든 라인 읽어오기
        access = lines[0].strip()  # 0번째 줄 가져오기 strip()메소드를 사용해 '\n'을 없애기.
        secret = lines[1].strip()
        f.close()

        self.upbit = pyupbit.Upbit(access, secret)
        balances = self.upbit.get_balances()

        # 업비트가 지원하는 모든 원화마켓 가져오기
        krw_market = pyupbit.get_tickers(fiat="KRW")
        btc_market = pyupbit.get_tickers(fiat="BTC")
        
        for j in range(len(balances)):
            ticker= "KRW-"+balances[j]['currency']
            
            # 지원하는 원화마켓과 다른 티커는 제외(비상장 코인이나 KRW-KRW문제)
            if ticker in krw_market:
                price = pyupbit.get_current_price(ticker)
                for i in range(len(balances)):
                    # 0) 코인명 
                    item_0 = self.tableBalances.item(i, 0)
                    item_0.setText(f"{balances[i]['currency']}")

                    # 1) 보유수량
                    item_1 = self.tableBalances.item(i, 1)
                    amount1 = float(balances[i]['balance']) + float(balances[i]['locked'])
                    item_1.setText(f"{amount1}")
                    
                    if "KRW-"+balances[i]['currency'] not in krw_market : pass
                    else :
                        # 2) 매수평균가
                        item_2 = self.tableBalances.item(i, 2)
                        item_2.setText(f"{balances[i]['avg_buy_price']} 원")

                        # 3) 평가금액
                        amount2 = price * (float(balances[i]['balance'])+float(balances[i]['locked']))  # 현재가 * (주문가능 금액 + 주문 묶여있는 금액)

                        item_3 = self.tableBalances.item(i, 3)
                        item_3.setText(f"{int(amount2)} 원")

                        # 4) 매수금액
                        amount3 = round(float(balances[i]['avg_buy_price']) * (float(balances[i]['balance']) + float(balances[i]['locked']))) # 매수평균가 * (주문가능 금액 + 주문 묶여있는 금액) 반올림
                        item_4 = self.tableBalances.item(i, 4)
                        item_4.setText(f"{str(amount3)} 원")

                        # 5) 평가손익
                        amount4 = round(amount2 - amount3, 2) # 평가금액 - 매수금액 -> 소수 둘째자리까지 반올림
                        item_5 = self.tableBalances.item(i, 5)
                        item_5.setText(f"{amount4}")
                    
                        try :
                            # 수익률
                            amount5 = round(amount4 / amount3 * 100,2) # 평가손익 / 매수금액
                            item_6 = self.tableBalances.item(i, 6)
                            item_6.setText(f"{str(amount5)} %")

                        except: pass

            # else:
            #     price = pyupbit.get_current_price(ticker)
            #     for i in range(len(balances)):
            #         # 0) 코인명
            #         item_0 = self.tableBalances.item(i, 0)
            #         item_0.setText(f"{balances[i]['currency']}")
            #
            #         # 1) 보유수량
            #         item_1 = self.tableBalances.item(i, 1)
            #         amount1 = float(balances[i]['balance']) + float(balances[i]['locked'])
            #         item_1.setText(f"{amount1}")

                    # if "BTC-" + balances[i]['currency'] not in btc_market:
                    #     pass
                    # else:
                    #     # 2) 매수평균가
                    #     item_2 = self.tableBalances.item(i, 2)
                    #     item_2.setText(f"{balances[i]['avg_buy_price']} 원")
                    #
                    #     # 3) 평가금액
                    #     amount2 = price * (float(balances[i]['balance']) + float(
                    #         balances[i]['locked']))  # 현재가 * (주문가능 금액 + 주문 묶여있는 금액)
                    #
                    #     item_3 = self.tableBalances.item(i, 3)
                    #     item_3.setText(f"{int(amount2)} 원")
                    #
                    #     # 4) 매수금액
                    #     amount3 = round(float(balances[i]['avg_buy_price']) * (float(balances[i]['balance']) + float(
                    #         balances[i]['locked'])))  # 매수평균가 * (주문가능 금액 + 주문 묶여있는 금액) 반올림
                    #     item_4 = self.tableBalances.item(i, 4)
                    #     item_4.setText(f"{str(amount3)} 원")
                    #
                    #     # 5) 평가손익
                    #     amount4 = round(amount2 - amount3, 2)  # 평가금액 - 매수금액 -> 소수 둘째자리까지 반올림
                    #     item_5 = self.tableBalances.item(i, 5)
                    #     item_5.setText(f"{amount4}")
                    #
                    #     try:
                    #         # 수익률
                    #         amount5 = round(amount4 / amount3 * 100, 2)  # 평가손익 / 매수금액
                    #         item_6 = self.tableBalances.item(i, 6)
                    #         item_6.setText(f"{str(amount5)} %")
                    #
                    #     except:
                    #         pass




    def closeEvent(self, event):
        self.ow.close()


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ow = MybalancesWidget()
    ow.show()
    exit(app.exec_())