# http://interactivepython.org/runestone/static/pythonds/SortSearch/TheBinarySearch.html
def binary_search(alist, item):
    first = 0
    last = len(alist) - 1
    midpoint = -1

    found = False
    while first <= last and not found:
        midpoint = (first + last) / 2
        if alist[midpoint] == item:
            found = True
        else:
            if item < alist[midpoint]:
                last = midpoint - 1
            else:
                first = midpoint + 1
    return midpoint
