# input efficiency in mpg
efficiencyMPG = float( input("Enter your fuel efficiency in MPG: ") )

# convert mpg to km/L (0.42514 km/L in mpg)
efficiencyKMPL = 0.42514 * efficiencyMPG

# output converted efficiency
print("The converted efficiency is %6.3f kilometers per liter." % (efficiencyKMPL) )

