from strategy.strategy import Strategy
import pandas as pd
import statsmodels.api as sm

import numpy as np
# import talib

# OLSよるストラテジ
# http://qiita.com/yubais/items/24f49df99b487fdc374d

class OLS(Strategy):
    def __init__(self, status):
        super(OLS, self).__init__(status)

        self.sma_ols_ts = pd.DataFrame()
        self.mean_for_ols_period = 100
        self.ols_period = 20

        self.a = 0
        self.b = 0
        self.pre_b = 0

    def calc_ols(self, timeseries, event):
        # データをならすために平均をとる.
        mean_for_ols = timeseries.get_latest_ts_as_df(
            self.mean_for_ols_period).mean()[0]
        self.sma_ols_ts.loc[event.time, event.instrument] = mean_for_ols

        x = range(self.ols_period)
        y = np.asarray(
            self.sma_ols_ts.tail(self.ols_period)[event.instrument])

        if len(y) < len(x):
            return

        # いい感じの線分にするために、大きな数をかける
        results = sm.OLS(y * 1000000, sm.add_constant(x), prepend=True).fit()
        self.pre_b = self.b
        self.a, self.b = results.params

        # print(str(self.a) + ", " + str(self.b))

    def ols_buy_condition(self):
        # 傾きがxx以上のときに buyする
        return self.b > 1.5

    def ols_sell_condition(self):
        # 傾きが-xx以上のときにsellする
        return self.b < -1.5
    
    def ols_close_buy_condition(self):
        # 傾きがひっくり返ったときに終了
        return self.pre_b >= 0 and self.b < 0

    def ols_close_sell_condition(self):
        # 傾きがひっくり返ったときに終了
        return self.pre_b <= 0 and self.b > 0

    def cleanup_data(self):
        if len(self.sma_ols_ts) > self.ols_period:
            self.sma_ols_ts.drop(self.sma_ols_ts.head(1).index)
