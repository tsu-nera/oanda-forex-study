from settings import ACCESS_TOKEN, ACCOUNT_ID, DOMAIN
import oandapy
from datetime import datetime
import pandas as pd


class Portfolio():
    def __init__(self, status):
        status["open_position"] = False
        status["position"] = 0

        self.status = status
        self.order_count = 0
        self.total_profit = 0
        self.total_loss = 0
        self.spread = 0.00005
        self.current_pnl = 0

        self.win_count = 0
        self.lose_count = 0

        status["opening_price"] = 0
        status["executed_price"] = 0
        status["unrealized_pnl"] = 0
        status["realized_pnl"] = 0

        self.rpnl = pd.DataFrame()

        self.oanda = oandapy.API(DOMAIN, ACCESS_TOKEN)

    def update_portfolio(self, event):
        # Update position upon successful order
        self.order_count += 1

        if event.side == "buy":
            self.status["position"] += self.status["units"]
            print("buy")
        else:
            self.status["position"] -= self.status["units"]
            print("sell")

        if self.status["position"] == 0:
            print("closed...")
            self.status["open_position"] = False
            self.status["close_time"] = event.time
            self.calculate_realized_pnl(event)
            if self.status["is_sim"]:
                self.rpnl.loc[event.time, "rpnl"] = self.status["realized_pnl"]
        else:
            self.status["opening_price"] = self.status["executed_price"]
            self.status["opening_time"] = event.time
            self.status["open_position"] = True

    def calculate_realized_pnl(self, event):
        self.current_pnl = self.status["units"] * (
            (self.status["opening_price"] - self.status["executed_price"]
             - self.spread)
            if event.side == "buy" else
            (self.status["executed_price"] - self.status["opening_price"]
             - self.spread))
        self.status["realized_pnl"] += self.current_pnl

        if self.is_win():
            self.total_profit += self.current_pnl
            self.win_count += 1
        else:
            self.total_loss -= self.current_pnl
            self.lose_count += 1

    def is_win(self):
        return self.current_pnl > 0

    def print_current_status(self, event, pnl):
        print("[%s] no=%2s open_price=%.7s exe_price=%.7s PnL=%.7s" % (
            event.time,
            self.order_count,
            round(self.status["opening_price"], 6),
            round(self.status["executed_price"], 6),
            round(pnl, 5)
        ))


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
