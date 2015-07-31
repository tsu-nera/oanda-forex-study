from strategy.sma import SMA
from strategy.pip import PIP
from strategy.bol import BOL
from strategy.rsi import RSI
from strategy.time import Time


class SMABOLPIPRSI(SMA, PIP, Time, BOL, RSI):
    def __init__(self, status):
        SMA.__init__(self, status)
        PIP.__init__(self, status)
        BOL.__init__(self, status)
        Time.__init__(self, status)
        RSI.__init__(self, status)

    def calc_indicator(self, timeseries, event):
        self.calc_sma(timeseries, event)
        self.calc_pip_over_closs(timeseries, event)
        self.calc_pip_mean(timeseries, event)
        self.calc_bol(timeseries, event)
        self.calc_rsi(timeseries, event)        

    def buy_condition(self, event):
        return (self.sma_buy_condition() and self.rsi_is_up()) \
            or (self.bol_buy_condition() and self.rsi > 60) \
            and not self.time_close_guard_condition(event)

    def close_buy_condition(self, event):
        return self.pip_expand_close_condition(event) \
            or self.pip_loss_cut_condition(event) \
            or self.pip_over_cross_condiiton(event) \
            and not self.time_guard_condition(event) 

    def sell_condition(self, event):
        return (self.sma_sell_condition() and not self.rsi_is_up()) \
            or (self.bol_sell_condition() and self.rsi < 40) \
            and not self.time_close_guard_condition(event)
    
    def close_sell_condition(self, event):
        return self.pip_expand_close_condition(event) \
            or self.pip_loss_cut_condition(event) \
            or self.pip_over_cross_condiiton(event) \
            and not self.time_guard_condition(event)
