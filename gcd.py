import sys

def gcd(x,y): # 0 <= x   1 <= y
    if x == 0:
        print ' = ',y
        return y
    else:
        print ' = gcd(', y%x, x, ')'
        return gcd(y%x,x)

if __name__ == "__main__":
	gcd(int(sys.argv[1]), int(sys.argv[2]))
