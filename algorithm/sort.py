from typing import List


def merge_sort(li: List[object]) -> List[object]:
    if len(li) <= 1:
        return li
    mid = len(li) // 2
    left = merge_sort(li[:mid])
    # print(left)
    right = merge_sort(li[mid:])
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


def mao_pao(li: List[object]) -> List[object]:

    for j in range(0, len(li)):
        for i in range(0, len(li) - j - 1):
            if li[i] < li[i + 1]:
                temp = li[i]
                li[i] = li[i + 1]
                li[i + 1] = temp
    return li


def select_sort(li: List[object]) -> List[object]:
    for j in range(0, len(li)):
        for i in range(j + 1, len(li)):
            if li[j] < li[i]:
                tmp = li[j]
                li[j] = li[i]
                li[i] = tmp
    return li


def insert_sort(li: List[object]) -> List[object]:
    for j in range(0, len(li)):
        i = 0
        while j > i:
            if li[i] < li[j]:
                tmp = li[j]
                del li[j]
                li.insert(i, tmp)
                print(li)
            i = i + 1
    return li


if __name__ == '__main__':
    lst = [7, 10, 8, 9, 11, 22, 21, 23, 1, 3]

    print(mao_pao(lst))


    class ab:
        def __init__(self):
            self.v = id(self)
            print(self.v)


    o = ab()
    print(id(o) == o.v)
