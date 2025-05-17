.intel_syntax noprefix

.data
    format_int:     .asciz "%d"
    output_format:  .asciz "%d\n" 
    newline:        .asciz "\n"
    array:          .skip 400   

.text
.global main

main:
    push rbp
    mov rbp, rsp
    sub rsp, 32

    
    lea rdi, format_int[rip]
    lea rsi, [rbp-4]
    xor eax, eax
    call scanf
    mov r12d, [rbp-4]

    test r12d, r12d
    jle exit_error
    cmp r12d, 100
    jg exit_error

    lea rbx, array[rip]
    xor r13d, r13d
read_loop:
    cmp r13d, r12d
    jge read_done

    lea rdi, format_int[rip]
    mov rsi, rbx
    xor eax, eax
    call scanf
    cmp eax, 1
    jne exit_error

    add rbx, 4
    inc r13d
    jmp read_loop

read_done:
    lea rbx, array[rip]
    xor r13d, r13d
print_loop:
    cmp r13d, r12d
    jge print_done

    mov esi, [rbx]
    lea rdi, output_format[rip]  
    xor eax, eax
    call printf

    add rbx, 4
    inc r13d
    jmp print_loop

print_done:
    xor eax, eax
    leave
    ret

exit_error:
    mov eax, 1
    leave
    ret