.intel_syntax noprefix
.global main

main:
    
    push rbp              
    mov  rbp, rsp         
    push rbx              

    
    mov rax, 0            
    mov rbx, 0            
loop_start:
    cmp rax, 11           
    jge loop_end          
    add rbx, rax          
    inc rax               
    jmp loop_start        
loop_end:
    mov rdi, rbx          
    call writei64         
    call nl               
    
    pop rbx               
    pop rbp               
    call finish           
