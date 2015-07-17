import queue
import threading

from execution import OANDAExecutionHandler

from main import Main
from parser import HistoricCSVPriceHandler
from sma_strategy import SMAStrategy
from portfolio import Portfolio

if __name__ == "__main__":
    events = queue.Queue()  # 同期キュー

    prices = HistoricCSVPriceHandler("EUR_USD", events, "")

    status = dict()  # tick をまたいで記憶しておきたい情報

    # 戦略
    strategies = set([SMAStrategy(events, status)])

    portfolio = Portfolio(status)  # お金管理

    execution = OANDAExecutionHandler(status)  # 売買注文

    main = Main(0)

    trade_thread = threading.Thread(target=main.on_tick,
                                    args=[events, strategies,
                                          execution, portfolio])

    price_thread = threading.Thread(target=prices.stream_to_queue, args=[])

    trade_thread.start()
    price_thread.start()
