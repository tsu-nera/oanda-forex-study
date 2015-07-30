from strategy.strategy import Strategy


class PIP(Strategy):
    def __init__(self, status):
        super(PIP, self).__init__(status)

        self.pip_diff = 0.0005
        self.pip_mean_period = 5
        self.pip_mean = 0
        self.pip_mean_pre = 0
        self.pip_losscut_price = 0.0003

    def calc_pip_mean(self, timeseries, event):
        self.pip_mean_pre = self.pip_mean
#        self.pip_mean = event.bid
        self.pip_mean \
            = timeseries.get_latest_ts_as_df(self.pip_mean_period).mean()[0]

        # 利益確定条件を動的に伸ばす
        if not self.status["open_position"]:
            self.pip_diff = 0.0005

    # 4回クロスしたらcloseする
    def calc_pip_over_closs(self, timeseries, event):
        if self.status["open_position"]:
            if (self.sma_buy_condition() or self.sma_sell_condition()):
                self.pip_closs_count += 1
        else:
            self.pip_closs_count = 0
            self.pip_open_time = event.time

    def pip_over_cross_condiiton(self, event):
        return self.pip_closs_count >= 3

    def calc_pip_pnl(self):
        if self.status["position"] > 0:
            return self.pip_mean - self.status["opening_price"]
        else:
            return self.status["opening_price"] - self.pip_mean

    def pip_loss_cut_condition(self, event):
        # 損切りラインは 3pipにする.
        if abs(self.status["opening_price"] - self.pip_mean) \
           > self.pip_losscut_price:
            if self.calc_pip_pnl() < 0:

                return True
            else:
                return False
        else:
            return False

    def pip_close_condition(self, event):
        return self.calc_pip_pnl() > self.pip_diff

    def pip_expand_close_condition(self, event):
        if self.pip_diff > 0.0005 \
           and self.calc_pip_pnl() < self.pip_diff - 0.00015:
            return True

        # 利確の場合は動的にリミットを広げていく.
        if abs(self.status["opening_price"] - self.pip_mean) \
           > self.pip_diff:
            if self.calc_pip_pnl() > 0:
                self.pip_diff += 0.0001
                return False
            else:
                return True
        else:
            return False

    def pip_return_condition(self, event):
        if (event.time-self.status["opening_time"]).total_seconds() < 180:
            return False
        if self.pip_mean_pre == 0:
            return False
        if self.pip_mean_pre > self.status["opening_price"] \
           and self.pip_mean < self.status["opening_price"]:
            return True
        if self.pip_mean_pre < self.status["opening_price"] \
           and self.pip_mean > self.status["opening_price"]:
            return True
        return False
