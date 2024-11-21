"""
Given a string s, find the length of the longest substring without repeating characters.

Examples:
Input: "ABCBC"
Output: 3
Explanation: The longest substring without repeating characters is “ABC”

Input: "AAA"
Output: 1
Explanation: The longest substring without repeating characters is “A”

Input: "GEEKSFORGEEKS"
Output: 7
Explanation: The longest substrings without repeating characters are “EKSFORG” and “KSFORGE”, with lengths of 7.

"""

# ABCBC
from collections import Counter


def longestUniqueSubstr(sc: str):
    n = len(sc)
    res = 0

    for i in range(n):
        # 初始化
        visited = [False] * 256

        for j in range(i, n):
            # If current character is visited
            # Break the loop
            if visited[ord(sc[j])] == True:
                break
            # Else update the result if this window is larger,
            # and mark current character as visited.
            else:
                res = max(res, j - i + 1)
                visited[ord(sc[j])] = True
    # print(visited)
    # print(len(visited))
    return res


# def longeststr(ss: str):
#     n = len(ss)
#     res = 0
#     for i in range(n):
#         visit = [False] * 256
#         for j in range(i, n):
#             if visit[ord(ss[j])] == True:
#                 break
#             else:
#                 res = max(res, j-i+1)
#                 visit[ord(ss[j])] = True
#
#     return res


def f(ransomNote: str, magazine: str) -> bool:
    s = Counter(ransomNote)
    for a in magazine:
        if s[a] - 1 < 0:
            return False
    return True


def lengthOfLongestSubstring(ss: str):
    n = len(ss)
    char_set = set()
    left = 0
    right = 0
    max_len = 0
    while right < n and left < n:
        # print(f'n={n}')
        if ss[right] not in char_set:
            char_set.add(ss[right])
            max_len = max(max_len, right - left + 1)
            right += 1
            # print(f'right={right}')

        else:
            char_set.remove(ss[left])
            left += 1
            # print(f'left={left}')
        print(char_set)
    return max_len


if __name__ == "__main__":
    s = "geeksforgeeks"
    s = "AAA"
    # s = "GEEKSFORGEEKS"
    # s = "ABCDEFGG"
    # s = ''
    print(lengthOfLongestSubstring(s))
    print(longestUniqueSubstr(s))
    # print(longeststr(s))
    print(f("Hello", "Hellooo"))
