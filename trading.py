import queue
import threading
import time

from execution import OANDAExecutionHandler
from settings import ACCESS_TOKEN, ACCOUNT_ID
from streaming import StreamingForexPrices

# from parser import HistoricCSVPriceHandler
from sma_strategy import SMAStrategy
from portfolio import Portfolio

heartbeat = 0.5


def on_tick(event_queue, strategies, execution, portfolio):

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

        time.sleep(heartbeat)

if __name__ == "__main__":
    events = queue.Queue()  # 同期キュー

    prices = StreamingForexPrices(environment="practice",
                                  access_token=ACCESS_TOKEN)
#    prices = HistoricCSVPriceHandler("EUR_USD", events, "")

    status = dict()  # tick をまたいで記憶しておきたい情報

    # 戦略
    strategies = set([SMAStrategy(events, status)])

    portfolio = Portfolio(status)  # お金管理

    execution = OANDAExecutionHandler(status)  # 売買注文

    trade_thread = threading.Thread(target=on_tick,
                                    args=[events, strategies,
                                          execution, portfolio])

#    price_thread = threading.Thread(target=prices.stream_to_queue, args=[])
    price_thread = threading.Thread(target=prices.begin, args=[
        ACCOUNT_ID, "EUR_USD", events
    ])

    trade_thread.start()
    price_thread.start()
