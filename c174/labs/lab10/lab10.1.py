def surNames(filename):
    import string
    
    punct = set(string.punctuation)
    
    
    file = open(filename)
    
    freq = {}
    for line in file:
        
        splitLine = line.split(',')
        i = 0
        while i < len(splitLine):
            splitLine[i] = splitLine[i].strip()
            i = i + 1
            
        if len(splitLine) == 2:
            if len((set(splitLine[0]).union(set(splitLine[1]))).intersection(punct)) == 0:
                if splitLine[0] in freq:
                    freq[splitLine[0]] = freq[splitLine[0]] + 1
                else:
                    freq[splitLine[0]] = 1
                
            
    return freq

def mode(d):
    
    parallel = {}
    highest = 0
    for k,v in d.items():
        
        if v in parallel:
            parallel[v].append(k)
        else:
            parallel[v] = [k]
            
        if v > highest:
            highest = v
    return parallel[highest]

filename = input('name of file? ')

print(mode(surNames(filename)))