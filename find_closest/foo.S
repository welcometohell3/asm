.intel_syntax noprefix
.data
    array:  .double 1.2, 3.4, 5.6, 7.8, 9.0 
    target: .double 6 
    size:   .quad   5                         
    closest: .double 0.0                      
    format: .asciz  "Closest number: %lf\n"   
.text
.global main
main:
    finit
    fld QWORD PTR target[rip]       
    lea rbx, array[rip]
    mov rcx, QWORD PTR size[rip]
    fld QWORD PTR [rbx] #загружаем первый элемент
    fstp QWORD PTR closest[rip] #сохраняем первый элемент
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
    loop find_closest          
    fld QWORD PTR closest[rip] 
    sub rsp, 8                 
    fstp QWORD PTR [rsp]       
    movq xmm0, QWORD PTR [rsp] 
    lea rdi, format[rip]       
    mov rax, 1                 
    call printf                
    add rsp, 8                     
    syscall