fruits = ['apple', 'banana', 'guava', 'kiwi', 'grape', 'blueberry']

bStart = []
for fruit in fruits:
    if fruit[0] == 'b':
        print(fruit + " starts with the letter 'b'")
        
print("\n")        
        
fiveLetters = []
for fruit in fruits:
    if len(fruit) == 5:
        print(fruit + " has 5 letters")