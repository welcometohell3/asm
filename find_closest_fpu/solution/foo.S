.intel_syntax noprefix

.data
    format_input:   .asciz "%lf"
    format_int:     .asciz "%d"
    format_output:  .asciz "%g\n"
    malloc_error:   .asciz "Memory allocation failed\n"
    
    target:        .double 0.0
    closest:       .double 0.0
    size:          .quad   0
    array_ptr:     .quad   0      

.text
.global main

main:
    push rbp
    mov rbp, rsp
    sub rsp, 32                  

    lea rdi, format_int[rip] # размер массива
    lea rsi, size[rip]
    xor eax, eax
    call scanf
    
    mov rcx, [size]
    cmp rcx, 0
    jle invalid_size
    
    mov rax, rcx
    shl rax, 3                   
    mov rdi, rax
    call malloc
    test rax, rax
    jz allocation_failed
    mov [array_ptr], rax         
    
    mov rbx, 0                   
    mov r12, [array_ptr]         
input_loop:
    lea rdi, format_input[rip]
    mov rsi, r12
    xor eax, eax
    call scanf
    
    add r12, 8
    inc rbx
    cmp rbx, [size]
    jl input_loop
    
    lea rdi, format_input[rip] # число
    lea rsi, target[rip]
    xor eax, eax
    call scanf
    
    finit
    fld QWORD PTR target[rip]    
    mov rbx, [array_ptr]         
    mov rcx, [size]              
    
    fld QWORD PTR [rbx]          
    fstp QWORD PTR closest[rip]  
    
find_closest:
    fld QWORD PTR [rbx]          
    fsub st(0), st(1)            
    fabs                         
    
    fld QWORD PTR closest[rip]   
    fsub st(0), st(2)            
    fabs                         
    
    fcomip st(0), st(1)          
    fstp st(0)                   
    jbe next_element             
    
    fld QWORD PTR [rbx]          
    fstp QWORD PTR closest[rip]  
    
next_element:
    add rbx, 8                   
    dec rcx
    jnz find_closest             
    
    fld QWORD PTR closest[rip] # вывод
    sub rsp, 8
    fstp QWORD PTR [rsp]
    movq xmm0, QWORD PTR [rsp]
    add rsp, 8
    
    lea rdi, format_output[rip]
    mov rax, 1
    call printf
    
    mov rdi, [array_ptr]
    call free
    
    xor eax, eax
    leave
    ret
    
invalid_size:
    mov eax, 1
    leave
    ret
    
allocation_failed:
    lea rdi, malloc_error[rip]
    call printf
    mov eax, 1
    leave
    ret