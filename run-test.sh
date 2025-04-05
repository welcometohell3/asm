#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <test_directory>"
    exit 1
fi

test_dir="$1"
solution_dir="$test_dir/solution"

gcc -g -no-pie "$solution_dir"/*.S -o "$test_dir/task.elf" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Compilation failed"
    exit 1
fi

for i in {1..2}; do
    input_file="$test_dir/input/input$i.txt"
    expected_output="$test_dir/output/output$i.txt"
    temp="$test_dir/task-out$i.txt"

    if [ ! -f "$input_file" ]; then
        echo "Missing input file: $input_file"
        continue
    fi

    "$test_dir/task.elf" < "$input_file" > "$temp"
    if diff -w -B "$expected_output" "$temp"> /dev/null; then
        echo "Test $i passed."
        echo "----------------------"
    else
        echo "Test $i failed!"
        echo "Expected:"
        cat "$expected_output"
        echo -e "\nGot:"
        cat "$temp"
        echo "----------------------"
    fi

    rm -f "$temp"
done