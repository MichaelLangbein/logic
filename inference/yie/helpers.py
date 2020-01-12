from functools import wraps



def toList(results, nr=None):
    out = []
    for i, result in enumerate(results):
        if nr and i >= nr:
            break
        out.append(result)
    return out


def log(func):
    funcName = func.__name__
    separator = '|  '
    log.recursionDepth = 0

    @wraps(func)
    def loggedFunc(*args, **kwargs):
        print(f"{separator * log.recursionDepth} |-- {funcName}{args}")
        log.recursionDepth += 1
        result = func(*args, **kwargs)
        log.recursionDepth -= 1
        print(f"{separator * (log.recursionDepth + 1)} |-- return {result}")
        return result