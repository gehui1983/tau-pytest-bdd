import itertools
import sys
import time

from common.Log4test import Log4test
from typing import List

LOGGER = Log4test()


# from qtpy.QtWidgets import QApplication, QLabel, QPushButton
#
# app = QApplication([])
# hello = QLabel("Hello, World!")
# hello.setWindowTitle('My First PyQt Application')
# hello.show()
# # button = QPushButton("Click me!")
# # button.clicked.connect(lambda: hello.setText("Hello, PyQt!"))
# # button.show()
# app.exec_()
# import math


def twoSum(nums: List[int], target: int) -> List[int]:
    res = list()
    for i in range(0, len(nums)):
        diff = target - nums[i]
        for j in range(i + 1, len(nums)):
            if nums[j] == diff:
                res.append(i)
                res.append(j)
    return res


# if __name__ == '__main__':
#     nums = twoSum([1, 2, 0, 5, 3], 4)
#     print(nums)
#
#     cookie = '''gfkadpd=2631,22740; s_v_web_id=verify_m52arvsg_vH2eoiND_VspF_48bI_ByZb_piLgImqadqBl; passport_csrf_token=123e1557e047eaa939af301781d81a62; passport_csrf_token_default=123e1557e047eaa939af301781d81a62; ttwid=1%7CIA6afkepGpD2f1dvRzgenrBI13tIZTbcYsyf9kUheM8%7C1735034580%7Cfb3d6ded6fd58c210f976fe03acb4e19a91e3db095213fbbadbd035ac9092ddc; uid_tt=1717e809e702e47e5cc24fc5fed8a668; uid_tt_ss=1717e809e702e47e5cc24fc5fed8a668; sid_tt=d1d47c7811689c0167956d0842dde65c; sessionid=d1d47c7811689c0167956d0842dde65c; sessionid_ss=d1d47c7811689c0167956d0842dde65c; is_staff_user=false; store-region=cn-zj; store-region-src=uid; odin_tt=10cecf85e3efb853e39d0621cd29af5027f50c7ae96e60b884166b6108736e7e304fdda27e463d3fb2d0cb51d67c01a9da1a2d98869aeb6f9522fb8616554bb6; ucas_c0_buyin=CkEKBTEuMC4wELKIipa32qG1Zxi9LyDgmYCv0Yy7AiiPETCt_cDa-ozhB0DXjaq7BkjXwea9BlCovK2KqcPAqGNYfhIUKKQjR7NAIaueXVcoStVPiXGOaQU; ucas_c0_ss_buyin=CkEKBTEuMC4wELKIipa32qG1Zxi9LyDgmYCv0Yy7AiiPETCt_cDa-ozhB0DXjaq7BkjXwea9BlCovK2KqcPAqGNYfhIUKKQjR7NAIaueXVcoStVPiXGOaQU; sid_guard=d1d47c7811689c0167956d0842dde65c%7C1735034584%7C5183999%7CSat%2C+22-Feb-2025+10%3A03%3A03+GMT; sid_ucp_v1=1.0.0-KDc3MTQ5MTljYzFhN2E1ZmIyN2E0NTI3ZGQ1NWFjODhiOTBmYzk4MzIKGAit_cDa-ozhBxDYjaq7BhiPESAMOAhAJhoCbGYiIGQxZDQ3Yzc4MTE2ODljMDE2Nzk1NmQwODQyZGRlNjVj; ssid_ucp_v1=1.0.0-KDc3MTQ5MTljYzFhN2E1ZmIyN2E0NTI3ZGQ1NWFjODhiOTBmYzk4MzIKGAit_cDa-ozhBxDYjaq7BhiPESAMOAhAJhoCbGYiIGQxZDQ3Yzc4MTE2ODljMDE2Nzk1NmQwODQyZGRlNjVj; SASID=SID2_7451913467422146867; BUYIN_SASID=SID2_7451913467422146867; buyin_shop_type=24; buyin_account_child_type=1128; buyin_app_id=1128; buyin_shop_type_v2=24; buyin_account_child_type_v2=1128; buyin_app_id_v2=1128; x-web-secsdk-uid=fd89876d-5a32-4010-a3f4-920c853dc225; _tea_utm_cache_3813=undefined; scmVer=1.0.1.8354; csrf_session_id=ccc3aff7fe928c1bc25e0f46c77aca02'''
#     arr = cookie.split("; ")
#     d = dict()
#     for a in arr:
#         print(files"key={a.split('=')[0]}----value={a.split('=')[1]}")
#         d.setdefault(a.split('=')[0], {a.split('=')[1]})
#     print(d)


# class Solution:
#     def minimumOperations(self, nums: List[int]) -> int:
#         count = 0
#         arr_len = len(nums)
#         for i in range(0, arr_len, 3):
#             temp = nums[i:arr_len]
#             sets = set(temp)
#             if len(temp) == len(sets):
#                 break
#             else:
#                 count += 1
#         return count


# class Solution:
#     def maxDistinctElements(self, nums: List[int], k: int) -> int:
#         if k > 0:
#             maxa = k
#             mini = 0 - k
#         else:
#             maxa = 0 - k
#             mini = k
#         addition = [i for i in range(mini, maxa + 1) if i != 0]
#         addition_len = len(addition)
#         nums = sorted(nums)
#         nums_len = len(nums)
#         count = 0
#         sets = set(nums)
#
#         res = list()
#         if nums_len == len(sets):
#             count = nums_len
#         else:
#             i = 0
#             j = 0
#             while i < addition_len:
#                 temp = list()
#                 while j < min(addition_len, nums_len):
#                     temp.append(addition[i + j] + nums[j])
#                     j += 1
#                 i += 1
#                 res.append(len(set(temp)))
#             count = max(res)
#
#         return count
#
#
# if __name__ == '__main__':
#     so = Solution()
#     n = so.maxDistinctElements([1, 2, 2, 3, 3, 4], 2)
#     print(n)

# import itertools
#
#
# # 利用itertools库中的permutations函数,给定一个排列,输出他的全排列
# def allPermutation(n):
#     permutation = []
#     # 首先需要初始化一个1-n的排列
#     for i in range(n):
#         permutation.append(i + 1)
#     # itertools.permutations返回的只是一个对象,需要将其转化成list
#     # 每一种排列情况以元组类型存储
#     all_permutation = list(itertools.permutations(permutation))
#     return all_permutation
#
#
# al = allPermutation(4)
# print(al)
# print(len(al))

s = []


def permutation(nums: List[int], index: int, length: int):
    if index == length:
        # 这里使用 list(nums)是因为如果直接添加 添加的都是指向nums所存数组的地址 nums变化了 s里面的数组内容也会跟着变化。
        s.append(list(nums))
    else:
        for i in range(index, length):
            nums[i], nums[index] = nums[index], nums[i]
            permutation(nums, index + 1, length)
            nums[i], nums[index] = nums[index], nums[i]


# s = []
# nums = [i for i in range(1, 4)]
# permutation(nums, 0, len(nums))
# LOGGER.info(s)
#
# nu = itertools.product(nums, repeat=3)
# rs = list()
# for n in nu:
#     LOGGER.info(n)
#     rs.append(list(n))
#
# print(rs)
# print(len(rs))


def maxLetters(nums: List[int], k: int):
    if len(nums) == len(set(nums)):
        return len(nums)
    if len(nums) <= 2 * k:
        return len(nums)
    r = []
    for i in range(0 - k, k + 1):
        r.append(i)
    length = len(nums)
    p = itertools.product(r, repeat=length)
    print(type(p))
    max_i = 0
    for j in p:
        s = list(j)
        for l in range(0, length):
            s[l] += nums[l]
        if len(set(s)) > max_i:
            max_i = len(set(s))
            if max_i == length:
                break
    return max_i


def maxLetter(lis: List[int], k: int):
    lis = sorted(lis)
    ans = 0
    l = -(2 ** 63)
    for x in lis:
        x = min(max(x - k, l + 1), x + k)
        LOGGER.info(x)
        if x > l:
            ans += 1
            l = x

    return ans


if __name__ == '__main__':
    before = int(time.time())
    LOGGER.info(maxLetter([9, 10, 10, 10, 10, 10, 10, 10, 10], 3))
    after = int(time.time())
    print(after - before)
