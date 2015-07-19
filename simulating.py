import queue

from execution import SimulatedExecutionHandler

from parser import DukascopyCSVPriceHandler
#from parser import MetatraderCSVPriceHandler
from strategy.sma import SMA
#from strategy.momentum import Momentum
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

            if events.empty():
                # 最後は決済して終了
                if status["position"] < 0:
                    strategy.order_and_calc_portfolio(event, True)
                else:
                    strategy.order_and_calc_portfolio(event, False)
                break
        progress.update(i + 1)


if __name__ == "__main__":
    events = queue.Queue()  # 同期キュー

#    prices = MetatraderCSVPriceHandler("EUR_USD", events)
    prices = DukascopyCSVPriceHandler("EUR_USD", events)

    status = dict()  # tick をまたいで記憶しておきたい情報
    status["heartbeat"] = 0

    portfolio = PortfolioLocal(status)

    execution = SimulatedExecutionHandler(status)

    strategy = SMA(events, status, execution, portfolio)
#    strategy = Momentum(events, status, execution, portfolio)
    strategies = set([strategy])

    print("=== Backtesting Start =================================== ")

    prices.stream_to_queue()

    simulating()

    print("=== End .... v(^_^)v  =================================== ")

    print("Total Order Count: %s" % portfolio.order_count)
    print("Realized P&L     : %s" % round(status["realized_pnl"], 5))
    print("Profit Factor    : %s" % round(
        portfolio.total_profit/portfolio.total_loss, 5))
    # print("Profit/Loss      : %s/%s" % (
    #     portfolio.total_profit, portfolio.total_loss))

    plt.plot(strategy.prices.index, strategy.prices)
    plt.plot(strategy.buys.index, strategy.buys, "ro")
    plt.plot(strategy.sells.index, strategy.sells, "go")

    portfolio.rpnl.plot()
    plt.show()
