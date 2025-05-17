import os
import random
from jinja2 import Environment, FileSystemLoader

TASK_VARIANTS = [
    {
        "id": "E",
        "title": "Проверка на простое число",
        "description": "Определите, является ли число простым.",
        "input_description": "На вход подаётся одно целое положительное число.",
        "output_description": "Выведите \"prime\", если число простое, иначе \"not prime\".",
        "code_goal": "проверка на простое",
        "function": lambda n: "prime" if n > 1 and all(n % i != 0 for i in range(2, int(n**0.5)+1)) else "not prime",
    },
    {
        "id": "F",
        "title": "Проверка на чётность",
        "description": "Определите, является ли число чётным.",
        "input_description": "На вход подаётся одно целое число.",
        "output_description": "Выведите \"even\", если число чётное, иначе \"odd\".",
        "code_goal": "проверка на чётность",
        "function": lambda n: "even" if n % 2 == 0 else "odd",
    },
    {
        "id": "G",
        "title": "Проверка делимости на 3 и 5",
        "description": "Определите, делится ли число на 3 и на 5 одновременно.",
        "input_description": "На вход подаётся одно целое число.",
        "output_description": "Выведите \"yes\", если число делится и на 3, и на 5. Иначе \"no\".",
        "code_goal": "проверка делимости",
        "function": lambda n: "yes" if n % 3 == 0 and n % 5 == 0 else "no",
    },
    {
        "id": "H",
        "title": "Проверка на полный квадрат",
        "description": "Определите, является ли число полным квадратом.",
        "input_description": "На вход подаётся одно неотрицательное целое число.",
        "output_description": "Выведите \"perfect square\", если число является квадратом целого, иначе \"not perfect square\".",
        "code_goal": "проверка квадрата",
        "function": lambda n: "perfect square" if int(n**0.5)**2 == n else "not perfect square",
    },
]

env = Environment(loader=FileSystemLoader("."))
statement_template = env.get_template("statement.xml")


def generate_task_variant(task):
    base_dir = f"generated/{task['id']}"
    tests_dir = os.path.join(base_dir, "tests")
    os.makedirs(tests_dir, exist_ok=True)

    examples = []
    for i in range(10):
        n = random.randint(1, 100)
        input_str = str(n)
        output_str = task["function"](n)

        examples.append({"input": input_str, "output": output_str})

        test_id = f"{i+1:03d}"
        with open(os.path.join(tests_dir, f"{test_id}.dat"), "w") as f_in:
            f_in.write(input_str)
        with open(os.path.join(tests_dir, f"{test_id}.ans"), "w") as f_out:
            f_out.write(output_str)
    with open(os.path.join(base_dir, "statement.xml"), "w", encoding="utf-8") as f_stat:
        f_stat.write(statement_template.render(task=task, examples=examples))

for task in TASK_VARIANTS:
    generate_task_variant(task)