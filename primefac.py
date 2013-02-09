import primes
import sys

def primefac(n,prints=False,cumul=[]):
    for p in primes.primes(n):
        if n%p == 0:
            if prints:
                print p
            cumul.append(p)
            if n/p  == 1:
                return cumul
            else:
                return primefac(n/p, prints, cumul)

if __name__ == "__main__":
    if sys.argv[1] == "test":
        try:
            two = primefac(2)
            two.remove(2)
            assert two==[]
            six = primefac(6)
            six.remove(2)
            six.remove(3)
            assert six==[]
        except:
            print "shit's fucked"
    else:
        try:
            primefac(int(sys.argv[1]),True)
        except ValueError:
            print "you're a fucking dick"
