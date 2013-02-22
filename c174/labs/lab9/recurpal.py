import string

def isPal(s):
   
   if len(s) < 2:
      return True
   
   else:
      if s[0] in string.punctuation + ' ':
         return isPal(s[1:])
      
      if s[len(s)-1] in string.punctuation + ' ':
         return isPal(s[0:len(s)-1])
      
      if s.lower()[0] == s.lower()[len(s)-1]:
         return isPal(s[1:len(s)-1])
      
      else:
         return False
    

test = input('potential palindrome: ')

if isPal(test) == True:
   print('"' + test + '"' + ' is a palindrome.')
else:
   print('"' + test + '"' + ' is not a palindrome.')