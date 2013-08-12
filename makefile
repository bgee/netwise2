CC = gcc
CFLAGS = -std='c99' -shared -I/usr/include/python2.7 -lpython2.7 -o
all: ldModule.so

ldModule.so: ldModule.c
	$(CC) $(CFLAGS) ldModule.so ldModule.c
