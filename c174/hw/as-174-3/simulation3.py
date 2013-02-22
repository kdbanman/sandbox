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

#function to determine rate of customer arrival based upon time of day
def number_new_customers(time):
    if time < 29: #before 8:30
        customers = 5
    elif time < 209 and time%3 == 1: #before 11:30, every third minute
        customers = 1
    elif time < 329: #before 13:30
        customers = 10
    elif time < 569 and time%3 == 1: #before 17:30
        customers = 1
    elif time < 629:
        customers = 8
    elif time < 721 and time%5 == 1: #before 20:00, every fifth minute
        customers = 1
    else:
        customers = 0
    
    return customers

#function to add new incoming customers
def add_incoming_customers(time, arrivals, lineup):
    number = number_new_customers(time) # number of customers arriving now
    first_new = len(arrivals) # ID of the first new customer
    last_new = first_new + number # ID of the last new customer
        
    #add the new customer IDs and arrival times
    for ID in range(first_new, last_new):
        arrivals.append(now)
        lineup.append(ID)
    
#function to record customer ordering time
def take_customer_orders(time, order, departure, lineup, waitup):
    number = random.choice([3,5,7]) #number of customers whose orders are taken now
    orders = min(number, len(lineup))
    while orders > 0:
        order.append(time)
        service_time = random.choice([1,1,1,1,1,2,2,2,5,9])
        departure.append(time + service_time)

        ID = lineup.popleft()
        waitup.append(ID)
        
        orders = orders - 1
        
    if len(lineup) > 10: #second cashier if the line is longer than 10 customers
        number = random.choice([3,5,7]) #number of customers whose orders are taken now
        orders = min(number, len(lineup))
        while orders > 0:
            order.append(time)
            service_time = random.choice([1,1,1,1,1,2,2,2,5,9])
            departure.append(time + service_time)

            ID = lineup.popleft()
            waitup.append(ID)
        
            orders = orders - 1
            
#function to send customers out
def serve_customers(time, departure, waitup, serviced):
    leaving = [ ]
    for ID in waitup:
        if departure[ID] == time:
            leaving.append(ID)
            
    for ID in leaving:
        waitup.remove(ID)
        serviced.append(ID)

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
    add_incoming_customers(now, arr_time, in_line)
    
    #*** STEP 2***
    #now we take some orders
    take_customer_orders(now, ord_time, dep_time, in_line, waiting_food)
    
    #*** STEP 3***
    #hand-over the food so customers can leave!
    serve_customers(now, dep_time, waiting_food, serviced)
        
    #un-comment the lines below while testing!
    #print_status(now, arr_time, ord_time, dep_time, \
    #             in_line, waiting_food, serviced)
    
    #*** STEP 4***
    #increment the time
    now = now + 1

#compute and print statistics about the simulation
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