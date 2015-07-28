from strategy.sma import SMA


class SMAPIP(SMA):
    def __init__(self, status):
        super(SMAPIP, self).__init__(status)

    def calc_indicator(self, timeseries, event):
        self.calc_sma(timeseries, event)

    def buy_condition(self):
        return self.sma_buy_condition()

    def close_buy_condition(self, event):
        return abs(self.status["opening_price"] - event.bid) > 0.0005

    def sell_condition(self):
        return self.sma_sell_condition()

    def close_sell_condition(self, event):
        return abs(self.status["opening_price"] - event.bid) > 0.0005
