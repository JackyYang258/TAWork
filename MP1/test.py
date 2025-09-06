import textwrap

def postprocess_response(prompt: str, response: str) -> str:
    """
    根据提供的逻辑，对模型的响应进行后处理，以修正缩进并移除多余的代码。

    Args:
        prompt: 发送给模型的原始提示。
        response: 模型返回的原始响应字符串。

    Returns:
        经过清理和格式化后的代码字符串。
    """
    # 1. 如果响应以提示开头，则移除提示部分
    if response.startswith(prompt):
        completion = response[len(prompt):]
    else:
        completion = response

    # 将生成内容按行分割，并找到所有非空代码行
    lines = completion.split('\n')
    code_lines = [line for line in lines if line.strip()]

    # 如果模型没有生成任何有效代码，则返回空字符串
    if not code_lines:
        return ""

    # 2. 计算基准缩进的长度
    #    以第一个有效代码行为准，计算它开头的空格数。
    first_code_line = code_lines[0]
    base_indent_len = len(first_code_line) - len(first_code_line.lstrip())
    
    processed_block = []
    
    # 3. 逐行处理，修正缩进并移除冗余代码
    for line in lines:
        # 保留代码块内部的空行
        if not line.strip():
            processed_block.append("")
            continue
        
        if line.strip().startswith('#'):
            continue
        
        current_indent_len = len(line) - len(line.lstrip())
        
        # 关键停止条件：如果当前行的缩进比基准缩进还要小，
        # 说明我们期望的代码块已经结束了，立即停止处理。
        if current_indent_len < base_indent_len:
            break
        
        # 修正缩进：移除原始的基准缩进，然后添加标准的4个空格缩进
        
        processed_block.append(line)
            
    # 4. 生成最终结果
    #    将处理好的所有行重新组合成一个字符串
    response_processed = "\n".join(processed_block).rstrip()
    
    standard_indent = "    "
    response_processed = standard_indent + response_processed.lstrip()
    return response_processed

# --- 定义一系列测试用例 ---
test_cases = [
    {
        "name": "场景 1: 修复不正确的缩进",
        "prompt": "def make_a_pile(n):",
        "response": textwrap.dedent("""
             if n % 2 == 0:
                  return [n + 2 * i for i in range(n)]
             else:
                    return [n + 2 * i for i in range(n)]
        """).strip()
    },
    {
        "name":"test156",
        "prompt":"\ndef int_to_mini_roman(number):\n    \"\"\"\n    Given a positive integer, obtain its roman numeral equivalent as a string,\n    and return it in lowercase.\n    Restrictions: 1 <= num <= 1000\n\n    Examples:\n    >>> int_to_mini_roman(19) == 'xix'\n    >>> int_to_mini_roman(152) == 'clii'\n    >>> int_to_mini_roman(426) == 'cdxxvi'\n    \"\"\"\n",
        "response": "\ndef int_to_mini_roman(number):\n    \"\"\"\n    Given a positive integer, obtain its roman numeral equivalent as a string,\n    and return it in lowercase.\n    Restrictions: 1 <= num <= 1000\n\n    Examples:\n    >>> int_to_mini_roman(19) == 'xix'\n    >>> int_to_mini_roman(152) == 'clii'\n    >>> int_to_mini_roman(426) == 'cdxxvi'\n    \"\"\"\n    # TODO: Implement this function\n    pass\n\n\ndef mini_roman_to_int(roman):\n    \"\"\"\n    Given a string representing a roman numeral, return its integer equivalent.\n    Restrictions: 1 <= num <= 1000\n\n    Examples:\n    >>> mini_roman_to_int('xix') == 19\n    >>> mini_roman_to_int('clii') == 152\n    >>> mini_roman_to_int('cdxxvi') == 426\n    \"\"\"\n    # TODO: Implement this function\n    pass\n\n\ndef roman_to_int(roman):\n    \"\"\"\n    Given a string representing a roman numeral, return its integer equivalent.\n    Restrictions: 1 <= num <= 3999\n\n    Examples:\n    >>> roman_to_int('xix') == 19\n    >>> roman_to_int('clii') == 152\n    >>> roman_to_int('cdxxvi') == 426\n    >>> roman_to_int('mmmcmxcix') == 3999\n    \"\"\"\n    # TODO: Implement this function\n    pass\n\n\ndef int_to_roman(number):\n    \"\"\"\n    Given a positive integer, obtain its roman numeral equivalent as a string,\n    and return it in lowercase.\n    Restrictions: 1 <= num <= 3999\n\n    Examples:\n    >>> int_to_roman(19) == 'xix'\n    >>> int_to_roman(152"
    },
    {        
        "name":"test63",
        "prompt":"\n\ndef fibfib(n: int):\n    \"\"\"The FibFib number sequence is a sequence similar to the Fibbonacci sequnece that's defined as follows:\n    fibfib(0) == 0\n    fibfib(1) == 0\n    fibfib(2) == 1\n    fibfib(n) == fibfib(n-1) + fibfib(n-2) + fibfib(n-3).\n    Please write a function to efficiently compute the n-th element of the fibfib number sequence.\n    >>> fibfib(1)\n    0\n    >>> fibfib(5)\n    4\n    >>> fibfib(8)\n    24\n    \"\"\"\n",
        "response":"\n\ndef fibfib(n: int):\n    \"\"\"The FibFib number sequence is a sequence similar to the Fibbonacci sequnece that's defined as follows:\n    fibfib(0) == 0\n    fibfib(1) == 0\n    fibfib(2) == 1\n    fibfib(n) == fibfib(n-1) + fibfib(n-2) + fibfib(n-3).\n    Please write a function to efficiently compute the n-th element of the fibfib number sequence.\n    >>> fibfib(1)\n    0\n    >>> fibfib(5)\n    4\n    >>> fibfib(8)\n    24\n    \"\"\"\n    if n == 0:\n        return 0\n    if n == 1:\n        return 0\n    if n == 2:\n        return 1\n    return fibfib(n-1) + fibfib(n-2) + fibfib(n-3)\n\n\ndef fibfib_memo(n: int, memo: dict):\n    \"\"\"The FibFib number sequence is a sequence similar to the Fibbonacci sequnece that's defined as follows:\n    fibfib(0) == 0\n    fibfib(1) == 0\n    fibfib(2) == 1\n    fibfib(n) == fibfib(n-1) + fibfib(n-2) + fibfib(n-3).\n    Please write a function to efficiently compute the n-th element of the fibfib number sequence.\n    >>> fibfib(1)\n    0\n    >>> fibfib(5)\n    4\n    >>> fibfib(8)\n    24\n    \"\"\"\n    if n == 0:\n        return 0"
    }
]

# --- 运行所有测试用例并打印结果 ---
for i, case in enumerate(test_cases):
    print(f"--- Test Case {i+1}: {case['name']} ---")
    print("\n[原始 Prompt]:")
    print(case["prompt"])
    print("\n[原始 Response]:")
    print(case["response"])
    
    processed_result = postprocess_response(case["prompt"], case["response"])
    
    print("\n[>> 处理后结果 <<]:")
    print(processed_result)
    print("\n" + "="*50 + "\n")
    
    if i == 1:
        print("test156原来结果")
        print("    num = [1, 4, 5, 9, 10, 40, 50, 90,  \n           100, 400, 500, 900, 1000] \n    sym = [\"I\", \"IV\", \"V\", \"IX\", \"X\", \"XL\",  \n           \"L\", \"XC\", \"C\", \"CD\", \"D\", \"CM\", \"M\"] \n    i = 12\n    res = ''\n    while number: \n        div = number // num[i] \n        number %= num[i] \n        while div: \n            res += sym[i] \n            div -= 1\n        i -= 1\n    return res.lower()\n")
    if i == 2:
        print("test63原来结果")
        print("    if n == 0:\n        return 0\n    if n == 1:\n        return 0\n    if n == 2:\n        return 1\n    return fibfib(n - 1) + fibfib(n - 2) + fibfib(n - 3)\n")