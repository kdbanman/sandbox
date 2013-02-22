import random, sys
from collections import deque

# do not remove the next two lines!
if len(sys.argv) > 1:
    random.seed(sys.argv[1])

#function to print the simulation status
def print_status(time, arrivals, orders, departures, lineup, waitup, serviced):
    print("at the end of step ", time)
    print("waiting in line :", lineup)
    print("waiting for food:", waitup)
    print("serviced        :", serviced)
    print("------ below you see time stamps ------")
    print("arrival times   :", arrivals)
    print("order times     :", orders)
    print("departure times :", departures)
    print()

# *** NO FUNCTION DEFINITION PAST THIS LINE ***

# data structures to keep track of the arrival, order, and departure times
arr_time = [ ] # arrival times of customers
ord_time = [ ] # order times of customers
dep_time = [ ] # departure times of customers

# data structures to keep customers IDs
in_line = deque([ ]) #customers who have not ordered yet
waiting_food = [ ] # customers who have ordered
serviced = [ ] #customers who have left

# total time for the simulation
tics = 720

#
# simulation main loop
#
now = 0
while now < tics:
    #*** STEP 1 ****
    #the first thing is to add new customers (all arriving at the same time)

    number = random.randint(3,10) # number of customers arriving now
    first_new = len(arr_time) # ID of the first new customer
    last_new = first_new + number # ID of the last new customer
        
    #add the new customer IDs and arrival times
    for ID in range(first_new, last_new):
        arr_time.append(now)
        in_line.append(ID)
    
    #*** STEP 2***
    #now we take some orders
 
    number = random.choice([3,5,7]) #number of customers whose orders are taken now
    orders = min(number, len(in_line))
    while orders > 0:
        ord_time.append(now)
        service_time = random.choice([1,1,1,1,1,2,2,2,5,9])
        dep_time.append(now + service_time)

        ID = in_line.popleft()
        waiting_food.append(ID)
        
        orders = orders - 1
    
    #*** STEP 3***
    #hand-over the food so customers can leave!
    leaving = [ ]
    for ID in waiting_food:
        if dep_time[ID] == now:
            leaving.append(ID)
            
    for ID in leaving:
        waiting_food.remove(ID)
        serviced.append(ID)
        
    #un-comment the lines below while testing!
    #print_status(now, arr_time, ord_time, dep_time, \
    #             in_line, waiting_food, serviced)
    
    #*** STEP 4***
    #increment the time
    now = now + 1

#TODO: compute and print statistics about the simulation
waitTimes = []
serviceTimes = []

for i in range(0,len(dep_time)-1):
    waitTimes.append(ord_time[i] - arr_time[i])
    serviceTimes.append(dep_time[i] - ord_time[i])
    
minWait = min(waitTimes)
maxWait = max(waitTimes)
avgWait = sum(waitTimes)/len(waitTimes)

minService = min(serviceTimes)
maxService = max(serviceTimes)
avgService = sum(serviceTimes)/len(serviceTimes)

serviced  = len(serviceTimes)
waiting = len(in_line)

print('waiting times:')
print('\tminimum: %d maximum: %d average: %f' % (minWait, maxWait, avgWait))

print('service times:')
print('\tminimum: %d maximum: %d average: %f' % (minService, maxService, avgService))

print('serviced: ' + str(serviced))
print('waiting: ' + str(waiting))