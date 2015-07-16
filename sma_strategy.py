import pandas as pd
from event import SignalEvent
from datetime import datetime


class SMAStrategy:
    def __init__(self, events, status):

        self.instrument = "EUR_USD"
        self.qty = 1000
        self.resample_interval = '15s'

        self.mean_period_short = 5
        self.mean_period_long = 20
        self.buy_threshold = 1.0
        self.sell_threshold = 1.0

        self.prices = pd.DataFrame()
        self.beta = 0
        self.opening_price = 0
        self.executed_price = 0
        self.unrealized_pnl = 0
        self.realized_pnl = 0
        self.position = 0

        self.events = events
        self.status = status

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

        self.print_tick_data(event, round(self.beta, 5))

        return self.perform_trade_logic(self.beta)

        # self.calculate_unrealized_pnl(event.bid, event.ask)
        # self.print_status()

    def perform_trade_logic(self, beta):
        if beta > self.buy_threshold:
            if not self.status["open_position"] \
                    or self.position < 0:
                signal = SignalEvent(self.instrument, "market", "buy")
                self.events.put(signal)
                return True

        elif beta < self.sell_threshold:
            if not self.status["open_position"] \
                    or self.position > 0:
                signal = SignalEvent(self.instrument, "market", "sell")
                self.events.put(signal)
                return True

        return False

    def print_tick_data(self, event, info):
        print("[%s] %s bid=%s, ask=%s, info=%s" % (
            datetime.now().time(),
            event.instrument,
            event.bid,
            event.ask,
            info))

    def print_status(self):
        print("[%s] %s pos=%s beta=%s RPnL=%s UPnL=%s" % (
            datetime.now().time(),
            self.instrument,
            self.position,
            round(self.beta, 5),
            self.realized_pnl,
            self.unrealized_pnl))
