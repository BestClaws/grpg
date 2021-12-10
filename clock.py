import logging

class Clock:

    def __init__(self):

        self.global_tick = 0

        self.tickers = [] # m ticker methods
        self.conc_tickers = [] # m ticker methods x n obj


    def tick(self):
        """
        makes the global clock tick.\n
        should be called ONLY AT ONE PLACE that makes the clock run.\n
        all tickers and tokens work based on this tick
        """
        self.global_tick += 1

        # invoke all registered ticker instances.

        indexes = []

        for i in range(len(self.conc_tickers)):
            entry = self.conc_tickers[i]
        

            if (self.global_tick - entry['registered_at']) % entry['interval'] == 0:
                entry['times'] -= 1
                entry['func'](entry['obj'])
            
            # mark finished entries.
            if entry['times'] <= 0:
                indexes.append(i)

        # remove finished entries
        for index in sorted(indexes, reverse=True):
            del self.conc_tickers[index]


    def register(self, obj):
        """
        registers a class to be able to use @clock.ticker
        """

        for ticker in self.tickers:
            # obj's class and base classes
            obj_class_tree  = [obj.__class__.__name__, *list(map(lambda base: base.__name__, obj.__class__.__bases__))]


            # check if any of the obj's class or base classes defined this ticker's func
            match = False
            for obj_class in obj_class_tree:
                if obj_class in ticker['func'].__qualname__:
                    match = True
                    break


            if match:
                # make sure entry with given (obj, ticker's func) is not already present
                # may happen when both, a class and it's base class register with clock
                # ex: Kaeya and GrpgCharacter's __init__() register with clock and GrpgCharacter defines a ticker's func
                # then ticker's func defiend GrpgCharacter matches  GrpgCharacter's and Kaeya's obj
                for conc_ticker in self.conc_tickers:
                    if conc_ticker['func'] is ticker['func'] and conc_ticker['obj'] is obj: return

                logging.info(f"registering <obj: {id(obj)}, class-tree: {obj_class_tree}>, with ticker func defined in <class: {ticker['func'].__qualname__}>")

                self.conc_tickers.append({
                    'obj': obj,
                    'registered_at': self.global_tick,
                    **ticker
                })



    def ticker(self, interval=1, times=1000000):
        """
        decorator to convert a method into a ticker 
        """
        def decorator(func):
            self.tickers.append({
                'func':func,
                'interval': interval,
                'times': times
            })
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