#!/bin/bash

# Проверка наличия аргументов
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <path_to_variant> [test_numbers...]"
    echo "Example 1: $0 tasks/task1/variants/A"
    echo "Example 2: $0 tasks/task1/variants/B 1 3 5"
    exit 1
fi

variant_dir="$1"
solution_bin="$variant_dir/solution/solution"
tests_dir="$variant_dir/tests"

# Проверка существования директории
if [ ! -d "$variant_dir" ]; then
    echo -e "\033[31mError: Variant directory not found\033[0m"
    exit 1
fi

# Компиляция
echo -e "\n\033[34mCompiling solution in $variant_dir\033[0m"
if ! make -C "$variant_dir/solution" > /dev/null; then
    echo -e "\033[31mCompilation failed\033[0m"
    exit 1
fi

# Получаем список тестов
if [ "$#" -gt 1 ]; then
    # Тесты указаны вручную
    shift
    tests=()
    for num in "$@"; do
        test_file=$(printf "$tests_dir/%03d.dat" "$num")
        if [ -f "$test_file" ]; then
            tests+=("$test_file")
        else
            echo -e "\033[33mWarning: Test $num not found\033[0m"
        fi
    done
else
    # Все тесты
    tests=($(ls "$tests_dir"/*.dat 2>/dev/null | sort -V))
fi

if [ ${#tests[@]} -eq 0 ]; then
    echo -e "\033[33mNo tests found in $tests_dir\033[0m"
    exit 0
fi

# Статистика
passed=0
total=${#tests[@]}

echo -e "\n\033[1mTesting variant: $(basename "$variant_dir")\033[0m"
echo -e "Found $total test(s)\n"

for test_file in "${tests[@]}"; do
    test_num=$(basename "$test_file" .dat)
    answer_file="${test_file%.dat}.ans"
    temp_out=$(mktemp)
    
    # Запуск теста с таймаутом (5 секунд)
    timeout 5 "$solution_bin" < "$test_file" > "$temp_out" 2>&1
    exit_code=$?
    
    if [ $exit_code -eq 124 ]; then
        echo -e "\033[31m[TIMEOUT] Test $test_num (5s)\033[0m"
    elif [ $exit_code -ne 0 ]; then
        echo -e "\033[31m[CRASH] Test $test_num (exit code $exit_code)\033[0m"
    elif diff -w -B -Z "$temp_out" "$answer_file" > /dev/null; then
        echo -e "\033[32m[PASS] Test $test_num\033[0m"
        ((passed++))
    else
        echo -e "\033[31m[FAIL] Test $test_num\033[0m"
        echo "Input:"
        cat "$test_file"
        echo -e "\nExpected:"
        cat "$answer_file"
        echo -e "\nGot:"
        cat "$temp_out"
        echo "----------------------"
    fi

    rm -f "$temp_out"
done

# Вывод статистики
echo -e "\n\033[1mResults for $(basename "$variant_dir"):\033[0m"
echo -e "Passed: \033[1m$passed/$total\033[0m"

if [ "$passed" -eq "$total" ]; then
    echo -e "\033[42mALL TESTS PASSED\033[0m"
    exit 0
else
    echo -e "\033[41mSOME TESTS FAILED\033[0m"
    exit $((total - passed))
fi