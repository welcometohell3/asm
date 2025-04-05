.intel_syntax noprefix
.global main
.section .note.GNU-stack, "", @progbits  

.bss
    .align 8
num:    .skip 8

.text
main:
    push rbp                  
    mov rbp, rsp              

    lea rdi, input_fmt        
    lea rsi, num              
    xor eax, eax              
    call scanf                

    mov rdi, [num]            
    cmp rdi, 1                
    je not_prime              
    cmp rdi, 2                
    je is_prime               

    mov rsi, 2                
loop_check:
    xor rdx, rdx              
    mov rax, [num]            
    div rsi                   
    cmp rdx, 0                
    je not_prime              

    mov rax, rsi              
    mul rsi                   
    cmp rax, [num]            
    jg is_prime               

    inc rsi                   
    jmp loop_check            

not_prime:
    lea rdi, not_prime_msg    
    call printf               
    jmp exit                  

is_prime:
    lea rdi, is_prime_msg     
    call printf               

exit:
    xor eax, eax              
    mov rsp, rbp              
    pop rbp                   
    ret                       

.section .data
input_fmt: .asciz "%lld"         
is_prime_msg: .asciz "prime\n"   
not_prime_msg: .asciz "not prime\n"