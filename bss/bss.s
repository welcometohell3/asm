.intel_syntax noprefix  
.section .bss
    .lcomm array, 8000  

.section .text
    .global _start

_start:
    mov eax, 60         
    xor edi, edi        
    syscallcl