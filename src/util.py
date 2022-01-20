"""
Adapted from Andy Salerno (2016)
"""

import math
import random

K = 0
V = 1


silent = False


def make_silent(val):
    assert val is True or val is False
    global silent
    silent = val


def info(message):
    if not silent:
        if not message:
            print()
        else:
            print(message)


def info_newline():
    if not silent:
        print()


def to_offset(move, size):
    x, y = move
    return y * size + x


def is_in_bounds(x, y, size):
    return 0 <= x < size and 0 <= y < size


def prop_parse(props):
    """
    Given an input list of strings, for each string that has an = in it,
    return a mapping of the left halves to the right halves. For a string to
    end up in the map it must have format key=value, forming {key: value}
    """

    result = {}

    for arg in props:
        split = arg.split("=")
        if len(split) != 2:
            continue
        property = split[0]
        value = split[1]

        if value == "True":
            value = True
        elif value == "False":
            value = False
        else:
            try:
                value = float(value)
                if value.is_integer():
                    value = int(value)
            except ValueError:
                pass

        result[property] = value

    return result


class CacheDict:
    def __init__(self):
        self.c_list = []
        self.flip = True

    def update(self, k, v):
        if len(self.c_list) < 2:
            self.c_list.append((k, v))
        else:
            if self.flip:
                self.c_list[0] = (k, v)
            else:
                self.c_list[1] = (k, v)
            self.flip = not self.flip

    def get(self, k):
        size = len(self.c_list)
        if size >= 1 and self.c_list[0][K] == k:
            # if size >= 1 and np.array_equal(self.c_list[0][K], k):
            return self.c_list[0][V]
        elif size >= 2 and self.c_list[1][K] == k:
            # elif size >= 2 and np.array_equal(self.c_list[1][K], k):
            return self.c_list[1][V]
        else:
            return None
