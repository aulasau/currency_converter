from abc import ABC, abstractmethod


class ExchangeRates(ABC):
    """A class for managing exchange rates relative to the dollar."""

    @abstractmethod
    def get_courses(self):
        pass


class StaticExchangeRates(ExchangeRates):
    """Static rates for 21.02.2022"""

    def get_courses(self):
        return {'GEL': 0.34,
                'USD': 1,
                'UAH': 0.035,
                'BYN': 0.39, }
