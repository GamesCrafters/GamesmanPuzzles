CC = gcc # C compiler
BIN = bin

install:
	$(CC) -fpic -shared -o libsolver.so \
		src/Solver.c
	mv -f libsolver.so $(BIN)/libsolver.so	