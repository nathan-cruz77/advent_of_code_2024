# Enumerate iterable containing iterables recursively.
#
# Like `enumerate` but can recursively go into nested iterables yielding each
# entry's index as a tuple.
#
#
# Sample usage:
#
#   >>> list(enumerate_n('123'))
#   [(0, '1'), (1, '2'), (2, '3')]
#
#   >>> list(enumerate_n(['123']))
#   [(0, '123')]
#
#   >>> list(enumerate_n(['123'], n=2))
#   [((0, 0), '1'), ((0, 1), '2'), ((0, 2), '3')]
#
#   >>> list(enumerate_n(['123', [1, 2]], n=2))
#   [((0, 0), '1'),
#    ((0, 1), '2'),
#    ((0, 2), '3'),
#    ((1, 0), 1),
#    ((1, 1), 2)]
#
def enumerate_n(iterable, start=0, n=1):
    from collections.abc import Iterable

    count = start

    for item in iterable:
        if isinstance(item, Iterable) and n > 1:
            for index, value in enumerate_n(iter(item), start=start, n=n - 1):
                if not isinstance(index, Iterable):
                    index = [index]

                yield tuple([count, *index]), value
        else:
            yield count, item

        count += 1


# Slides through iterable each `n` elements.
#
# Sample usage:
#
#   >>> list(sliding_window([1, 2, 3, 4]))
#   [(1, 2), (2, 3), (3, 4)]
#
#   >>> list(sliding_window([1, 2, 3]))
#   [(1, 2), (2, 3)]
#
#   >>> list(sliding_window([1, 2, 3, 4], n=3))
#   [(1, 2, 3), (2, 3, 4)]
#
def sliding_window(iterable, n=2):
    from itertools import islice

    args = [islice(iter(iterable), i, None) for i in range(n)]
    return zip(*args)
