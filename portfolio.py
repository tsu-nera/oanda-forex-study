from settings import ACCESS_TOKEN, ACCOUNT_ID
import oandapy
from datetime import datetime
import pandas as pd

class Portfolio():
    def __init__(self, status):
        status["open_position"] = False
        status["position"] = 0

        self.unit = 1000
        self.status = status
        self.order_count = 0
        self.total_profit = 0
        self.total_loss = 0

        status["opening_price"] = 0
        status["executed_price"] = 0
        status["unrealized_pnl"] = 0
        status["realized_pnl"] = 0

        self.rpnl = pd.DataFrame()

        self.oanda = oandapy.API("practice", ACCESS_TOKEN)

    def update_portfolio(self, event):
        # Update position upon successful order
        self.order_count += 1

        if event.side == "buy":
            self.status["position"] += self.unit
        else:
            self.status["position"] -= self.unit

        if self.status["position"] == 0:
            self.status["open_position"] = False
            self.calculate_realized_pnl(event)
            self.rpnl.loc[event.time, "rpnl"] = self.status["realized_pnl"]
        else:
            self.status["opening_price"] = self.status["executed_price"]
            self.status["open_position"] = True

    def calculate_realized_pnl(self, event):
        current_pnl = self.unit * (
            (self.status["opening_price"] - self.status["executed_price"])
            if event.side == "buy" else
            (self.status["executed_price"] - self.status["opening_price"]))
        self.status["realized_pnl"] += current_pnl

        if current_pnl > 0:
            self.total_profit += current_pnl
        else:
            self.total_loss -= current_pnl

class PortfolioRemote(Portfolio):
    def show_current_status(self, event):
        self.calculate_unrealized_pnl(event)
        self.print_status(event)

    def calculate_unrealized_pnl(self, event):
        if self.status["open_position"]:
            # Retrieve position from server
            pos = self.oanda.get_position(ACCOUNT_ID,
                                          event.instrument)
            units = pos["units"]
            side = pos["side"]
            avg_price = float(pos["avgPrice"])

            self.status["unrealized_pnl"] = units * (
                (event.bid - avg_price)
                if (side == "buy")
                else (avg_price - event.ask))
        else:
            self.status["unrealized_pnl"] = 0

    def print_status(self, event):
        print("[%s] %s pos=%s RPnL=%s UPnL=%s" % (
            datetime.now().time(),
            event.instrument,
            self.status["position"],
            round(self.status["realized_pnl"], 5),
            round(self.status["unrealized_pnl"], 5)))

    
class PortfolioLocal(Portfolio):
    def show_current_status(self, event):
        print("[%s] %s pos=%s RPnL=%s UPnL=%s" % (
            datetime.now().time(),
            event.instrument,
            self.status["position"],
            round(self.status["realized_pnl"], 5),
            round(self.status["unrealized_pnl"], 5)))
