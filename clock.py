import logging

import warnings

class Ticker():

    def __init__(self, func, interval, times, registered_at, offset):
        self.func = func
        self.interval = interval
        self.times = times
        self.registered_at = registered_at
        self.offset = offset

        self._injected = None
        self.callable = True
        self.expired = False


    def inject(self, obj):

        self.callable = False

        copy = Ticker(
            self.func,
            self.interval,
            self.times,
            self.registered_at,
            self.offset
        )

        copy._injected = obj
        setattr(obj, self.func.__name__, copy)



        clock.tickers.append(copy)

    


    def __call__(self, *args, **kwargs):
        """
        Calls the internal callback that the ticker holds.
        Returns true if function call was succeeded.
        """

        if not self.callable: return 

        if self._injected is not None:
            args = (self._injected, *args)

        try:
            self.func(*args, **kwargs)
        except TypeError as e:
            # some tickers' func require self as argument.
            # but if self is not yet injected in this ticker
            # function call would happen without self and gives this error.
            raise Exception(f"error possibly due to :{self.func} requires a `self` argument so not called. also settings this ticker as uncallable") from e
            self.callable = False
            return False
        else:
            return True


    def __str__(self):
        return (f"(callable: {self.callable}, expired: {self.expired},"
            + f"interval: {self.interval}, offset: {self.offset},"
            + f"registered_at: {self.registered_at}, times:{self.times},"
            + f"_injected: {self._injected}, func: {self.func.__qualname__}")

    def __repr__(self):
        return (f"(callable: {self.callable}, expired: {self.expired},"
            + f"interval: {self.interval}, offset: {self.offset},"
            + f"registered_at: {self.registered_at}, times:{self.times},"
            + f"_injected: {self._injected}, func: {self.func.__qualname__}")

            


class Clock:

    def __init__(self):

        self.global_tick = 0
        self.tickers = []

 

    def reset(self):
        self.global_tick = 0
        logging.info(f"{'>' * 30} CLOCK RESET: {self.global_tick} {'<' * 30}")
        self.handle_tickers(self.tickers)


    def tick(self):
        """
        makes the global clock tick.\n
        should be called ONLY AT ONE PLACE that makes the clock run.\n
        all tickers and tokens work based on this tick
        """
        self.global_tick += 1
        logging.info(f"{'>' * 30} TICK: {self.global_tick} {'<' * 30}")
        self.handle_tickers(self.tickers)


    def handle_tickers(self, tickers):
        logging.info("handling ticker(s)")


        # remove expired tickers
        indexes = []
        for i, ticker in enumerate(tickers):
            if ticker.expired:
                indexes.append(i)
                continue

        for index in sorted(indexes, reverse=True):
            del self.tickers[index]

        # tick all tickers
        for ticker in tickers:

            if ticker.interval + ticker.offset == 0:
            # not supporting because some tickers that want to run immediately
            # might be methods, to call these methods ticker MUST obtain the self
            # first. but before self is obtained the self obj should be fully 
            # prepared. (this means you can't inject self in the obj's __init__
            # as only a little part of obj is initialized in __init__)
            # but by not allowing immediate execution  there's atleast a tick
            # difference between obtaining self via __init__ and  calling the method
            # and hopefully the self obj was fully initialized.
                raise Exception('`interval` and `offset` should not cancel out each other\n\
                    which implies ticker should run immediately, which is not intentionally\n\
                    supported. call the function being decorated with ticker directly instead.')

            rio = (ticker.registered_at +  ticker.interval + ticker.offset)
            diff = self.global_tick - rio

            if diff % ticker.interval == 0 and diff >= 0:
                ran = ticker()
                if ran: ticker.times -= 1


            # mark finished entries.
            if ticker.times <= 0:
                ticker.expired = True

        logging.info("end handling ticker(s)")








    def ticker(self, interval=1, *, times=1000000, offset=0):
        """
        decorator to convert a method into a ticker 
        """
        def decorator(func):
            

            ticker = Ticker(
                func=func,
                interval=interval,
                times=times,
                registered_at=clock.global_tick,
                offset=offset

            )

            self.tickers.append(ticker)
            return ticker
        
        return decorator




class Token:
    def __init__(self, duration):
        self.duration = duration
        self.created_at = clock.global_tick

    
    @property
    def expired(self):
        if clock.global_tick >= self.created_at +  self.duration:
            return True
        else:
            return False

clock = Clock()