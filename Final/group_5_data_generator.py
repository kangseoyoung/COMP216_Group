"""
Centennial College COMP216 Final Project
Publisher - Value generation
@author: Group 5
"""
import random

# this class generates indoor temperaute with a fluctuation
class sample_set:
    def __init__(self, base_temperature: int = None) -> None:
        self.base_temperature = base_temperature or random.randint(18, 22)
        self._data: float = 0

    # public property
    @property
    def data(self) -> float:
        self._data: float = self._get_random()
        return self.base_temperature + (self._data * 8) # make the random value bigger

    random_dict = {
        'value': random.randint(3, 7)/10, # base random value to be used
        'delta': 0.004,
        'cycle': 0 # each cycle, the 'trend' is decided
        }

    # private method
    def _get_random(self) -> float:
        # make a big flow
        if self.random_dict['cycle'] == 0:
            self.random_dict['cycle'] = random.randint(2, 8)*10
            self.random_dict['delta'] *= -1

        self.random_dict['cycle'] -= 1
        self.random_dict['value'] += self.random_dict['delta']

        # put some fluctuations
        self.random_dict['value'] += random.randint(-30, 30)/1000

        # make the value between 0 and 1
        if (self.random_dict['value'] < 0):
            self.random_dict['delta'] = abs(self.random_dict['delta'])
            self.random_dict['value'] = random.randint(50, 150)/1000

        if (self.random_dict['value'] > 1):
            self.random_dict['delta'] = abs(self.random_dict['delta']) * -1
            self.random_dict['value'] = random.randint(850, 950)/1000
            
        return round(self.random_dict['value'],2)