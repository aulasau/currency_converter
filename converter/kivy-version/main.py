from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from currency_widgets import CurrencyRowPool
from exchange_rates import StaticExchangeRates


class ConverterApp(App):
    def build(self):
        layout = BoxLayout()
        layout.add_widget(CurrencyRowPool(StaticExchangeRates()))

        return layout

    def on_press_button(self):
        print('You pressed the button!')


if __name__ == '__main__':
    app = ConverterApp()
    app.run()
