from abc import ABCMeta, abstractmethod
from event import TickEvent
import pandas as pd
from dateutil.parser import parse


class PriceHandler(object):
    __metaclass__ = ABCMeta

    def __init__(self, pairs, events_queue):
        self.pairs = pairs
        self.events_queue = events_queue
#        self.file_path = "data/EURUSD_Ticks_24.07.2015-24.07.2015.csv"
        self.file_path = "data/EURUSD_Ticks_24.07.2015-1H.csv"

    @abstractmethod
    def stream_to_queue(self):
        raise NotImplementedError("Should implement stream_to_queue()")

    @abstractmethod
    def _open_convert_csv_files(self):
        raise NotImplementedError("Should implement stream_to_queue()")


class DukascopyCSVPriceHandler(PriceHandler):
    def _open_convert_csv_files(self):

        self.pair = pd.io.parsers.read_csv(
            self.file_path, header=True, index_col=0, parse_dates=True,
            names=("Time", "Ask", "Bid", "AskVolume", "BidVolume")
        ).iterrows()

    def stream_to_queue(self):
        self._open_convert_csv_files()
        for index, row in self.pair:
            tev = TickEvent(self.pairs, index, row["Bid"], row["Ask"])
            self.events_queue.put(tev)


class MetatraderCSVPriceHandler(PriceHandler):
    def _open_convert_csv_files(self):
        pair_path = "data/EURUSD1_150716_mt4.csv"
        self.pair = pd.io.parsers.read_csv(
            pair_path, header=True, parse_dates=True,  # index_col=0,
            names=("Date", "Time", "Start", "Low", "High", "End", "Hoge")
        ).iterrows()

    def stream_to_queue(self):
        self._open_convert_csv_files()
        for index, row in self.pair:
            date = parse(row["Date"] + " " + row["Time"])
            tev = TickEvent(self.pairs, date, row["Start"], row["Start"])
            self.events_queue.put(tev)
