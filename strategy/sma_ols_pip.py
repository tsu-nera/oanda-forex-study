from strategy.sma import SMA
from strategy.ols import OLS
from strategy.pip import PIP
from strategy.time import Time
from strategy.rsi import RSI

class SMAOLSPIP(SMA, OLS, PIP, Time, RSI):
    def __init__(self, status):
        SMA.__init__(self, status)
        OLS.__init__(self, status)
        PIP.__init__(self, status)

        self.mean_for_ols_period = 25
        self.ols_period = 25

    def calc_indicator(self, timeseries, event):
        self.calc_sma(timeseries, event)
        self.calc_ols(timeseries, event)
        self.calc_pip_over_closs(timeseries, event)
        self.calc_pip_mean(timeseries, event)
        self.calc_rsi(timeseries, event)

    def buy_condition(self):
        return self.sma_buy_condition() \
            and self.is_up()
            #           and self.b > 0 \

    def close_buy_condition(self, event):
        return self.pip_close_condition(event) \
            or self.pip_over_cross_condiiton(event) \
            or self.pip_loss_cut_condition(event) \
            or self.ols_close_buy_condition(event) \
            and not self.time_guard_condition(event)            

    def sell_condition(self):
        return self.sma_sell_condition() \
            and not self.is_up()
            #            and self.b < 0 \

    def close_sell_condition(self, event):
        return self.pip_close_condition(event) \
            or self.pip_over_cross_condiiton(event) \
            or self.pip_loss_cut_condition(event) \
            or self.ols_close_sell_condition(event) \
            and not self.time_guard_condition(event)
