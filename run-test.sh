#!/bin/bash

if [ $# -lt 1 ]; then
    echo "Использование: $0 <путь_к_варианту> [номера_тестов...]"
    exit 1
fi

variant_dir="$1"
solution_bin="$variant_dir/solution/solution"
tests_dir="$variant_dir/tests"

if [ ! -d "$variant_dir" ]; then
    echo "Ошибка: директория варианта не найдена"
    exit 1
fi

echo "Компиляция решения..."
if ! make -C "$variant_dir/solution" > /dev/null; then
    echo "Ошибка компиляции"
    exit 1
fi

shift
if [ $# -gt 0 ]; then
    tests=()
    for num in "$@"; do
        test_file="$tests_dir/$(printf "%03d.dat" "$num")"
        if [ -f "$test_file" ]; then
            tests+=("$test_file")
        else
            echo "Внимание: тест $num не найден"
        fi
    done
else
    tests=($(ls "$tests_dir"/*.dat 2>/dev/null | sort))
fi

if [ ${#tests[@]} -eq 0 ]; then
    echo "Тесты не найдены"
    exit 0
fi

passed=0
total=${#tests[@]}

echo "Запуск тестов ($total)..."

for test in "${tests[@]}"; do
    test_num=$(basename "$test" .dat)
    answer="${test%.dat}.ans"
    output=$(mktemp)

    timeout 5 "$solution_bin" < "$test" > "$output" 2>&1
    code=$?

    if [ $code -eq 124 ]; then
        echo "Тест $test_num: Время вышло"
    elif [ $code -ne 0 ]; then
        echo "Тест $test_num: Ошибка выполнения (код $code)"
    elif diff -w "$output" "$answer" > /dev/null; then
        echo "Тест $test_num: OK"
        ((passed++))
    else
        echo "Тест $test_num: Ошибка"
    fi

    rm -f "$output"
done

echo "Результат: $passed из $total тестов пройдено"

if [ $passed -eq $total ]; then
    echo "Все тесты успешно пройдены"
    exit 0
else
    echo "Некоторые тесты не прошли"
    exit 1
fi