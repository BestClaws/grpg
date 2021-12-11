import logging



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


        # some tickers may  run immediately after registering.
        clock.handle_tickers([copy])

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
        except TypeError:
            # some tickers' func require self as argument.
            # but if self is not yet injected in this ticker
            # function call would happen without self and gives this error.
            return False
        else:
            return True



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


        # remove expired entries
        indexes = []
        for i in range(len(tickers)):
            if tickers[i].expired:
                indexes.append(i)
                continue

        for index in sorted(indexes, reverse=True):
            del self.tickers[index]

        
        for ticker in tickers:
            # tick

            # if self.global_tick == ticker.registered_at and ticker.offset == 0:
            #     # if global_tick and registered_at are equal the below if condition
            #     # will be true, no matter the interval (assuming offset=0)
            #     return

            tick_diff = self.global_tick - (ticker.registered_at + ticker.offset)


            if (self.global_tick - tick_diff) % ticker.interval == 0:
                ran = ticker()
                if ran: ticker.times -= 1


            # mark finished entries.
            if ticker.times <= 0:
                ticker.expired = True








    def ticker(self, interval=1, *, times=1000000, offset=0):
        """
        decorator to convert a method into a ticker 
        """
        logging.info(f"decorating interval: {interval}, times: {times}")
        def decorator(func):
            

            ticker = Ticker(
                func=func,
                interval=interval,
                times=times,
                registered_at=clock.global_tick,
                offset=offset

            )

            # some tickers may  run immediately after registering.
            self.handle_tickers([ticker])

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