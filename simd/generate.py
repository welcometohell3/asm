#!/usr/bin/env python3

import os
import tarfile
import shutil
from jinja2 import Environment, FileSystemLoader

# Описание вариантов
ops = [
    {'id': 'A', 'op': '+', 'desc': 'выполняет поэлементное сложение двух массивов'},
    {'id': 'B', 'op': '-', 'desc': 'выполняет поэлементное вычитание второго массива из первого'},
    {'id': 'C', 'op': '*', 'desc': 'выполняет поэлементное умножение двух массивов'},
]

# Jinja2 окружение
env = Environment(loader=FileSystemLoader('templates'))
solution_template = env.get_template('solution.S.j2')
statement_template = env.get_template('statement.xml.j2')
makefile_template = env.get_template('Makefile.j2')

def gen_variant(opdata):
    vid = opdata['id']
    vdir = f'variants/{vid}'
    sdir = f'{vdir}/solution'
    tdir = f'{vdir}/tests'

    os.makedirs(sdir, exist_ok=True)
    os.makedirs(tdir, exist_ok=True)

    # Создание statement.xml
    with open(f'{vdir}/statement.xml', 'w') as f:
        f.write(statement_template.render(id=vid, op=opdata['op'], desc=opdata['desc']))

    # Создание solution.S
    with open(f'{sdir}/solution.S', 'w') as f:
        f.write(solution_template.render(op=opdata['op']))

    # Создание Makefile
    with open(f'{sdir}/Makefile', 'w') as f:
        f.write(makefile_template.render())

    # Пример простого набора тестов
    a = [1, 2, 3, 4]
    b = [5, 6, 7, 8]
    if opdata['op'] == '+':
        c = [x + y for x, y in zip(a, b)]
    elif opdata['op'] == '-':
        c = [x - y for x, y in zip(a, b)]
    elif opdata['op'] == '*':
        c = [x * y for x, y in zip(a, b)]
    else:
        c = [0, 0, 0, 0]

    # Сохраняем тест
    with open(f'{tdir}/001.dat', 'w') as f:
        f.write(" ".join(map(str, a + b + c)))
    with open(f'{tdir}/001.ans', 'w') as f:
        f.write("1")

    # Архив solution.tar
    with tarfile.open(f'{vdir}/solution.tar', 'w') as tar:
        for fname in os.listdir(sdir):
            full_path = os.path.join(sdir, fname)
            tar.add(full_path, arcname=os.path.join('solution', fname))

if __name__ == '__main__':
    if os.path.exists('variants'):
        shutil.rmtree('variants')
    os.makedirs('variants')

    for opdata in ops:
        gen_variant(opdata)

    print(f'Сгенерировано {len(ops)} вариантов в папке variants/')
