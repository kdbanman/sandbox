def f(x,y):
    x = x + 1
    return x * y

def g(x, y):
    z = x + y
    prod = f(z, z)
    return prod

def h(x,y,z):
    w = y + z
    v = g(x, w)**2
    return v

x = 1
y = x + 1
print(h(x, y+3, x+y))