# greeting
print("Welcome to Hangman! Guess the mystery word with less than 6 mistakes!")

# set world list and ASCII art list
wordList = ['cow', 'horse', 'deer', 'elephant', 'lion', 'tiger', 'baboon', 'donkey', 'fox', 'giraffe']
hangman = [' -------------',' |         |',' |          0',' |         / |',' |          |',' |         / |\n |\n |']

# prompt for word integer until appropriate input is given, error case initially true
error = True
while error:
    
    number = input('Please enter an integer number (0<=number<10) to choose the word in the list: ')
    
    # assume nonempty input initially
    emptyInput = False
    
    # test for empty input
    if number == '':
        
        # output notification of error and set error case
        print('Empty input!')
        emptyInput = True
    
    # assume integer input initially
    nonInteger = False
    
    # if the above case passed, test for non-integer, non-empty input
    if emptyInput == False:
        
        # int() will ValueError if the input was not an integer
        try:
            number = int(number)
        except ValueError:
            
            # output notification of error and set error case
            print('Input must be an integer!')
            nonInteger = True
    
    
    # assume input is within interval initially
    outsideInterval = False
    
    # if both of the previous tests passed, test if integer input is within interval
    if (not emptyInput) and (not nonInteger) and (number < 0 or number >= 10):
        
        # output notification of error and set error case
        print('Index is out of range!')
        outsideInterval = True
    
    # set input to word integer if all tests have passed
    if (not outsideInterval) and (not emptyInput) and (not nonInteger):
        
        wordNum = number
        
        error = False

# set word to guess
word = wordList[wordNum]
wordLength = len(word)

# print word length
print('The length of the word is: %d' % (wordLength))

# set blanks to accumulate guesses
wordGuess = []
for i in range(0,wordLength):
    wordGuess.append('_')

# set counter for incorrect guesses and set the victory condition to false
incorrectCount = 0
victory = False

# loop for up to 6 guesses or until player has won
while incorrectCount < 6 and not victory:
    
    # prompt for guess until single, alphabetic character is given, assume error case is true initially
    error = True
    while error:
        
        letterGuess = input('Please enter the letter you guess: ')
        
        # ensure guess is in lower case
        letterGuess = letterGuess.lower()
        
        # length must be 1, and the ASCII value must be between lower case 'a' (97) and lower case 'z' (122)
        if len(letterGuess) != 1 or ord(letterGuess) < 97 or ord(letterGuess) > 122:
            
            # output notification of error
            print('You need to input a single alphabetic character!')
            
        # if the input was suitable, set error case to false
        else:
            error = False
    
    # check if guess is in word
    rightLetter = letterGuess in word
    
    # guess was correct?
    if rightLetter:
        
        # inform player
        print('The letter is in the word.')
        
        # fill blanks with correct guess (loop over word, set appropriate index of blanks to the correct guess)
        for k in range(0,wordLength):
            if word[k] == letterGuess:
                wordGuess[k] = letterGuess
        
        # display progress (accumulate blanks and correct guesses into a string for output)
        progress = ''
        for character in wordGuess:
            progress = progress + character
        print('Letters matched so far: %s' % (progress))
        
        # determine if user has won (are there still blanks to be filled?)
        victory = not '_' in wordGuess
    
    # guess was incorrect?
    else:
        
        # inform player
        print('The letter is not in the word.')
        
        # display progress (accumulate blanks and correct guesses into a string for output)
        progress = ''
        for character in wordGuess:
            progress = progress + character
        print('Letters matched so far: %s' % (progress))        
        
        # increment incorrect counter
        incorrectCount = incorrectCount + 1
        
        # display as many lines of the hangman as there have been incorrect guesses
        for i in range(0,incorrectCount):
            print(hangman[i])
    

# determine if player has won or lost, output accordingly
if victory:
    print('You have found the mystery word. You win!\nGoodbye!')
else:
    print('Too many incorrect guesses. You lost!\nThe word was: %s.\nGoodbye!' % (word))