import queue
import threading
import time

from settings import ACCESS_TOKEN, ACCOUNT_ID
from execution import OANDAExecutionHandler
from streaming import StreamingForexPrices
from portfolio import PortfolioRemote
from timeseries import TimeSeries
from manager import Manager

from strategy.sma import SMA


heartbeat = 0.5


def on_tick(events, manager):
    while True:
        while not events.empty():

            event = events.get(False)

            manager.perform_trade(event)

            manager.portfolio.print_status(event)

        time.sleep(heartbeat)

if __name__ == "__main__":
    events = queue.Queue()  # 同期キュー

    price_src = StreamingForexPrices(environment="practice",
                                     access_token=ACCESS_TOKEN)

    status = dict()  # tick をまたいで記憶しておきたい情報

    portfolio = PortfolioRemote(status)  # お金管理

    execution = OANDAExecutionHandler(status)  # 売買注文

    strategy = SMA(status)

    timeseries = TimeSeries(False)

    manager = Manager(status, events, execution,
                      portfolio, strategy, timeseries)

    trade_thread = threading.Thread(target=on_tick,
                                    args=[events, manager])

    price_thread = threading.Thread(target=price_src.begin, args=[
        ACCOUNT_ID, "EUR_USD", events
    ])

    trade_thread.start()
    price_thread.start()
