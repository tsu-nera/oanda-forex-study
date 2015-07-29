from strategy.strategy import Strategy


class RSI(Strategy):
    def __init__(self, status):
        Strategy.__init__(self, status)

        self.rsi = 50
        self.rsi_period = 40

    def calc_indicator(self, timeseries, event):
        self.calc_rsi(timeseries, event)

    def calc_rsi(self, timeseries, event):
        delta = timeseries.get_latest_ts_as_df(
            self.rsi_period).diff()

        if len(delta) < self.rsi_period:
            return

        diff_up, diff_down = delta.copy(), delta.copy()
        diff_up[diff_up < 0] = 0
        diff_down[diff_down > 0] = 0

        rol_up = diff_up.mean()[0]
        rol_down = diff_down.mean().abs()[0]

        rs = rol_up / rol_down
        self.rsi = 100.0 - (100.0 / (1.0 + rs))

    def buy_condition(self):
        return self.rsi > 70

    def close_buy_condition(self):
        return self.rsi < 30

    def sell_condition(self):
        return self.rsi < 30

    def close_sell_condition(self):
        return self.rsi > 70
