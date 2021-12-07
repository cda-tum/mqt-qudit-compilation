import itertools
import numpy as np


class H:
    def __init__(self, dimension):
        l = [list(range(dimension)), list(range(dimension))]
        # print(l)

        ret = np.outer([0 for x in range(dimension)], [0 for x in range(dimension)])
        # print(ret)

        for e0, e1 in itertools.product(*l):
            omega = np.mod(2 / dimension * (e0 * e1), 2)
            omega = omega * np.pi * 1j
            omega = np.e ** omega

            l1 = [0 for x in range(dimension)]
            l2 = [0 for x in range(dimension)]
            l1[e0] = 1
            l2[e1] = 1

            array1 = np.array(l1, dtype="complex")
            array2 = np.array(l2, dtype="complex")

            result = omega * np.outer(array1, array2)

            ret = ret + result

        ret = (1 / np.sqrt(dimension)) * ret

        # print()
        # print(ret)
        self.matrix = ret


class Z:
    def __init__(self, dimension):
        l = list(range(dimension))

        ret = np.outer([0 for x in range(dimension)], [0 for x in range(dimension)])

        for el in l:
            # print((2 * el / dimension, 2))
            omega = np.mod(2 * el / dimension, 2)
            omega = omega * np.pi * 1j
            omega = np.e ** omega

            # print(el)

            l1 = [0 for x in range(dimension)]
            l2 = [0 for x in range(dimension)]
            l1[el] = 1
            l2[el] = 1

            array1 = np.array(l1, dtype="complex")
            array2 = np.array(l2, dtype="complex")

            result = omega * np.outer(array1, array2)

            ret = ret + result

        # print("\n")
        # print(ret)
        self.matrix = ret


class X:
    def __init__(self, dimension):
        l = list(range(dimension))

        ret = np.outer([0 for x in range(dimension)], [0 for x in range(dimension)])

        for el in l:
            i = el
            i_plus_1 = np.mod(i + 1, dimension)

            l1 = [0 for x in range(dimension)]
            l2 = [0 for x in range(dimension)]
            l1[i_plus_1] = 1
            l2[i] = 1

            array1 = np.array(l1, dtype="complex")
            array2 = np.array(l2, dtype="complex")

            result = np.outer(array1, array2)

            ret = ret + result

        # print("\n")
        # print(ret)
        self.matrix = ret


class S:
    def __init__(self, dimension):
        l = list(range(dimension))

        ret = np.outer([0 for x in range(dimension)], [0 for x in range(dimension)])

        for el in l:
            omega = np.mod(2 / dimension * el * (el + 1) / 2, 2)
            omega = omega * np.pi * 1j
            omega = np.e ** omega

            l1 = [0 for x in range(dimension)]
            l2 = [0 for x in range(dimension)]
            l1[el] = 1
            l2[el] = 1

            array1 = np.array(l1, dtype="complex")
            array2 = np.array(l2, dtype="complex")

            result = omega * np.outer(array1, array2)

            ret = ret + result

        # print("\n")
        # print(ret)
        self.matrix = ret
