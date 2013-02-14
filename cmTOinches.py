# take input as number of centimeters
centimeters = float( input("How many centimeters do you want to convert? ") )

# convert input from centimeters to inches (2.54 centimeters to an inch)
inches = centimeters / 2.54

# number of yards (36 inches in a yard)
yards = inches // 36

# first remainder of inches
remainderOne = inches % 36

# number of feet in first remainder (12 inches in a foot)
feet = remainderOne // 12

# second remainder of inches
remainderTwo = remainderOne % 12

# formatted output
print("This is %d yards, %d feet, %f inches" % (yards, feet, remainderTwo) )

