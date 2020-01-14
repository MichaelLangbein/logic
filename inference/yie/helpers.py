from functools import wraps



def toList(results, nr=None):
    out = []
    for i, result in enumerate(results):
        if nr and i >= nr:
            break
        out.append(result)
    return out
