CC = gcc
AS = as

CFLAGS = -g -no-pie

all: solution

solution: solution.o
	$(CC) $(CFLAGS) -o solution solution.o

solution.o: solution.S
	$(AS) $(CFLAGS) -c -o solution.o solution.S
	
clean:
	rm -f solution solution.o