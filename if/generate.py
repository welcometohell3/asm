#!/usr/bin/env python3

import os
import random
import shutil
import tarfile
from jinja2 import Environment, FileSystemLoader

# Конфигурация вариантов
VARIANTS = [
    {"id": "A", "op": ">",  "value": 10, "desc": " &gt; 10"},
    {"id": "B", "op": "<",  "value": 3,  "desc": " &lt; 3"},
    {"id": "C", "op": "==", "value": 7,  "desc": " == 7"},
    {"id": "D", "op": ">=", "value": 5,  "desc": " &gt;= 5"},
    {"id": "E", "op": "!=", "value": 0,  "desc": " != 0"}
]

# Маппинг операторов на ассемблерные мнемоники
OP_MAP = {
    ">": "jg",
    "<": "jl",
    "==": "je",
    ">=": "jge",
    "<=": "jle",
    "!=": "jne"
}

# Инициализация Jinja2
env = Environment(loader=FileSystemLoader("templates"))

def generate_test_data(op, value, n=5):
    """Генерирует тестовые данные и ожидаемый результат"""
    test_cases = [
        value - 1, value, value + 1,
        random.randint(-20, 20),
        0 if value != 0 else 1
    ]
    results = []
    for num in test_cases:
        if op == ">" and num > value: results.append(1)
        elif op == "<" and num < value: results.append(1)
        elif op == "==" and num == value: results.append(1)
        elif op == ">=" and num >= value: results.append(1)
        elif op == "!=" and num != value: results.append(1)
        else: results.append(0)
    return test_cases, results

def generate_variant(variant):
    variant_dir = f"variants/{variant['id']}"
    solution_dir = f"{variant_dir}/solution"
    os.makedirs(solution_dir, exist_ok=True)
    
    # Контекст для шаблонов
    context = {
        "id": variant["id"],
        "op": variant["op"],
        "op_asm": OP_MAP[variant["op"]],
        "value": variant["value"],
        "desc": variant["desc"],
        "example_input": variant["value"] - 1,  # Для примера в statement.xml
        "example_output": 0 if variant["op"] in [">", ">="] else 1
    }
    
    # 1. Копируем библиотеку (если нужна)
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
    
    inputs, outputs = generate_test_data(variant["op"], variant["value"])
    for i, (inp, out) in enumerate(zip(inputs, outputs), 1):
        with open(f"{tests_dir}/{i:03d}.dat", "w") as f:
            f.write(f"{inp}")
        with open(f"{tests_dir}/{i:03d}.ans", "w") as f:
            f.write(f"{out}")

    # 6. Создаем архив solution.tar
    tar_path = os.path.join(variant_dir, "solution.tar")
    with tarfile.open(tar_path, "w") as tar:
        for root, dirs, files in os.walk(solution_dir):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.join("solution", os.path.basename(file))
                tar.add(full_path, arcname=arcname)

if __name__ == "__main__":
    if os.path.exists("variants"):
        shutil.rmtree("variants")
    os.makedirs("variants")
    
    for variant in VARIANTS:
        generate_variant(variant)
    
    print(f"Сгенерировано {len(VARIANTS)} вариантов в папке variants/")