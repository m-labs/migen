CC := clang
INSTDIR := /usr/local/lib/ivl
INCDIRS := /usr/include/iverilog

OBJ := ipc.o main.o

all: migensim.vpi

%.o: %.c
	$(CC) -fPIC -Wall -O2 -c -I$(INCDIRS) -o $@ $<

migensim.vpi: $(OBJ)
	$(CC) -shared -o $@ $(OBJ) -lvpi

install: migensim.vpi
	install -D -m755  $^ $(INSTDIR)

clean:
	rm -f $(OBJ)
	rm -f migensim.vpi

.PHONY: install clean
