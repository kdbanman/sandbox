import eucl
import sys

def primes(n,prints=False):
    lprimes = []
    for t in xrange(2,n+1):
        if len(set([eucl.euclid(t,x) for x in xrange(1,t)])) == 1:
            if prints:
                print t
            lprimes.append(t)
    return lprimes

if __name__ == "__main__":
    try:
        primes(int(sys.argv[1]),True)
    except ValueError:
        print("fuck you asshole")
