import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from currency_widgets import CurrencyRowPool
from exchange_rates import StaticExchangeRates


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Converter")

        widget = CurrencyRowPool(StaticExchangeRates())

        self.setCentralWidget(widget)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
