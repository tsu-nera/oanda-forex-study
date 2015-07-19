import queue
import threading
import time

from execution import OANDAExecutionHandler
from settings import ACCESS_TOKEN, ACCOUNT_ID
from streaming import StreamingForexPrices

from sma_strategy import SMAStrategy
from portfolio import PortfolioRemote

heartbeat = 0.5


def on_tick(event_queue, strategies, portfolio):
    while True:
        while not event_queue.empty():
            event = event_queue.get(False)

            # ストラテジチェック
            for strategy in strategies:
                if(strategy.check(event)):
                    break
            portfolio.print_status(event)

        time.sleep(heartbeat)

if __name__ == "__main__":
    events = queue.Queue()  # 同期キュー

    prices = StreamingForexPrices(environment="practice",
                                  access_token=ACCESS_TOKEN)

    status = dict()  # tick をまたいで記憶しておきたい情報

    portfolio = PortfolioRemote(status)  # お金管理

    execution = OANDAExecutionHandler(status)  # 売買注文

    # 戦略
    strategy = SMAStrategy(events, status, execution, portfolio)
    strategies = set([strategy])

    trade_thread = threading.Thread(target=on_tick,
                                    args=[events, strategies, portfolio])

    price_thread = threading.Thread(target=prices.begin, args=[
        ACCOUNT_ID, "EUR_USD", events
    ])

    trade_thread.start()
    price_thread.start()
