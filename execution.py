from __future__ import print_function

from abc import ABCMeta, abstractmethod
from settings import ACCESS_TOKEN, ACCOUNT_ID
import oandapy


class ExecutionHandler(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def execute_order(self):
        raise NotImplementedError("Should implement execute_order()")


class SimulatedExecutionHandler(ExecutionHandler):
    def execute_order(self, event):
        pass


class OANDAExecutionHandler(ExecutionHandler):

    def __init__(self, status):
        self.oanda = oandapy.API("practice", ACCESS_TOKEN)
        self.status = status

    def execute_order(self, event):
        response = self.oanda.create_order(
            account_id=ACCOUNT_ID,
            instrument=event.instrument,
            units=1000,
            side=event.side,
            type='market')

        if response is not None:
            # 購入時の値段を記録
            self.status["executed_price"] = float(response["price"])

            print("Placed order %s %s %s at market." %
                  (event.side, 1000, event.instrument))
            return True  # Order is successful

        return False  # Order is unsuccessful
