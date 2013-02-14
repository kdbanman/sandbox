#PART 2
def percentSafeGreen(animals):
    
    count = 0
    for animal in animals[1:]:
        parsed = animal.split()
        
        if parsed[0] == 'green' and parsed[3] == 'safe':
            count = count + 1
    return 100*count/(len(animals) - 1)

def percentDangerousRedLarge(animals):
    
    count = 0
    for animal in animals[1:]:
        parsed = animal.split()
        
        if ( parsed[0] == 'red' or parsed[1] == 'large' ) and parsed[3] == 'dangerous':
            count = count + 1
    return 100*count/(len(animals) - 1)


total = 0
green = 0
redDangerous = 0
smallDangerous = 0
safeBrownORRedORSmall = 0

animals = []

animalFile = open('animals.dat')

for line in animalFile:
    animals.append(line)
    
animalFile.close()         

for animal in animals[1:]:
    
    total = total + 1
    
    parsed = animal.split()
    
    if parsed[0] == 'green':
        green = green + 1
    
    if parsed[3] == 'dangerous':
        if parsed[0] == 'red':
            redDangerous = redDangerous + 1
        if parsed[1] == 'small':
            smallDangerous = smallDangerous + 1
    else:
        if parsed[0] == 'brown' or parsed[0] == 'red' or parsed[1] == 'small':
            safeBrownORRedORSmall = safeBrownORRedORSmall + 1

percentSmallDangerous = 100*smallDangerous/total            
            
answer = open('answer.dat','w')            

answer.write('Total number of animals: %d\nTotal number of green animals: %d\nNumber of red animals that are dangerous: %d\nPercentage of animals that are dangerous and small: %5.2f %%\nNumber of safe animals with brown or red color, or small size: %d' % (total, green, redDangerous, percentSmallDangerous, safeBrownORRedORSmall))


#PART 2
print('percent safe and green: %5.2f %%\npercent dangerous and (red or large): %5.2f %%' % (percentSafeGreen(animals), percentDangerousRedLarge(animals)))

answer.close()