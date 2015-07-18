import pandas as pd
from event import SignalEvent


class SMAStrategy:
    def __init__(self, events, status, execution, portfolio):

        self.resample_interval = '15s'

        self.mean_period_short = 5
        self.mean_period_long = 20
        self.buy_threshold = 1.0
        self.sell_threshold = 1.0

        self.prices = pd.DataFrame()
        self.buys = pd.DataFrame()
        self.sells = pd.DataFrame()

        self.beta = 0
        self.opening_price = 0
        self.executed_price = 0
        self.unrealized_pnl = 0
        self.realized_pnl = 0
        self.position = 0

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

        mean_short = resampled_prices.tail(
            self.mean_period_short).mean()[0]
        mean_long = resampled_prices.tail(
            self.mean_period_long).mean()[0]
        self.beta = mean_short / mean_long

#        self.portfolio.show_current_status(event)

        return self.perform_trade_logic(event)

    def perform_trade_logic(self, event):
        if self.beta > self.buy_threshold:
            if not self.status["open_position"] \
               or self.status["position"] < 0:
                self.order_and_calc_portfolio(event, True)
                return True

        elif self.beta < self.sell_threshold:
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

        self.execution.execute_order(signal)  # 売り買いの実行
        self.portfolio.update_portfolio(signal)  # ポートフォリオ更新
