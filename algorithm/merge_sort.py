from typing import List


def merge_sort(li):
    length = len(li)
    if length <= 1:
        return li
    mid = length // 2
    left = merge_sort(li[:mid])
    right = merge_sort(li[mid:])
    return sort(left, right)


def sort(left, right):
    result = list()
    li = ri = 0
    while li < len(left) and ri < len(right):
        k_li, v_li = left[li]
        k_ri, v_ri = right[ri]
        if v_li < v_ri:
            result.append(left[li])
            li = li + 1
        else:
            result.append(right[ri])
            ri = ri + 1
    if li < len(left):
        result += left[li:]
    if ri < len(right):
        result += right[ri:]
    return result


if __name__ == '__main__':
    arr = [(0, 1), (1, 0), (2, 2), (3, 16), (4, -1), (5, -9), (6, 10), (7, 10), (8, 25), (9, 16), (10, 30)]
    print(merge_sort(arr))
