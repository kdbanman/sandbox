
import random

def CtoF(cTemp):
    fTemp = cTemp * 9 / 5 + 32
    return fTemp

def difference(temp):
    separation = temp - CtoF(temp)
    return separation


guess = random.randrange(-1000000,1000000)
deltaLower = 0
deltaUpper = 0


while difference(guess) >= 0:
    guess = random.randrange(-1000000,1000000)
    
lowerGuess = guess

while difference(guess) <= 0:
    guess = random.randrange(-1000000,1000000)
    
    
upperGuess = guess

deltaLower = difference(lowerGuess)
deltaUpper = difference(upperGuess)


while difference(int(lowerGuess)) != 0:
    
    print(str(lowerGuess) + '   ' + str(upperGuess))
    
    interval = (upperGuess - lowerGuess) / 2
    
    if abs(deltaLower) < abs(deltaUpper):
        upperGuess = upperGuess - interval
        deltaUpper = difference(upperGuess)
    else:
        lowerGuess = lowerGuess + interval
        deltaLower = difference(lowerGuess)

print('whole number equivalence found at %d' % (lowerGuess))
    