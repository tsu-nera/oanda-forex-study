import time


class Main():
    def __init__(self, heartbeat):
        self.heartbeat = heartbeat

    def on_tick(self, event_queue, strategies, execution, portfolio):

        while True:
            while not event_queue.empty():
                event = event_queue.get(False)

                if event.type == 'TICK':
                    # 未決済ポジションの計算
                    portfolio.calculate_unrealized_pnl(event)

                    # ストラテジチェック
                    for strategy in strategies:
                        if(strategy.check(event)):
                            break
                elif event.type == 'SIGNAL':
                    print("signal event")
                    # 売り買いの実行
                    execution.execute_order(event)

                    # ポートフォリオ更新
                    portfolio.update_portfolio(event)

            time.sleep(self.heartbeat)
