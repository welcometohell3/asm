.intel_syntax noprefix

.global asm_foo  

asm_foo:
    
    push rbp          
    mov rbp, rsp      
    push rbx          
    push r12
    push r13
    push r14
    push r15

    mov r15, 0
    add r15, rdi      
    add r15, rsi     
    add r15, rdx      
    add r15, rcx       
    add r15, r8       
    add r15, r9    
    add r15, [rbp+16]      
    add r15, [rbp+24]   

    mov rdi, 9
    mov rsi, 10
    call c_foo
    mov r14, rax

    add r15, r14 
    mov rax, r15 

    pop r15           
    pop r14
    pop r13
    pop r12
    pop rbx
    mov rsp, rbp      
    pop rbp           
    ret               