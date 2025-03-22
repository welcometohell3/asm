CC = gcc
AS = as
CFLAGS = -g -no-pie

all: foo

foo: simpleio.o foo.o
	$(CC) $(CFLAGS) -o foo simpleio.o foo.o

foo.o: foo.S
	$(AS) $(CFLAGS) -o foo.o foo.S
	
simpleio.o: simpleio.S
	$(AS) $(CFLAGS) -o simpleio.o simpleio.S

clean:
	rm -f foo foo.o simpleio.o
