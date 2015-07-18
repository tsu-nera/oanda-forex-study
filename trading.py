import queue
import threading
import time

from execution import OANDAExecutionHandler
from settings import ACCESS_TOKEN, ACCOUNT_ID
from streaming import StreamingForexPrices

from main import Main
from sma_strategy import SMAStrategy
from portfolio import PortfolioRemote

heartbeat = 0.5


def on_tick(self, event_queue, strategies, progress=None):
    while True:
        while not event_queue.empty():
            event = event_queue.get(False)

            # ストラテジチェック
            for strategy in strategies:
                if(strategy.check(event)):
                    break

        time.sleep(heartbeat)

if __name__ == "__main__":
    events = queue.Queue()  # 同期キュー

    prices = StreamingForexPrices(environment="practice",
                                  access_token=ACCESS_TOKEN)

    status = dict()  # tick をまたいで記憶しておきたい情報

    # 戦略
    strategies = set([SMAStrategy(events, status)])

    portfolio = PortfolioRemote(status)  # お金管理

    execution = OANDAExecutionHandler(status)  # 売買注文

    main = Main()

    trade_thread = threading.Thread(target=main.on_tick,
                                    args=[events, strategies,
                                          execution, portfolio])

    price_thread = threading.Thread(target=prices.begin, args=[
        ACCOUNT_ID, "EUR_USD", events
    ])

    trade_thread.start()
    price_thread.start()
