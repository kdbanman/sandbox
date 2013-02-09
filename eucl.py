import sys

def euclid(m,n,prints=False):
    rem = m%n
    if rem == 0:
        if prints:
            print ""
            print n
        return n
    else:
        if prints:
            print rem
        return euclid(n,rem,prints)

if __name__ == "__main__":
    try:
        euclid(int(sys.argv[1]),int(sys.argv[2]),True)
    except ValueError:
        print("you're an asshole")
