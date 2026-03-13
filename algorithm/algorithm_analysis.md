# 数学表达式计算算法分析

## 1. 算法功能概述
该算法实现了一个基本的数学表达式计算器，支持：
- 整数的加减运算
- 括号优先级处理
- 空格忽略
- 一元负号处理（如 "- (3 + 4)"）

## 2. 核心设计思路
采用**栈**数据结构来处理括号优先级，通过**状态机**思想遍历字符串字符进行计算：

### 关键变量
- `stack`: 存储括号前的计算结果和符号
- `num`: 拼接当前处理的多位数
- `res`: 当前层（括号内/外）的计算结果
- `sign`: 当前数字的符号（1 为正，-1 为负）

### 处理流程
1. **遍历字符串**：逐个字符处理
2. **数字处理**：拼接多位数（如 "123" → 1*10+2=12 → 12*10+3=123）
3. **运算符处理**：
   - `+`: 将当前数字和符号累加到结果，重置数字和符号
   - `-`: 同理，符号设为 -1
4. **括号处理**：
   - `(`: 将当前结果和符号入栈，重置结果和符号（进入括号内层计算）
   - `)`: 先完成括号内最后一次计算，再与栈中保存的外层结果/符号合并
5. **空格处理**：直接跳过
6. **结束处理**：处理表达式末尾的数字

## 3. 时间复杂度分析
- **时间复杂度**: O(n)，其中 n 是字符串长度
  - 每个字符只被遍历一次
  - 栈的操作（push/pop）都是 O(1) 时间

## 4. 空间复杂度分析
- **空间复杂度**: O(n)，最坏情况需要存储所有字符
  - 当表达式包含嵌套括号时，栈的深度最大为括号嵌套层数
  - 平均情况下空间复杂度为 O(1)

## 5. 算法优缺点

### 优点
1. **简洁高效**: 仅使用栈和几个变量，避免了复杂的表达式树构建
2. **正确性**: 正确处理了运算符优先级和括号嵌套
3. **鲁棒性**: 能处理空格和一元负号等边界情况
4. **内存友好**: 空间复杂度低，适合处理大型表达式

### 缺点
1. **功能受限**: 仅支持加减运算，不支持乘除、幂运算等
2. **错误处理**: 缺乏对非法表达式的验证（如括号不匹配、无效字符等）
3. **浮点数支持**: 目前只支持整数运算
4. **扩展性差**: 添加新运算符需要修改核心逻辑

## 6. 代码优化建议

### 优化1：支持乘除运算
```python
def calculate(s: str) -> int:
    stack = []
    num = 0
    sign = '+'  # 使用字符表示运算符
    s = s.replace(' ', '')  # 预处理去除空格
    
    for i, c in enumerate(s):
        if c.isdigit():
            num = num * 10 + int(c)
        if i == len(s) - 1 or c in '+-*/()':
            if sign == '+':
                stack.append(num)
            elif sign == '-':
                stack.append(-num)
            elif sign == '*':
                stack.append(stack.pop() * num)
            elif sign == '/':
                # 整数除法处理
                stack.append(int(stack.pop() / num))
            
            if c == '(':
                stack.append(sign)
                sign = '+'
                num = 0
            elif c == ')':
                # 计算括号内结果
                temp = 0
                while isinstance(stack[-1], int):
                    temp += stack.pop()
                stack[-1] = temp * stack[-1]  # 乘以前面的符号
                num = 0
            else:
                sign = c
                num = 0
    
    return sum(stack)
```

### 优化2：添加错误处理
```python
def calculate(s: str) -> int:
    stack = []
    num = 0
    res = 0
    sign = 1
    bracket_count = 0
    
    for c in s:
        if c.isdigit():
            num = num * 10 + int(c)
        elif c in '+-()':
            res += sign * num
            num = 0
            
            if c == '(':
                stack.append(res)
                stack.append(sign)
                res = 0
                sign = 1
                bracket_count += 1
            elif c == ')':
                if bracket_count == 0:
                    raise ValueError("括号不匹配：右括号过多")
                res *= stack.pop()
                res += stack.pop()
                bracket_count -= 1
            elif c == '+':
                sign = 1
            elif c == '-':
                sign = -1
        elif c != ' ':
            raise ValueError(f"无效字符：{c}")
    
    if bracket_count > 0:
        raise ValueError("括号不匹配：左括号过多")
    
    res += sign * num
    return res
```

### 优化3：支持浮点数运算
```python
def calculate(s: str) -> float:
    stack = []
    num = 0.0
    decimal = False
    decimal_place = 0.1
    res = 0.0
    sign = 1
    
    for c in s:
        if c.isdigit():
            if decimal:
                num += int(c) * decimal_place
                decimal_place *= 0.1
            else:
                num = num * 10 + int(c)
        elif c == '.':
            if decimal:
                raise ValueError("无效表达式：多个小数点")
            decimal = True
        elif c in '+-()':
            res += sign * num
            num = 0.0
            decimal = False
            decimal_place = 0.1
            
            if c == '(':
                stack.append(res)
                stack.append(sign)
                res = 0.0
                sign = 1
            elif c == ')':
                res *= stack.pop()
                res += stack.pop()
            elif c == '+':
                sign = 1
            elif c == '-':
                sign = -1
        elif c != ' ':
            raise ValueError(f"无效字符：{c}")
    
    res += sign * num
    return res
```

## 7. 测试用例分析
原算法的测试用例覆盖了：
- 基本加减运算："1 + 1" → 2
- 带空格的表达式：" 2-1 + 2 " → 3
- 复杂括号嵌套："(1+(4+5+2)-3)+(6+8)" → 23
- 一元负号："- (3 + (4 + 5))" → -12

这些测试用例验证了算法在各种场景下的正确性。

## 8. 算法应用场景
该算法适用于：
- 简单计算器应用
- 配置文件中的表达式解析
- 基本的数学表达式求值场景

## 9. 总结
该算法是一个**高效简洁**的数学表达式计算器实现，通过栈巧妙处理了括号优先级，时间复杂度为 O(n)，空间复杂度为 O(n)。虽然功能相对基础，但设计思路清晰，是学习栈数据结构应用和状态机思想的良好范例。通过扩展可以支持更复杂的运算和错误处理。