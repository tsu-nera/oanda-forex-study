from abc import ABCMeta, abstractmethod
from event import TickEvent
import pandas as pd

from decimal import Decimal,  ROUND_HALF_DOWN


class PriceHandler(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def stream_to_queue(self):
        raise NotImplementedError("Should implement stream_to_queue()")


class HistoricCSVPriceHandler(PriceHandler):

    def __init__(self, pairs, events_queue, csv_dir):
        """
        pairs - The list of currency pairs to obtain.
        events_queue - The events queue to send the ticks to.
        csv_dir - Absolute directory path to the CSV files.
        """
        self.pairs = pairs
        self.events_queue = events_queue
        self.csv_dir = csv_dir
        self.cur_bid = None
        self.cur_ask = None

    def _open_convert_csv_files(self):
        """
        Opens the CSV files from the data directory, converting
        them into pandas DataFrames within a pairs dictionary.
        """
        pair_path = "data/EURUSD_Candlestick_15_s_BID_17.07.2015-17.07.2015.csv"
        self.pair = pd.io.parsers.read_csv(
            pair_path, header=True, index_col=0, parse_dates=True,
            names=("Time", "Ask", "Bid", "AskVolume", "BidVolume")
        ).iterrows()

    def stream_to_queue(self):
        self._open_convert_csv_files()
        for index, row in self.pair:
            # self.cur_bid = Decimal(str(row["Bid"])).quantize(
            #     Decimal("0.00001", ROUND_HALF_DOWN)
            # )
            # self.cur_ask = Decimal(str(row["Ask"])).quantize(
            #     Decimal("0.00001", ROUND_HALF_DOWN)
            # )
            # tev = TickEvent(self.pairs[0], index, self.cur_bid, self.cur_ask)
            tev = TickEvent(self.pairs, index, row["Bid"], row["Ask"])
            self.events_queue.put(tev)
