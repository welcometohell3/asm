#!/usr/bin/env python3
import os
import shutil
import tarfile
from jinja2 import Environment, FileSystemLoader

# Варианты операций
VARIANTS = [
    {"id": "A", "op_asm": "vaddps", "desc": "Сложение"},
    {"id": "B", "op_asm": "vmulps", "desc": "Умножение"},
    {"id": "C", "op_asm": "vsubps", "desc": "Вычитание"},
    {"id": "D", "op_asm": "vdivps", "desc": "Деление"},
    {"id": "E", "op_asm": "vmaxps", "desc": "Поиск максимума"}
]

env = Environment(loader=FileSystemLoader("templates"))

def generate_variant(variant):
    variant_dir = f"variants/{variant['id']}"
    solution_dir = f"{variant_dir}/solution"
    os.makedirs(solution_dir, exist_ok=True)

    # Рендерим solution.S
    template_solution = env.get_template("solution.S.j2")
    with open(f"{solution_dir}/solution.S", "w") as f:
        f.write(template_solution.render(**variant))

    # Рендерим statement.xml в папке варианта (не в solution/)
    template_statement = env.get_template("statement.xml.j2")
    with open(f"{variant_dir}/statement.xml", "w") as f:
        f.write(template_statement.render(**variant))

    # Makefile
    with open(f"{solution_dir}/Makefile", "w") as f:
        f.write("all: solution\n\nsolution: solution.S \n\tgcc -o $@ $^ -no-pie -mavx\n")

    # Архив solution.tar
    with tarfile.open(f"{variant_dir}/solution.tar", "w") as tar:
        tar.add(f"{solution_dir}/solution.S", arcname="solution/solution.S")
        tar.add(f"{solution_dir}/Makefile", arcname="solution/Makefile")
        tar.add(f"{variant_dir}/statement.xml", arcname="solution/statement.xml")  # Добавляем statement.xml в архив под solution/


if __name__ == "__main__":
    if os.path.exists("variants"):
        shutil.rmtree("variants")
    os.makedirs("variants")

    for variant in VARIANTS:
        generate_variant(variant)

    print(f"Сгенерировано {len(VARIANTS)} вариантов в папке variants/")
