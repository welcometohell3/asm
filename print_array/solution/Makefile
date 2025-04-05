CC = gcc
AS = as

CFLAGS = -g -no-pie

all: foo

foo: foo.o
	$(CC) $(CFLAGS) -o foo foo.o

foo.o: foo.S
	$(AS) $(CFLAGS) -c -o foo.o foo.S
	
clean:
	rm -f foo foo.o