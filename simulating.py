import matplotlib.pyplot as plt
import queue

from execution import SimulatedExecutionHandler
from csv_parser import DukascopyCSVPriceHandler

#from parser import MetatraderCSVPriceHandler
from portfolio import PortfolioLocal
from progressbar import ProgressBar
from timeseries import TimeSeries
from manager import Manager

from strategy.sma_ols import SMAOLS
from strategy.sma_rsi import SMARSI
from strategy.rsi import RSI
from strategy.granville import Granville
from strategy.sma import SMA
from strategy.sma2 import SMA2
from strategy.ema import EMA
from strategy.momentum import Momentum
from strategy.bolingerband import BolingerBand

def simulating(events, manager):
    progress = ProgressBar(events.qsize()).start()

    for i in range(events.qsize()):
        # キューからTickEvent取り出し
        event = events.get(False)

        # トレード実行
        manager.perform_trade(event)

        # 最後は決済して終了
        check_and_close_last_order(event)

        progress.update(i + 1)


def check_and_close_last_order(event):
    if events.empty():
        if status["position"] < 0:
            manager.order_and_calc_portfolio(event, True)
        else:
            manager.order_and_calc_portfolio(event, False)

if __name__ == "__main__":
    events = queue.Queue()  # 同期キュー

    status = dict()  # tick をまたいで記憶しておきたい情報

    portfolio = PortfolioLocal(status)

    execution = SimulatedExecutionHandler(status)

    timeseries = TimeSeries(True)
    
#    strategy = SMARSI(status)
    strategy = EMA(status)
#    strategy = SMA2(status)
#    strategy = RSI(status)
#    strategy = SMAOLS(status)
#    strategy = Granville(status)
#    strategy = Momentum(status)
#    strategy = BolingerBand(status)

    manager = Manager(status, events, execution,
                      portfolio, strategy, timeseries)

    print("=== Backtesting Start =================================== ")

    #    event_src = MetatraderCSVPriceHandler("EUR_USD", events)
    event_src = DukascopyCSVPriceHandler("EUR_USD", events)
    event_src.stream_to_queue()

    simulating(events, manager)

    print("=== End .... v(^_^)v  =================================== ")

    print("Total Order Count: %s" % portfolio.order_count)
    print("Realized P&L     : %s" % round(status["realized_pnl"], 5))
    print("Profit Factor    : %s" % round(
        portfolio.total_profit/portfolio.total_loss, 5))
    # print("Profit/Loss      : %s/%s" % (
    #     portfolio.total_profit, portfolio.total_loss))

    plt.plot(timeseries.prices.index, timeseries.prices)

    plt.plot(strategy.sma_long_ts.index, strategy.sma_long_ts)
    plt.plot(strategy.sma_short_ts.index, strategy.sma_short_ts)
    # plt.plot(strategy.sma_ols_ts.index, strategy.sma_ols_ts)

    plt.plot(timeseries.buys.index, timeseries.buys, "ro")
    plt.plot(timeseries.sells.index, timeseries.sells, "go")

    portfolio.rpnl.plot()

    plt.grid(True)
    plt.show()
