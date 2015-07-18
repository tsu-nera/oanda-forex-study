import queue

from execution import SimulatedExecutionHandler

from main import Main
from parser import HistoricCSVPriceHandler
from sma_strategy import SMAStrategy
from portfolio import PortfolioLocal

if __name__ == "__main__":
    events = queue.Queue()  # 同期キュー

    prices = HistoricCSVPriceHandler("EUR_USD", events, "")

    status = dict()  # tick をまたいで記憶しておきたい情報
    status["heartbeat"] = 0

    strategy = SMAStrategy(events, status)
    strategies = set([strategy])

    portfolio = PortfolioLocal(status)

    execution = SimulatedExecutionHandler(status)

    main = Main(False)

    print("=== Backtesting Start === ")

    prices.stream_to_queue()
    main.on_tick(events, strategies, execution, portfolio)

    print("=== End .... v(^_^)v  === ")

    import matplotlib.pyplot as plt
    plt.plot(strategy.prices.index, strategy.prices)
    plt.plot(strategy.buys.index, strategy.buys, "ro")
    plt.plot(strategy.sells.index, strategy.sells, "go")
    plt.show()

