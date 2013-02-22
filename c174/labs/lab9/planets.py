
planets = {
    'mercury' : {'radius' : 2439.7,
                 'distance from the sun' : 58000000,
                 'moons' : [],
                 'atmosphere' : True,
                 'gas planet' : False},
           
    'venus' : {'radius' : 6051.8,
               'distance from the sun' : 108000000,
               'moons' : [],
               'atmosphere' : True,
               'gas planet' : False},
    
    'earth' : {'radius' : 6371.0,
               'distance from the sun' : 150000000, 
               'moons' : ['moon'],
               'atmosphere' : True,
               'gas planet' : False},
    
    'mars' : {'radius' : 3396.2,
              'distance from the sun' : 107000000,
              'moons' : ['phobos','diemos'],
              'atmosphere' : True,
              'gas planet' : False},
    
    'jupiter' : {'radius' : 69911.0,
                 'distance from the sun' : 483000000,
                 'moons' : ['io','ganymede','callisto','europa','adrastea'],
                 'atmosphere' : True,
                 'gas planet' : True},
    
    'saturn' : {'radius' : 60268.0,
                'distance from the sun' : 1400000000,
                'moons' : ['pan','prometheus','titan','phoebe','rhea'],
                'atmosphere' : True,
                'gas planet' : True},
    
    'uranus' : {'radius' : 25559.0,
                'distance from the sun' : 3000000000,
                'moons' : ['miranda', 'ariel','umbriel','titania','oberon'],
                'atmosphere' : True,
                'gas planet' : True},
    
    'neptune': {'radius' : 24764.0,
                'distance from the sun' : 4500000000,
                'moons' : ['triton','nereid','proteus','naiad','thalassa'],
                'atmosphere' : True,
                'gas planet' : True}}

listType = type([])
for planet in planets:
    print(planet)
    for p,value in planets[planet].items():
        
        #print the list of moons with commas
        if type(value) == listType and len(value)>1:
            string = value[0]
            for word in value[1:]:
                
                string = string + ', ' + word
            value = string
            
        print('\t' + str(p) + ' - ' + str(value))
       
print('\n\nfurthest gas planet from the sun is')
maxdist = 0
for planet in planets:
    if planets[planet]['gas planet'] == True:
        if planets[planet]['distance from the sun'] > maxdist:
            maxdist = planets[planet]['distance from the sun']
            maxplanet = planet
            
print(maxplanet)

print('\n\nclosest to the sun with at least 2 moons is')
minDist = 100**100
for planet in planets:
    if len(planets[planet]['moons']) > 1:
        if planets[planet]['distance from the sun'] < minDist:
            minDist = planets[planet]['distance from the sun']
            minplanet = planet
            
print(minplanet)

print('\n\nplanet with moon europa is')
for planet in planets:
    if 'europa' in planets[planet]['moons']:
        print(planet)