CC := g++
DEBUGOPTS := -Wall -Wextra
RELEASEOPTS :=  -DNDEBUG

# swap commentedness depending on release or debug
#   debugging:
#OPTS := $(DEBUGOPTS) 
#   releasing:
OPTS := $(RELEASEOPTS)

% : %.c
	$(CC) $(OPTS) -o $@ $^

#TODO:  figure out a way to generalize the pattern of only compiled things
#clean: 
#	rm -rf %

all: abss artest getting mem pointtest recursize

abss: abss.c
artest: artest.c
getting: getting.c
mem: mem.c
pointtest: pointtest.c
recursize: recursize.c
