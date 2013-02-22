def fib(N):
    if N == 0:
        return 0
    if N == 1:
        return 1
    else:
        return fib(N-1) + fib(N-2)

#assuming 0 is the 'zeroth' fibonacci number, this returns the (i+1)th fibonacci number    
number = int(input('input:' )) + 1
print(fib(number))