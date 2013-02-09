import sys

fibmemo = {}
fibmemo[1] = 1
fibmemo[2] = 1

def fib(n):
	assert n >= 1, 'undefined for n < 1'
	if n not in fibmemo:
		fibmemo[n] = fib(n - 1) + fib(n - 2)
	return_val = fibmemo[n]
	return return_val

if __name__ == '__main__':
	try:
		N = int(sys.argv[1])
		nth_fib = fib(N)
	except ValueError or AssertionError:
		print('positive integers, bitch')
		quit()
	print(nth_fib)
