from typing import List, Any


def merge_sort(lst: List[int]):
    if len(lst) <= 1:
        return lst
    mid = len(lst) // 2
    left = merge_sort(lst[:mid])
    print(left)
    right = merge_sort(lst[mid:])
    print(right)
    return merge(left, right)


def merge(left: List[int], right: List[int]):
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


if __name__ == '__main__':
    lst = [10, 8, 9, 11, 23, 1, 3]

    print(merge_sort(lst))
