#prompt for each grade out of 100
labs = float(input("lab exercises? "))
assignments = float(input("assignments? "))
midterm = float(input("midterm? "))
exam = float(input("exam? "))

#weight each grade and sum to final grade
final = 0.15 * labs + 0.25 * assignments + 0.25 * midterm + 0.35 * exam

#determine letter grade
if final >= 80:
    grade = 'A'
elif final >= 70:
    grade = 'B'
elif final >= 60:
    grade = 'C'
elif final >= 50:
    grade = 'D'
else:
    grade = 'F'
    
#output result
print("the final mark is %2.0f%% and the letter grade is %s." % (final, grade))