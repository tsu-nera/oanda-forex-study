from event import SignalEvent
from timeseries import TimeSeries


class Manager():
    def __init__(self, status, events, execution, portfolio, strategy):
        self.events = events
        self.status = status
        self.execution = execution
        self.portfolio = portfolio
        self.ts = TimeSeries()
        self.strategy = strategy

    def perform_trade(self, event):
        # 時系列データに追加
        self.ts.add_tick_event(event)

        # ストラテジチェック
        self.strategy.calc_indicator(self.ts, event)

        # ストラテジ判定
        self.check_condition(event, self.strategy)

    def check_condition(self, event, strategy):
        if strategy.buy_condition():
            if not self.status["open_position"] \
               or self.status["position"] < 0:
                self.order_and_calc_portfolio(event, True)

        elif strategy.sell_condition():
            if not self.status["open_position"] \
               or self.status["position"] > 0:
                self.order_and_calc_portfolio(event, False)

    def order_and_calc_portfolio(self, event, is_buy):
        if is_buy:
            signal = SignalEvent(event.instrument, event.time,
                                 "market", "buy", event.bid)
            self.ts.add_buy_event(event)
        else:
            signal = SignalEvent(event.instrument, event.time,
                                 "market", "sell", event.ask)
            self.ts.add_sell_event(event)

        self.execution.execute_order(signal)     # 売り買いの実行
        self.portfolio.update_portfolio(signal)  # ポートフォリオ更新

