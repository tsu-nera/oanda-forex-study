import queue
import threading
import time

from execution import OANDAExecutionHandler
from settings import ACCESS_TOKEN, ACCOUNT_ID
from streaming import StreamingForexPrices

# from parser import HistoricCSVPriceHandler
from sma_strategy import SMAStrategy

heartbeat = 0.5


def on_tick(event_queue, strategies, execution, status):
    status["open_position"] = False
    status["position"] = 0

    while True:
        while not event_queue.empty():
            event = event_queue.get(False)

            if event.type == 'TICK':
                # ストラテジチェック
                for strategy in strategies:
                    if(strategy.check(event)):
                        break
            elif event.type == 'SIGNAL':
                print("signal event")

                # 売り買いの実行
                execution.execute_order(event)

                # ポートフォリオ更新
                check_and_send_order(event, status)

        time.sleep(heartbeat)


def check_and_send_order(event, status):
    # Update position upon successful order
        if event.side == "buy":
            status["position"] += 1000
        else:
            status["position"] -= 1000

        if status["position"] == 0:
            status["open_position"] = False
#            self.calculate_realized_pnl(is_buy)
        else:
            #  self.opening_price = self.executed_price
            status["open_position"] = True


def calculate_realized_pnl(self, is_buy):
    self.realized_pnl += self.qty * (
        (self.opening_price - self.executed_price)
        if is_buy else
        (self.executed_price - self.opening_price))


def calculate_unrealized_pnl(self, bid, ask):
    if self.is_position_opened:
        # Retrieve position from server
        pos = self.oanda.get_position(self.account_id,
                                      self.instrument)
        units = pos["units"]
        side = pos["side"]
        avg_price = float(pos["avgPrice"])

        self.unrealized_pnl = units * (
            (bid - avg_price)
            if (side == "buy")
            else (avg_price - ask))
    else:
        self.unrealized_pnl = 0

if __name__ == "__main__":
    events = queue.Queue()

    prices = StreamingForexPrices(environment="practice",
                                  access_token=ACCESS_TOKEN)
#    prices = HistoricCSVPriceHandler("EUR_USD", events, "")

    status = dict()  # tick をまたいで記憶しておきたい情報

    strategies = set([SMAStrategy(events, status)])

    execution = OANDAExecutionHandler()

    trade_thread = threading.Thread(target=on_tick,
                                    args=[events, strategies,
                                          execution, status])

#    price_thread = threading.Thread(target=prices.stream_to_queue, args=[])
    price_thread = threading.Thread(target=prices.begin, args=[
        ACCOUNT_ID, "EUR_USD", events
    ])

    trade_thread.start()
    price_thread.start()
