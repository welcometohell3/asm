.intel_syntax noprefix
.global main
.section .data
input_fmt: .asciz "%lld"
is_prime_msg: .asciz "prime\n"
not_prime_msg: .asciz "not prime\n"
num: .quad 0

.text
main:
    push rbp
    mov rbp, rsp

    lea rdi, [rip + input_fmt]
    lea rsi, [rip + num]
    xor eax, eax
    call scanf

    mov rdi, [rip + num]
    cmp rdi, 1
    je not_prime
    cmp rdi, 2
    je is_prime

    mov rsi, 2
loop_check:
    xor rdx, rdx
    mov rax, [rip + num]
    div rsi
    cmp rdx, 0
    je not_prime

    mov rax, rsi
    mul rsi
    cmp rax, [rip + num]
    jg is_prime

    inc rsi
    jmp loop_check

not_prime:
    lea rdi, [rip + not_prime_msg]
    call printf
    jmp exit

is_prime:
    lea rdi, [rip + is_prime_msg]
    call printf

exit:
    xor eax, eax
    mov rsp, rbp
    pop rbp
    ret
