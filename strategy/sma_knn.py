from strategy.sma import SMA
from strategy.knn import KNN


class SMAKNN(SMA, KNN):
    def __init__(self, status):
        SMA.__init__(self, status)
        KNN.__init__(self, status)

    def calc_indicator(self, timeseries, event):
        self.calc_sma(timeseries, event)
        self.calc_knn(timeseries, event)

    def buy_condition(self, event):
        return self.knn_buy_condition()

    # smaを継承
    # def close_buy_condition(self, event):
    #     return self.sma_close_buy_condition(event)

    def sell_condition(self, event):
        return self.knn_sell_condition()

    # smaを継承    
    # def close_sell_condition(self, event):
    #     return self.sma_close_sell_condition(event)
