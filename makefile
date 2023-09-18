# Michael Sirna
# 1094947
# 2023-09-10
# CIS2750 Assignment 4 Updated 2

CC = clang
CFLAGS = -Wall -std=c99 -pedantic
INCLUDE = /usr/include/python3.11
LIB = /usr/lib/python3.11/config-3.11-x86_64-linux-gnu

all: _molecule.so

mol.o: mol.c mol.h
	$(CC) $(CFLAGS) -c mol.c -fPIC -o mol.o

libmol.so: mol.o
	$(CC) mol.o -shared -o libmol.so

swig:
	swig -python molecule.i

molecule_wrap.c: molecule.i
	swig -python molecule.i

molecule_wrap.o: swig molecule_wrap.c
	$(CC) $(CFLAGS) -c molecule_wrap.c -fPIC -I$(INCLUDE) -o molecule_wrap.o

_molecule.so: libmol.so molecule_wrap.o
	$(CC) $(CFLAGS) molecule_wrap.o -shared -L. -lmol -L$(LIB) -lmol -dynamiclib -o _molecule.so

clean:
	rm -f *.o *.so
