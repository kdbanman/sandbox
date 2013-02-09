import sys

def primroot(roots, base, pmod):

    need = set(xrange(1,pmod))

    if base > pmod:
        if len(roots) == 0:
            print "no primitive root\n"
        else:
            print "primitive roots:\n"
            roots.sort()
            for root in roots:
                print root
        quit()

    for t in xrange(pmod-1):
        need.discard((base**t)%pmod)

    if len(need) == 0:
        roots.append(base)
    primroot(roots, base + 1, pmod)


if __name__ == "__main__":
    n = 1
    roots = []
    try:
        primroot(roots, n, int(sys.argv[1]))
    except ValueError:
        print("you're an asshole")
