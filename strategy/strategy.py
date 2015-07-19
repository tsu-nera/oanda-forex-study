import pandas as pd
from event import SignalEvent


class Strategy:
    def __init__(self, events, status, execution, portfolio):

        self.resample_interval = '60s'

        self.prices = pd.DataFrame()
        self.buys = pd.DataFrame()
        self.sells = pd.DataFrame()

        self.events = events
        self.status = status
        self.execution = execution
        self.portfolio = portfolio

    def resample(self, event):
        self.prices.loc[event.time, event.instrument] = event.bid

        self.resampled_prices = self.prices.resample(
            self.resample_interval,
            how='last',
            fioll_method="ffill")

    def perform_trade_logic(self, event, buy_condition, sell_condition):
        if buy_condition():
            if not self.status["open_position"] \
               or self.status["position"] < 0:
                self.order_and_calc_portfolio(event, True)
                return True

        elif sell_condition():
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
