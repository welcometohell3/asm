CC = gcc
AS = as
CFLAGS = -g -no-pie

all: foo

foo: foo_asm.o foo_c.o
	$(CC) $(CFLAGS) -o foo foo_asm.o foo_c.o

foo_c.o: foo.c
	$(CC) $(CFLAGS) -o foo_c.o -c foo.c

foo_asm.o: foo.S
	$(AS) $(CFLAGS) -o foo_asm.o foo.S

clean:
	rm -f foo foo_asm.o foo_c.o
