from strategy.strategy import Strategy


class Time(Strategy):
    def __init__(self, status):
        super(Time, self).__init__(status)

        self.guard_time = 30
        
    def time_guard_condition(self, event):
        return (self.status["opening_time"] - event.time).total_seconds() \
            < self.guard_time
