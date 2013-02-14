line = input('type in a line of text: ')

length = len(line) - 1
half = length//2
i = 0

isPalindrome = True

while i <= half:
        if line[i] != line[length - i]:
                isPalindrome = False
        i = i + 1
print('Palindrome? ', isPalindrome)
