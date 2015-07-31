import queue
import threading
import time

from settings import ACCESS_TOKEN, ACCOUNT_ID, DOMAIN
from execution import OANDAExecutionHandler
from streaming import StreamingForexPrices
from portfolio import PortfolioRemote
from timeseries import TimeSeries
from manager import Manager

from strategy.sma import SMA
from strategy.sma_pip import SMAPIP
from strategy.bol_pip_rsi import BOLPIPRSI

heartbeat = 0.5


def on_tick(events, manager):
    while True:
        try:
            event = events.get(False)
        except queue.Empty:
            pass
        else:
            manager.perform_trade(event)
            manager.portfolio.show_current_status(event)
        time.sleep(heartbeat)

if __name__ == "__main__":
    events = queue.Queue()

    price_src = StreamingForexPrices(environment=DOMAIN,
                                     access_token=ACCESS_TOKEN)

    status = dict() 
    status["is_sim"] = False

    portfolio = PortfolioRemote(status)

    execution = OANDAExecutionHandler(status)

    strategy = BOLPIPRSI(status)

    timeseries = TimeSeries(status)

    manager = Manager(status, events, execution,
                      portfolio, strategy, timeseries)

    trade_thread = threading.Thread(target=on_tick,
                                    args=[events, manager])

    price_thread = threading.Thread(target=price_src.begin, args=[
        ACCOUNT_ID, "EUR_USD", events
    ])

    trade_thread.start()
    price_thread.start()
