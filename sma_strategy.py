import pandas as pd
from event import SignalEvent
from datetime import datetime


class SMAStrategy:
    def __init__(self, events, status):

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

        self.print_status(event, self.beta)

        return self.perform_trade_logic(event)

        # self.calculate_unrealized_pnl(event.bid, event.ask)
        # self.print_status()

    def perform_trade_logic(self, event):
        if self.beta > self.buy_threshold:
            if not self.status["open_position"] \
                    or self.position < 0:
                signal = SignalEvent(event.instrument, "market", "buy")
                self.events.put(signal)
                return True

        elif self.beta < self.sell_threshold:
            if not self.status["open_position"] \
                    or self.position > 0:
                signal = SignalEvent(event.instrument, "market", "sell")
                self.events.put(signal)
                return True

        return False

    def print_tick_data(self, event, info):
        print("[%s] %s info=%s" % (
            datetime.now().time(),
            event.instrument,
            event.bid,
            event.ask,
            info))

    def print_status(self, event, info):
        print("[%s] %s pos=%s info=%s RPnL=%s UPnL=%s" % (
            datetime.now().time(),
            event.instrument,
            self.status["position"],
            round(info, 5),
            round(self.status["realized_pnl"], 5),
            round(self.status["unrealized_pnl"], 5)))
