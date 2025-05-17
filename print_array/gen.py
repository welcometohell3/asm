import os
import random
from jinja2 import Environment, FileSystemLoader

TASK_VARIANTS = [
    {
        "id": "A",
        "title": "Вывод массива",
        "description": "Выведите n целых чисел в том порядке, как они были введены.",
        "input_description": "На вход подаётся число n - размер массива, затем n целых чисел.",
        "output_description": "Выведите n чисел по одному в строке.",
        "code_goal": "печать массива",
        "function": lambda arr: arr,
    },
    {
        "id": "B",
        "title": "Сумма массива",
        "description": "Найдите сумму n целых чисел.",
        "input_description": "На вход подаётся число n - размер массива, затем n целых чисел.",
        "output_description": "Выведите сумму этих чисел.",
        "code_goal": "нахождение суммы",
        "function": lambda arr: [sum(arr)],
    },
    {
        "id": "C",
        "title": "Максимум в массиве",
        "description": "Найдите максимальное число среди n целых чисел.",
        "input_description": "На вход подаётся число n, затем n целых чисел.",
        "output_description": "Выведите максимальное из этих чисел.",
        "code_goal": "поиск максимума",
        "function": lambda arr: [max(arr)],
    },
    {
        "id": "D",
        "title": "Количество чётных чисел",
        "description": "Определите количество чётных чисел среди введённых.",
        "input_description": "На вход подаётся число n, затем n целых чисел.",
        "output_description": "Выведите количество чётных чисел.",
        "code_goal": "подсчёт чётных",
        "function": lambda arr: [sum(1 for x in arr if x % 2 == 0)],
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
        n = random.randint(3, 8)
        arr = [random.randint(-50, 50) for _ in range(n)]
        input_str = f"{n}\n" + "\n".join(map(str, arr))
        output_str = "\n".join(map(str, task["function"](arr)))
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