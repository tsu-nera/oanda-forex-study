import oandapy
import queue
from datetime import datetime

from settings import ACCESS_TOKEN, ACCOUNT_ID
from event import TickEvent


class StreamingForexPrices(oandapy.Streamer):
    def __init__(self, *args, **kwargs):
        oandapy.Streamer.__init__(self, *args, **kwargs)
        self.dt_format = "%Y-%m-%dT%H:%M:%S.%fZ"

    def begin(self, account_id, instruments, event_queue):
        self.event_queue = event_queue
        self.start(accountId=account_id, instruments=instruments)

    def on_success(self, data):
        time, symbol, bid, ask = self.parse_tick_data(data["tick"])
        event = TickEvent(symbol, time, bid, ask)
        self.event_queue.put(event)

    def parse_tick_data(self, dict_data):
        time = datetime.strptime(dict_data["time"], self.dt_format)
        ask = float(dict_data["ask"])
        bid = float(dict_data["bid"])
        instrument = dict_data["instrument"]
        return time, instrument, bid, ask


if __name__ == "__main__":
    prices = StreamingForexPrices(environment="practice",
                                  access_token=ACCESS_TOKEN)
    prices.begin(ACCOUNT_ID, "EUR_USD", queue.Queue())
