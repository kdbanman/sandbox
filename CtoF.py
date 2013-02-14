
def CtoF(cTemp):
    fTemp = cTemp * 9 / 5 + 32
    return fTemp

testTemp = '-273.15'
error = False

while error == False:
    try:
        testTemp = float(input('temperature in C? '))
        fahrenheit = CtoF(testTemp)
        print('%5.2f celsius is %5.2f fahrenheit' % (testTemp, fahrenheit))
    except ValueError:
        print('NOT A NUMBER, ASSHOLE.')
        error = True
        
    print('\n')