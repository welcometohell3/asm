.intel_syntax noprefix
.global main

.section .bss
    .align 8
array: .skip 80  

.section .text
main:
    push rbp
    mov  rbp, rsp
    lea rbx, [rip+array]  
    mov rcx, 10           
    xor rsi, rsi          

fill_loop:
    cmp rsi, rcx
    jge fill_done
    mov rax, rsi          
    mov [rbx + rsi*8], rax  
    inc rsi
    jmp fill_loop

fill_done:
    mov rcx, 10           
    xor rsi, rsi          

print_loop:
    cmp rsi, rcx
    jge print_done
    mov rdi, [rbx + rsi*8]  
    push rsi                
    push rcx                
    call writei64           
    call nl                 
    pop rcx                 
    pop rsi                 
    inc rsi
    jmp print_loop

print_done:
    pop rbp
    call finish             