from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from pyupbit import WebSocketManager
from volatility2 import tick

class OverViewWorker(QThread):
    # pyqtSignal = 사용자 정의 시그널(웹소켓에서 메인스레드로 데이터를 전송하기 위함)
    dataSent = pyqtSignal(int, float, int, float, int, int)

    def __init__(self, ticker):
        super().__init__()
        self.ticker = ticker
        self.alive = True

    def run(self):
        wm = WebSocketManager("ticker", [f"{self.ticker}"])
        while self.alive:
            data = wm.get()
            self.dataSent.emit(int  (data['trade_price']),
                                float(data['acc_trade_volume_24h']),
                                int  (data['high_price']),
                                float(data['acc_trade_price_24h']),
                                int  (data['low_price']),
                                int  (data['prev_closing_price']))
        wm.terminate()

    def close(self):
        self.alive = False


class OverviewWidget(QWidget):
    def __init__(self, parent=None, ticker=tick, ):
        super().__init__(parent)
        uic.loadUi("resource/overview.ui", self)

        self.ticker = ticker
        self.ovw = OverViewWorker(ticker)
        self.ovw.dataSent.connect(self.fillData)
        self.ovw.start()

    def closeEvent(self, event):
        self.ovw.close()

    def fillData(self, currPrice, volume, highPrice, value, lowPrice, PrevClosePrice):
        self.label_1.setText(f"{currPrice:,}")
        self.label_4.setText(f"{volume:.4f} {self.ticker}")
        self.label_6.setText(f"{highPrice:,}")
        self.label_8.setText(f"{value/100000000:,.1f} 억")
        self.label_10.setText(f"{lowPrice:,}")
        self.label_14.setText(f"{PrevClosePrice:,}")
        self.__updateStyle()


    def __updateStyle(self):
        if '-' in self.label_2.text():
            self.label_1.setStyleSheet("color:blue;")
            self.label_2.setStyleSheet("background-color:blue;color:white")
        else:
            self.label_1.setStyleSheet("color:red;")
            self.label_2.setStyleSheet("background-color:red;color:white")

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ob = OverviewWidget()
    ob.show()
    exit(app.exec_())
