from strategy.pip import PIP
from strategy.bol import BOL
from strategy.rsi import RSI
from strategy.time import Time


class BOLPIPRSI(PIP, Time, BOL, RSI):
    def __init__(self, status):
        PIP.__init__(self, status)
        BOL.__init__(self, status)
        Time.__init__(self, status)
        RSI.__init__(self, status)

        self.bol_mean_period = 20
        self.rsi_period = 40

    def calc_indicator(self, timeseries, event):
        self.calc_pip_mean(timeseries, event)
        self.calc_bol(timeseries, event)
        self.calc_rsi(timeseries, event)        

    def buy_condition(self):
        return  (self.bol_buy_condition() and self.rsi > 60)

    def close_buy_condition(self, event):
        return self.pip_expand_close_condition(event) \
            or self.pip_loss_cut_condition(event) \
            and not self.time_guard_condition(event)

    def sell_condition(self):
        return (self.bol_sell_condition() and self.rsi < 40)
    
    def close_sell_condition(self, event):
        return self.pip_expand_close_condition(event) \
            or self.pip_loss_cut_condition(event) \
            and not self.time_guard_condition(event)
