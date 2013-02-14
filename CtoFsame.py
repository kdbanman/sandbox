def CtoF(cTemp):
    fTemp = cTemp * 9 / 5 + 32
    return fTemp

def difference(temp):
    separation = temp - CtoF(temp)
    return separation

error = False

while not error:
    
    try:
        guess = int(input('what is your guess? '))
    
        if difference(guess) == 0:
            print('the guess is the same in C and F')
        else:
            print('the guess is not the same in C and F')
            
    except ValueError:
        print('not an integer number')
        error = True
        
    print('\n')
        