import csv

def checkIntersection(p1, p2):
    cond1 = max(p1[0], p1[2]) < min(p2[0], p2[2]) #p1 completely to left of p2
    cond2 = min(p1[0], p1[2]) > max(p2[0], p2[2]) #p2 completely to left of p1
    cond3 = max(p1[1], p1[3]) < min(p2[1], p2[3]) #p1 completely below p2
    cond4 = min(p1[1], p1[3]) > max(p2[1], p2[3]) #p2 completely below p1
    return not cond1 and not cond2 and not cond3 and not cond4

allProps = [] 
names = [];
file = open('properties.csv')

for line in file:
    line = line.rstrip('\n')
    tokens = line.split(',')
    name = tokens[0]
    properties = []
    names.append(name)
    p = 1
    propertyNum = 0
    while p < len(tokens):    
        
        if p%4 == 0:
            properties.append((tokens[1+propertyNum*4],tokens[2+propertyNum*4],tokens[3+propertyNum*4],tokens[4+propertyNum*4]))
            propertyNum = propertyNum + 1

        p = p +1
        
    allProps.append([name, properties])

print("List of all property holders:")
print(names)

name1 = input('first name? ').lower()
name2 = input('second name? ').lower()

for person in allProps:
    if name1 == allProps