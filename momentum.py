import pandas as pd
from event import SignalEvent

import numpy as np
# import talib


class Momentum:
    def __init__(self, events, status, execution, portfolio):

        self.resample_interval = '60s'

        self.period_back = 30
        self.momentum = 0

        self.prices = pd.DataFrame()
        self.buys = pd.DataFrame()
        self.sells = pd.DataFrame()

        self.events = events
        self.status = status
        self.execution = execution
        self.portfolio = portfolio

    def check(self, event):
        self.prices.loc[event.time, event.instrument] = event.bid

        # ティックだと多いので、間引く.
        # TODO 抽象クラスへ移動
        resampled_prices = self.prices.resample(
            self.resample_interval,
            how='last',
            fill_method="ffill")

        momentum_seq = np.asarray(resampled_prices.tail(self.period_back))

        if len(momentum_seq) < self.period_back:
            return False

        self.beta = (momentum_seq[self.period_back-1] / momentum_seq[0]) * 100

        return self.perform_trade_logic(event)

    def perform_trade_logic(self, event):
        if self.beta > 100:
            if not self.status["open_position"] \
               or self.status["position"] < 0:
                self.order_and_calc_portfolio(event, True)
                return True

        elif self.beta < 100:
            if not self.status["open_position"] \
               or self.status["position"] > 0:
                self.order_and_calc_portfolio(event, False)
                return True

        return False

    def order_and_calc_portfolio(self, event, is_buy):
        if is_buy:
            signal = SignalEvent(event.instrument, event.time,
                                 "market", "buy", event.bid)
            self.buys.loc[event.time, event.instrument] = event.bid
        else:
            signal = SignalEvent(event.instrument, event.time,
                                 "market", "sell", event.ask)
            self.sells.loc[event.time, event.instrument] = event.ask

        self.execution.execute_order(signal)     # 売り買いの実行
        self.portfolio.update_portfolio(signal)  # ポートフォリオ更新
