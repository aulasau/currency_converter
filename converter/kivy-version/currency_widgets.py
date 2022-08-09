from functools import partial

from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from exchange_rates import ExchangeRates


class CurrencyRowPool(BoxLayout):

    def __init__(self, exchange_rates: ExchangeRates, btn_name='Convert'):
        super().__init__(orientation='vertical')
        self.curr_rates = exchange_rates.get_courses()

        self.rows = self.get_text_widgets_per_each_currency()
        for row in self.rows:
            row.curr_text.bind(text=partial(self.price_changed, selected_row=row))
            self.add_widget(row)

        self.last_row_changed = self.rows[0]

        self.button = Button()
        self.button.text = btn_name
        self.button.bind(on_press=self.button_pressed)

        self.add_widget(self.button)

    def get_text_widgets_per_each_currency(self):
        widgets = [CurrencyRowLayout(curr, rate) for curr, rate in self.curr_rates.items()]
        return widgets

    def price_changed(self, text_input_instance: TextInput, text: str, selected_row: "CurrencyRowLayout"):
        # new_price = text.replace(',', '.')
        # try:
        #     new_price_float = float(new_price)
        # except ValueError:
        #     print('Price value is not digital')
        #     return

        # usd_price = selected_row.exchange_rate * new_price_float
        #
        # for row in self.rows:
        #     if row != selected_row:
        #         row.recalculate_price(usd_price)
        self.last_row_changed = selected_row
        print('Price changed')

    def button_pressed(self, button):
        new_price = self.last_row_changed.curr_text.text.replace(',', '.')
        try:
            new_price_float = float(new_price)
        except ValueError:
            print('Price value is not digital')
            return

        usd_price = self.last_row_changed.exchange_rate * new_price_float

        for row in self.rows:
            row.recalculate_price(usd_price)

        print('Button was pressed')


class CurrencyRowLayout(BoxLayout):
    def __init__(self, curr_name: str, exchange_rate: float):
        super().__init__(orientation='horizontal', padding=50)

        self.exchange_rate = exchange_rate
        self.curr_text = SelectInput(multiline=False, readonly=False,
                                     halign="left")
        self.curr_label = Label(text=curr_name)

        self.add_widget(self.curr_text)
        self.add_widget(self.curr_label)

    def recalculate_price(self, new_usd_price):
        new_price = new_usd_price / self.exchange_rate
        self.curr_text.text = f'{new_price:.2f}'


class SelectInput(TextInput):

    def on_focus(self, instance, isFocused):
        if isFocused:
            Clock.schedule_once(lambda dt: self.selected_text())

    def selected_text(self):
        ci = self.cursor_index()
        cc = self.cursor_col
        line = self._lines[self.cursor_row]
        len_line = len(line)
        start = max(0, len(line[:cc]) - line[:cc].rfind(u' ') - 1)
        end = line[cc:].find(u' ')
        end = end if end > - 1 else (len_line - cc)
        Clock.schedule_once(lambda dt: self.select_text(ci - start, ci + end))

# class CurrencyPriceLineText(QLineEdit):
#     def __init__(self, curr_name: str, exchange_rate: float):
#         super().__init__()
#         self.curr_name = curr_name
#         self.exchange_rate = exchange_rate
#         self.setPlaceholderText(f'Insert price in {curr_name}')
#
#     def recalculate_price(self, usd_price):
#         new_price = usd_price / self.exchange_rate
#         self.setText(f'{new_price:.2f}')
#
#     def mousePressEvent(self, a0) -> None:
#         self.selectAll()
