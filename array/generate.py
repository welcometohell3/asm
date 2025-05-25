#!/usr/bin/env python3

import os
import random
import shutil
from jinja2 import Environment, FileSystemLoader

# Конфигурация вариантов (теперь без параметра x)
VARIANTS = [
    {"id": "A", "op": ">", "desc": " > 0"},
    {"id": "B", "op": "<", "desc": " < 0"},
    {"id": "C", "op": "==", "desc": " == 0"},
    {"id": "D", "op": ">=", "desc": " ≥ 0"},
    {"id": "E", "op": "!=", "desc": " ≠ 0"}
]

# Маппинг операторов на ассемблерные мнемоники
OP_MAP = {
    ">": "g",
    "<": "l",
    "==": "e",
    ">=": "ge",
    "<=": "le",
    "!=": "ne"
}

# Инициализация Jinja2
env = Environment(loader=FileSystemLoader("templates"))

def generate_test_data(op, n=5):
    """Генерирует тестовые данные (x всегда 0)"""
    arr = [random.randint(-20, 20) for _ in range(n)]
    filtered = []
    for num in arr:
        if op == ">" and num > 0: filtered.append(num)
        elif op == "<" and num < 0: filtered.append(num)
        elif op == "==" and num == 0: filtered.append(num)
        elif op == ">=" and num >= 0: filtered.append(num)
        elif op == "!=" and num != 0: filtered.append(num)
    return arr, filtered

def generate_variant(variant):
    variant_dir = f"variants/{variant['id']}"
    solution_dir = f"{variant_dir}/solution"
    os.makedirs(solution_dir, exist_ok=True)
    
    # Контекст для шаблонов (без x)
    context = {
        "id": variant["id"],
        "op_asm": OP_MAP[variant["op"]],
        "desc": variant["desc"]
    }
    
    # 1. Копируем библиотеку
    shutil.copy2("lib/simpleio.S", solution_dir)
    
    # 2. Генерируем solution.S
    solution = env.get_template("solution.S.j2")
    with open(f"{solution_dir}/solution.S", "w") as f:
        f.write(solution.render(**context))
    
    # 3. Генерируем Makefile
    makefile = env.get_template("Makefile.j2")
    with open(f"{solution_dir}/Makefile", "w") as f:
        f.write(makefile.render())
    
    # 4. Генерируем statement.xml
    statement = env.get_template("statement.xml.j2")
    with open(f"{variant_dir}/statement.xml", "w") as f:
        f.write(statement.render(**context))
    
    # 5. Генерируем тесты
    tests_dir = f"{variant_dir}/tests"
    os.makedirs(tests_dir, exist_ok=True)
    
    for i in range(1, 6):
        arr, res = generate_test_data(variant["op"])
        
        with open(f"{tests_dir}/{i:03d}.dat", "w") as f:
            f.write(f"{len(arr)}\n" + "\n".join(map(str, arr)))
        
        with open(f"{tests_dir}/{i:03d}.ans", "w") as f:
            f.write("\n".join(map(str, res)) + f"\n{len(res)}\n")

if __name__ == "__main__":
    if os.path.exists("variants"):
        shutil.rmtree("variants")
    os.makedirs("variants")
    
    for variant in VARIANTS:
        generate_variant(variant)
    
    print(f"Сгенерировано {len(VARIANTS)} вариантов в папке variants/")