rev:=$(shell git log --pretty=format:'%h' -n 1)

.PHONY: clean
DEPS = hosts.cpp hosts.h

all: tophosts

tophosts: main.o hosts.o
	$(CXX) $(LDFLAGS) $^ $(shell pkg-config libcap_utils-0.7 --libs) -lssl -lcrypto -lrt -lsqlite3 -o $@

%.o: %.cpp Makefile $(DEPS)
	$(CXX) $(CFLAGS) -Wall -std=c++0x $(shell pkg-config libcap_utils-0.7 --cflags) -c $< -o $@

clean:
	rm -rf tophosts *.o tophosts-*.tar.gz

dist:	owd-$(rev).tar.gz

install: all
	install -m 0755 oneway $(PREFIX)/bin

tophosts-$(rev).tar.gz:
	git archive --prefix=owd-$(rev)/ -o tophosts-$(rev).tar.gz master

main.cpp: hosts.cpp
