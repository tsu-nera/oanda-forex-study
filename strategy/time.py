from strategy.strategy import Strategy


class Time(Strategy):
    def __init__(self, status):
        super(Time, self).__init__(status)

        self.guard_time = 30
        
    def time_guard_condition(self, event):
        return (event.time - self.status["opening_time"]).total_seconds() \
            < self.guard_time

    def time_close_guard_condition(self, event):
        if self.status["close_time"] == 0:
            return False
        return (event.time - self.status["close_time"]).total_seconds() \
            < self.guard_time
