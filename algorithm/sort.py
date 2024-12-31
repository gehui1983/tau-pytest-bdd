from typing import List
from common.Log4test import Log4test

LOGGER = Log4test()


def getNext(ss: str) -> List[int]:
    length = len(ss)
    j = 0  # 前缀
    nex = [0] * length
    for i in range(1, length):  # 后缀
        while j > 0 and ss[j] != ss[i]:
            j = nex[j-1]
        if ss[j] == ss[i]:
            j += 1
            nex[i] = j
    return nex


# KMP算法
def kmp(source: str, substr: str):
    nex = getNext(substr)
    total = len(source)
    sub_len = len(substr)
    j = 0
    for i in range(0, total):
        if source[i] == substr[j]:
            if j < sub_len:
                j += 1
            if j == sub_len:
                LOGGER.info(f"{i-sub_len+1}-{i}")
                j = 0
            continue
        if j > 0 and source[i] != substr[j]:
            j = nex[j-1]


# 堆排序
def heap_sort(a_list: List[object]) -> List[object]:
    if len(a_list) <= 1:
        return a_list


# 快速排序
def quick_sort(a_list: List[object]) -> List[object]:
    if len(a_list) < 2:
        return a_list
    low = 0
    high = len(a_list) - 1
    return _quick_sort(a_list, low, high)


def _quick_sort(a_list: List[object], low, high) -> List[object]:
    if low < high:
        index_key = sub_sort(a_list, low, high)
        _quick_sort(a_list, low, index_key)
        _quick_sort(a_list, index_key + 1, high)
    return a_list


def sub_sort(a_list: List[object], low, high) -> int:
    key = a_list[low]
    while low < high:
        while (low < high) and (a_list[high] >= key):
            high = high - 1
        while (low < high) and (a_list[high] < key):
            a_list[low] = a_list[high]
            low = low + 1
            a_list[high] = a_list[low]

    a_list[low] = key
    LOGGER.info(f"{low}---{high}")
    LOGGER.info(a_list)
    return low


# 归并排序
def merge_sort(a_list: List[object]) -> List[object]:
    if len(a_list) <= 1:
        return a_list
    mid = len(a_list) // 2
    left = merge_sort(a_list[:mid])
    # print(left)
    right = merge_sort(a_list[mid:])
    # print(right)
    return merge(left, right)


def merge(left: List[object], right: List[object]) -> List[object]:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result += left[i:]
    result += right[j:]
    return result


# 冒泡排序
def bubble_sort(a_list: List[object]) -> List[object]:
    for j in range(0, len(a_list)):
        for i in range(0, len(a_list) - j - 1):
            if a_list[i] < a_list[i + 1]:
                temp = a_list[i]
                a_list[i] = a_list[i + 1]
                a_list[i + 1] = temp
    return a_list


# 选择排序
def select_sort(a_list: List[object]) -> List[object]:
    for j in range(0, len(a_list)):
        for i in range(j + 1, len(a_list)):
            if a_list[j] < a_list[i]:
                tmp = a_list[j]
                a_list[j] = a_list[i]
                a_list[i] = tmp
    return a_list


# 插入排序
def insert_sort(a_list: List[object]) -> List[object]:
    for j in range(0, len(a_list)):
        i = 0
        while j > i:
            if a_list[i] < a_list[j]:
                tmp = a_list[j]
                del a_list[j]
                a_list.insert(i, tmp)
                print(a_list)
            i = i + 1
    return a_list


def insert_sort_01(a_list: List[object]) -> List[object]:
    """
    :type a_list: object
    """
    alist_len = len(a_list)
    if alist_len <= 1:
        return a_list
    for i in range(1, alist_len):
        temp = a_list[i]
        j = i - 1
        while j >= 0 and a_list[j] > temp:
            a_list[j + 1] = a_list[j]
            j = j - 1
            a_list[j + 1] = temp
    return a_list

if __name__ == '__main__':
    # a_list = [7, 5, 6, 10, 8, 9, 11, 22, 21, 23, 1, 3]
    # LOGGER.info(quick_sort(a_list))
    LOGGER.info(kmp("fcvabcdefgabc", "abc"))
    # LOGGER.error(bubble_sort(a_list))
    # LOGGER.debug(bubble_sort(a_list))

    # class ab:
    #     def __init__(self):
    #         self.v = id(self)
    #         print(self.v)
    #
    #
    # o = ab()
    # d = {"qw": 123}
    # print(hasattr(d, 'qw'))
    # print(id(o) == o.v)
