def calculate(s: str) -> int:
    stack = []  # 存储括号前的计算结果和符号
    num = 0  # 当前正在拼接的数字
    res = 0  # 当前层的计算结果
    sign = 1  # 当前数字的符号（1为正，-1为负）

    for c in s:
        # 1. 处理数字：拼接多位数
        if c.isdigit():
            num = num * 10 + int(c)
        # 2. 处理加号：将当前数字和符号累加到结果，重置数字和符号
        elif c == '+':
            res += sign * num
            num = 0
            sign = 1
        # 3. 处理减号：同理，符号设为-1
        elif c == '-':
            res += sign * num
            num = 0
            sign = -1
        # 4. 处理左括号：将当前结果和符号入栈，重置结果和符号（处理括号内的计算）
        elif c == '(':
            stack.append(res)
            stack.append(sign)
            res = 0
            sign = 1
        # 5. 处理右括号：先把括号内最后一个数字累加，再和栈中保存的结果/符号计算
        elif c == ')':
            res += sign * num
            num = 0
            # 弹出括号前的符号和结果，合并计算
            res *= stack.pop()  # 先乘括号前的符号
            res += stack.pop()  # 再加括号前的结果
        # 6. 空格直接跳过
        elif c == ' ':
            continue

    # 处理最后一个数字（表达式末尾没有运算符的情况）
    res += sign * num
    return res


# 测试用例
if __name__ == "__main__":
    print(calculate("1 + 1"))  # 输出 2
    print(calculate(" 2-1 + 2 "))  # 输出 3
    print(calculate("(1+(4+5+2)-3)+(6+8)"))  # 输出 23
    print(calculate("- (3 + (4 + 5))"))  # 输出 -12（测试一元负号）