.intel_syntax noprefix  
.section .data
    array: .fill 2000, 4, 0  

.section .text
    .global _start

_start:
    
    mov eax, 60         
    xor edi, edi        
    syscall