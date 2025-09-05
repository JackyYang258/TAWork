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
        
        current_indent_len = len(line) - len(line.lstrip())
        
        # 关键停止条件：如果当前行的缩进比基准缩进还要小，
        # 说明我们期望的代码块已经结束了，立即停止处理。
        if current_indent_len < base_indent_len:
            break
        
        # 修正缩进：移除原始的基准缩进，然后添加标准的4个空格缩进
        standard_indent = "    "
        reindented_line = standard_indent + line[base_indent_len:]
        processed_block.append(reindented_line)
            
    # 4. 生成最终结果
    #    将处理好的所有行重新组合成一个字符串
    response_processed = "\n".join(processed_block).rstrip()
    
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
        "name": "场景 2: 移除无关的后续函数",
        "prompt": "def incr_list(l: list):",
        "response": textwrap.dedent("""
          return [i + 1 for i in l]
        def desc_list(l:list):
            return [i - 1 for i in l]
        """).strip()
    },
    {
        "name": "场景 3: 响应包含原始提示",
        "prompt": "def my_func(a, b):",
        "response": textwrap.dedent("""
        def my_func(a, b):
            # 返回两数之和
            return a + b
        """).strip()
    },
    {
        "name": "场景 4: 保持多级缩进的相对结构",
        "prompt": "def process_data(data):",
        "response": textwrap.dedent("""
             results = []
             for item in data:
               if item > 0:
                 results.append(item * 2)
             return results
        """).strip()
    },
    {
        "name": "场景 5: 模型响应为空",
        "prompt": "def do_nothing():",
        "response": "   \n\n   "
    },
    {
        "name": "场景 6: 代码已经格式正确",
        "prompt": "def greet(name):",
        "response": textwrap.dedent("""
            print(f"Hello, {name}!")
            return True
        """).strip()
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