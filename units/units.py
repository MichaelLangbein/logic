class Unit:
    # enum: ["m", "kg"]
    # denom: ["s", "s"]
    def __init__(self, enum, denom):
        self.enum = sorted(enum)
        self.denom = sorted(denom)

    def __eq__(self, other):
        for es, eo in zip(self.enum, other.enum):
            if es != eo:
                return False
        for ds, do in zip(self.denom, other.denom):
            if ds != do:
                return False
        return True

    def __ne__(self, other):
        return not (self == other)

    def __add__(self, other):
        if self != other:
            raise Exception(f"Units don't match: {self} != {other}")
        return self

    def __mul__(self, other):
        allEnum = self.enum + other.enum
        allDenom = self.denom + other.denom
        newEnum = []
        newDenom = []
        for 
        return Unit(newEnum, newDenom)

    def __div__(self, other):


    def __str__(self):
        # TODO: when a factor appears multiple times, write it as a power
        es = " ".join(self.enum)
        ds = " ".join(self.denom)
        return f"[{es}/{ds}]"

        


class Factor:
    def __init__(self, value, unit):
        self.value = value
        self.unit = unit

    def __add__(self, other):
        return Factor(self.value + other.value, self.unit + other.unit)

    def __mul__(self, other):