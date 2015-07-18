import queue

from execution import SimulatedExecutionHandler

from parser import HistoricCSVPriceHandler
from sma_strategy import SMAStrategy
from portfolio import PortfolioLocal
from progressbar import ProgressBar

import matplotlib.pyplot as plt


def simulating():
    progress = ProgressBar(events.qsize()).start()
    for i in range(events.qsize()):
        event = events.get(False)
        # ストラテジチェック
        for strategy in strategies:
            if(strategy.check(event)):
                break
        progress.update(i + 1)

if __name__ == "__main__":
    events = queue.Queue()  # 同期キュー

    prices = HistoricCSVPriceHandler("EUR_USD", events, "")

    status = dict()  # tick をまたいで記憶しておきたい情報
    status["heartbeat"] = 0

    portfolio = PortfolioLocal(status)

    execution = SimulatedExecutionHandler(status)

    strategy = SMAStrategy(events, status, execution, portfolio)
    strategies = set([strategy])

    print("=== Backtesting Start =================================== ")

    prices.stream_to_queue()

    simulating()

    print("=== End .... v(^_^)v  =================================== ")

    print("Total Order Count: %s" % portfolio.order_count)
    print("Realized P&L     : %s" % round(status["realized_pnl"]), 5)
    print("Profit Factor    : %s" % round(
        portfolio.total_profit/portfolio.total_loss, 5))

    plt.plot(strategy.prices.index, strategy.prices)
    plt.plot(strategy.buys.index, strategy.buys, "ro")
    plt.plot(strategy.sells.index, strategy.sells, "go")

    portfolio.rpnl.plot()
    plt.show()
