def fn(n:int) -> int:
    # //递归条件
    if n > 1:
        print(f"fn({n})={n}*f({n-1})")
        return n* fn(n-1)
    #递归结束
    else:
        print(f"f({n})={n}")
        return n


print(f"fn({5})={fn(5)}")