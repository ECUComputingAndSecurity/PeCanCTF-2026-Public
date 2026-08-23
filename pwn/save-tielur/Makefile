CC=gcc
CFLAGS=-O2 -Wall -Wextra -std=c11

.PHONY: all clean

all: tielur_overflow

tielur_overflow: tielur_overflow.c
	$(CC) $(CFLAGS) tielur_overflow.c -o tielur_overflow

clean:
	rm -f tielur_overflow