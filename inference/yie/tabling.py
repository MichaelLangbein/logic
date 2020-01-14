"""
    1. trace calls to fib
    2. table calls to fib
    3. repeat with yielding fib
"""


def tabling(f):
    tabling.execs = 0
    tabling.table = []
    def wrapped(*args, **kwargs):
        for (targs, tkwargs), tresult in tabling.table:
            if args == targs and kwargs == tkwargs:
                return tresult
        result = f(*args, **kwargs)
        tabling.table.append(((args, kwargs), result))
        tabling.execs += 1
        print(f"... {tabling.execs} calls made ...")
        return result
    wrapped.__name__ = 'w' + f.__name__
    return wrapped


def logging(f):
    logging.depth = 0
    def wrapped(*args, **kwargs):
        print(f"{'|---' * logging.depth}{f.__name__}{args}")
        logging.depth += 1
        result = f(*args, **kwargs)
        logging.depth -= 1
        print(f"{'|---' * logging.depth}{f.__name__}{args} => {result}")
        return result
    return wrapped


if __name__ == '__main__':
        
    @logging
    @tabling
    def fib(n):
        if n == 0:
            return 0
        if n == 1:
            return 1
        return fib(n-1) + fib(n-2)

    print(fib(7))

    @logging
    @tabling
    def yfib(n):
        if n == 0:
            yield 0
        elif n == 1:
            yield 1
        else:
            for f1 in yfib(n-1):
                for f2 in yfib(n-2):
                    yield f1 + f2

    for r in yfib(7):
        print(r)