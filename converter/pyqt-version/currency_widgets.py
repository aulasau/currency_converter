from functools import partial

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, \
    QWidget, QLineEdit

from exchange_rates import ExchangeRates


class CurrencyRowPool(QWidget):

    def __init__(self, exchange_rates: ExchangeRates):
        super().__init__()
        self.curr_rates = exchange_rates.get_courses()
        self.rows = self.get_text_widgets_per_each_currency()

        layout = QVBoxLayout()
        for row in self.rows:
            row.curr_text.textEdited.connect(partial(self.price_changed, selected_row=row))
            layout.addWidget(row)

        self.setLayout(layout)

    def get_text_widgets_per_each_currency(self):
        widgets = [CurrencyRow(curr, rate) for curr, rate in self.curr_rates.items()]
        return widgets

    def price_changed(self, s: str, selected_row: "CurrencyRow"):
        new_price = s.replace(',', '.')
        try:
            new_price_float = float(new_price)
        except ValueError:
            print('Price value is not digital')
            return

        usd_price = selected_row.curr_text.exchange_rate * new_price_float

        for row in self.rows:
            if row != selected_row:
                row.recalculate_price(usd_price)
        print('Price changed')


class CurrencyRow(QWidget):
    def __init__(self, curr_name: str, exchange_rate: float):
        super().__init__()

        self.curr_text = CurrencyPriceLineText(curr_name, exchange_rate)

        self.curr_label = QLabel(curr_name)

        layout = QHBoxLayout()
        layout.addWidget(self.curr_text)
        layout.addWidget(self.curr_label)

        self.setLayout(layout)

    def recalculate_price(self, new_usd_price):
        self.curr_text.recalculate_price(new_usd_price)


class CurrencyPriceLineText(QLineEdit):
    def __init__(self, curr_name: str, exchange_rate: float):
        super().__init__()
        self.curr_name = curr_name
        self.exchange_rate = exchange_rate
        self.setPlaceholderText(f'Insert price in {curr_name}')

    def recalculate_price(self, usd_price):
        new_price = usd_price / self.exchange_rate
        self.setText(f'{new_price:.2f}')

    def mousePressEvent(self, a0) -> None:
        self.selectAll()
