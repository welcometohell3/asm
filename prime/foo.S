.intel_syntax noprefix
.global main

.bss
    .align 8
num:    .skip 8 

.text
main:
    call readi64    
    mov qword ptr num[rip], rax 

    mov rdi, qword ptr num[rip]
    cmp rdi, 1
    je not_prime
    cmp rdi, 2
    je is_prime

    mov rsi, 2
loop_check:
    xor rdx, rdx
    mov rax, qword ptr num[rip]
    div rsi
    cmp rdx, 0
    je not_prime  # Если делится нацело

    mov rax, rsi
    mul rsi
    cmp rax, qword ptr num[rip]
    jg is_prime  # Если rsi^2 > num, значит число простое

    inc rsi
    jmp loop_check

not_prime:
    mov rdi, 0
    call writei64
    call nl
    jmp exit

is_prime:
    mov rdi, 1
    call writei64
    call nl

exit:
    call finish
