import unittest

import sys
sys.path.append('../')

import queue

from execution import SimulatedExecutionHandler
#from parser import MetatraderCSVPriceHandler
from strategy.sma import SMA
from strategy.momentum import Momentum
from strategy.bolingerband import BolingerBand
from portfolio import PortfolioLocal

from csv_parser import DukascopyCSVPriceHandler
from manager import Manager


class TestHelloUnitTest(unittest.TestCase):

    def setUp(self):
        self.events = queue.Queue()
        self.status = dict()
        self.portfolio = PortfolioLocal(self.status)
        self.execution = SimulatedExecutionHandler(self.status)
        self.manager = Manager(self.status, self.events,
                               self.execution, self.portfolio, None)
        self.event_src = DukascopyCSVPriceHandler("EUR_USD", self.events)

    def simulate(self):
        while not self.events.empty():
            self.manager.perform_trade(self.events.get(False))

        print("Total Order Count: %s" % self.portfolio.order_count)
        print("Realized P&L     : %s" % round(self.status["realized_pnl"], 5))
        print("Profit Factor    : %s" % round(
            self.portfolio.total_profit/self.portfolio.total_loss, 5))

    def assertResult(self, count, pnl, pfac):
        self.assertEqual(count, self.portfolio.order_count)
        self.assertEqual(pnl, round(self.status["realized_pnl"], 5))
        self.assertEqual(pfac, round(
            self.portfolio.total_profit/self.portfolio.total_loss, 5))

    def test_sma(self):
        self.event_src.file_path = \
        "../data/EURUSD_Candlestick_15_s_BID_16.07.2015-16.07.2015.csv"
        self.event_src.stream_to_queue()

        strategy = SMA(self.status)
        strategy.mean_period_short = 20
        strategy.mean_period_long = 40
        self.manager.strategy = strategy
        self.simulate()

        self.assertResult(103, 19.3, 1.14339)

    def test_sma2(self):
        self.event_src.file_path = \
        "../data/EURUSD_Candlestick_15_s_BID_16.07.2015-16.07.2015.csv"
        self.event_src.stream_to_queue()

        strategy = SMA(self.status)
        strategy.mean_period_short = 40
        strategy.mean_period_long = 80
        self.manager.strategy = strategy
        self.simulate()

        self.assertResult(59, 58.6, 1.98157)

    def test_sma3(self):
        self.event_src.file_path = \
        "../data/EURUSD_Candlestick_15_s_BID_16.07.2015-16.07.2015.csv"
        self.event_src.stream_to_queue()

        strategy = SMA(self.status)
        strategy.mean_period_short = 20
        strategy.mean_period_long = 80
        self.manager.strategy = strategy
        self.simulate()

        self.assertResult(59, -14.2, 0.85899)

    def test_sma4(self):
        self.event_src.file_path = \
        "../data/EURUSD_Candlestick_15_s_BID_16.07.2015-16.07.2015.csv"
        self.event_src.stream_to_queue()

        strategy = SMA(self.status)
        strategy.mean_period_short = 40
        strategy.mean_period_long = 120
        self.manager.strategy = strategy
        self.simulate()

        self.assertResult(27, 35, 1.07973)

    def test_sma5(self):
        self.event_src.file_path = \
        "../data/EURUSD_Candlestick_15_s_BID_16.07.2015-16.07.2015.csv"
        self.event_src.stream_to_queue()

        strategy = SMA(self.status)
        strategy.mean_period_short = 30
        strategy.mean_period_long = 60
        self.manager.strategy = strategy
        self.simulate()

        self.assertResult(67, 11.4, 1.13029)
        
if __name__ == '__main__':
    unittest.main()
