import time


class Main():
    def __init__(self, is_real):
        self.is_real = is_real
        self.heartbeat = 0.5 if is_real else 0

    def on_tick(self, event_queue, strategies, execution, portfolio):

        while True:
            while not event_queue.empty():
                event = event_queue.get(False)

                if event.type == 'TICK':
                    if self.is_real:
                        # 現在のポジションの表示
                        portfolio.show_current_status(event)

                    # ストラテジチェック
                    for strategy in strategies:
                        if(strategy.check(event)):
                            break
                elif event.type == 'SIGNAL':
                    # 売り買いの実行
                    execution.execute_order(event)

                    # ポートフォリオ更新
                    portfolio.update_portfolio(event)

            if not self.is_real:   # シミュレーションの場合は抜ける
                break

            time.sleep(self.heartbeat)
