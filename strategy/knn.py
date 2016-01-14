from strategy.strategy import Strategy
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor

# K近傍法によるストラテジ
# http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsRegressor.html


class KNN(Strategy):
    def __init__(self, status):
        Strategy.__init__(self, status)

        self.knn_train_period = 100
        self.knn_pred_period = 100
        self.knn_neighbors = 10
        self.predict = 0
        self.now = 0
        self.beta = 0
        self.knn_ts = pd.DataFrame()

    def calc_knn(self, timeseries, event):

        x = [[i] for i in range(self.knn_train_period)]
        y = timeseries.get_latest_ts_as_array(self.knn_train_period, event)

        if len(y) < len(x):
            return

        neigh = KNeighborsRegressor(n_neighbors=self.knn_neighbors)
        neigh.fit(x, y)

        self.now = event.bid
        self.predict = neigh.predict(
            self.knn_train_period + self.knn_pred_period)

        if self.status["is_sim"]:
            self.knn_ts.loc[event.time, event.instrument] = self.predict

        self.beta = self.predict - self.now

    def knn_buy_condition(self):
        return self.beta > 0.0001

    def knn_sell_condition(self):
        return self.beta < -0.0001

    def knn_close_buy_condition(self):
        return self.beta <= 0

    def knn_close_sell_condition(self):
        return self.beta >= 0
