from strategy.time import Time
from strategy.ols import OLS


class OLSTIME(Time, OLS):
    def __init__(self, status):
        Time.__init__(self, status)
        OLS.__init__(self, status)

        # 60秒間ガード
        self.guard_time = 60

    def calc_indicator(self, timeseries, event):
        self.calc_ols(timeseries, event)

    def buy_condition(self, event):
        return self.ols_buy_condition()

    def sell_condition(self, event):
        return self.ols_sell_condition() 

    def close_buy_condition(self, event):
        return self.ols_close_buy_condition() \
            and not self.time_guard_condition(event)

    def close_sell_condition(self, event):
        return self.ols_close_sell_condition() \
            and not self.time_guard_condition(event)
