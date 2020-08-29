# cost_with_addition_and_exponentiation.py
from math import ceil, sqrt, log


# Calculates the cost of an integer using the operations {+, ^}


def c(limit: int):
    """Take a positive integer and returns a tuple where each index corresponding to an object representing the cost of
    the given index. For example,
    at index 6 is an object representing C_{+,^}(6).

    The cost object has the following attributes:
    .cost     -- the cost of the integer
    .how      -- how the given cost was calculated (a string)
    .num      -- the integer whose cost is being calculated
    .factors  -- the factors of the number whose cost is being calculated. (a tuple of tuples of integers)
                    for example, the factors of 6 is ((1,6), (2,3))

    At index 0 the value is None as C(0) is undefined
    """

    costs = [None, ]  # C(0)=undefined

    class Cost:

        def __init__(self, num: int, forced: int = -1):
            """forced is used to force a cost. this is used for C(1) and C(2) as these are needed or the
             program will break"""
            self.num = num

            # find the factors
            arr = []
            root = sqrt(num)
            root_ceil = ceil(root)
            for i in range(1, root_ceil):
                if num % i == 0:  # if factor
                    arr.append((i, num // i))

            if root == root_ceil:  # if root^2 = num
                arr.append((root_ceil, root_ceil))

            self.factors = tuple(arr)

            # is it forced?
            if forced >= 0:
                self.how = "defined"
                self.cost = forced
                return

            self.how = "undefined"
            self.cost = num + 1

            # exponents
            for e1 in range(2, ceil(sqrt(num)) + 1):
                e2 = int(log(num, e1))
                if (e2 == 1):  # if we get num^1 we skip, cuz num is undefined as of now
                    continue
                testCost = e1 ** e2
                if (testCost == num):  # if f1^f2 = num
                    tempCost = costs[e1].cost + costs[e2].cost
                    if (self.cost > tempCost):
                        self.cost = tempCost
                        self.how = ["%d ^ %d" % (e1, e2)]

            # addition
            for i in range(1, self.num // 2 + 1):  # [1, num/2]
                potential_cost = costs[self.num - i].cost + costs[i].cost
                if potential_cost < self.cost:
                    self.cost = potential_cost
                    self.how = "C(%d + %d)" % (i, self.num - i)

        def __str__(self):
            return "C_{+,^}(%d) = %d" % (self.num, self.cost)

        def __repr__(self):
            return str(self)

    costs.append(Cost(1, 1))  # C(1) = 1
    for i in range(2, limit):
        costs.append(Cost(i))

    return tuple(costs)
