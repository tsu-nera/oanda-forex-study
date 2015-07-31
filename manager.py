from event import SignalEvent

class Manager():
    def __init__(self, status, events,
                 execution, portfolio, strategy, timeseries):
        self.events = events
        self.status = status
        self.execution = execution
        self.portfolio = portfolio
        self.ts = timeseries
        self.strategy = strategy
        self.status["close_time"] = 0

    def perform_trade(self, event):
        # 時系列データに追加
        self.ts.add_tick_event(event)

        # ストラテジチェック
        self.strategy.calc_indicator(self.ts, event)

        # ストラテジ判定
        self.check_condition(event, self.strategy)

    def check_condition(self, event, strategy):
        if not self.status["open_position"]:
            if strategy.buy_condition(event):
                self.order_and_calc_portfolio(event, True, False)

            elif strategy.sell_condition(event):
                self.order_and_calc_portfolio(event, False, False)

        else:
            if self.status["position"] < 0:
                if strategy.close_sell_condition(event):
                    self.order_and_calc_portfolio(event, True, True)
            else:
                if strategy.close_buy_condition(event):
                    self.order_and_calc_portfolio(event, False, True)

    def order_and_calc_portfolio(self, event, is_buy, is_close):
        if is_buy:
            signal = SignalEvent(event.instrument, event.time,
                                 "market", "buy", event.bid)
            if self.status["is_sim"] and not is_close:
                self.ts.add_buy_event(event)
        else:
            signal = SignalEvent(event.instrument, event.time,
                                 "market", "sell", event.ask)
            if self.status["is_sim"] and not is_close:
                self.ts.add_sell_event(event)

        self.execution.execute_order(signal)     # 売り買いの実行
        self.portfolio.update_portfolio(signal)  # ポートフォリオ更新

        if self.status["is_sim"] and is_close:
            if self.portfolio.is_win():
                self.ts.add_close_win_event(event)
            else:
                self.ts.add_close_lose_event(event)
