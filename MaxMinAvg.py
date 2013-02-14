# prompt for first number
new = 0.0
try:
    new = float(input("What is the first number? "))
except ValueError:
    print("That isn't a number.")


# initialize counter
count = 1

# set max, min, and sum to new number
highest = new
lowest = new
total = new

# ask if there are more numbers
areMore = input("Are there more numbers? ")

while areMore.lower() == 'yes' or areMore.lower() == 'y':

    failed = False
    
    # prompt for new number
    try:
        new = float(input("What is the new number? "))
    except ValueError:
        print("That isn't a number.")
        failed = True
    
    if failed == False:
        
        # store number as highest if it is the highest
        if new > highest:
            highest = new
    
            # store number as lowest if it is the lowest
        elif new < lowest:
            lowest = new
    
        # increase the total by the new number
        total = total + new
    
        # increment the counter
        count = count + 1
    
        # ask if there are more numbers
        areMore = input("Are there more numbers? ")  

# compute average
average = total/count

# print results
print("The maximum is %5.2f\nThe minimum is %5.2f\nThe average is %5.2f" % (highest, lowest, average))