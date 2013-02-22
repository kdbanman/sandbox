def mylen(l):
    b = []
    for element in l:
        b.append(element)
        
    if b == []:
        return 0
    else:
        b.pop()
        return 1 + mylen(b)