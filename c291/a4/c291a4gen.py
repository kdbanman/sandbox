# kirby banman
# 22 nov 2012
# c291a4 dataset generator
# 
# - takes command line arguments of length and maximum users per song (<64)
# - users rating each song are drawn from a pool of 4096 usernames regardless
#   of song count or raters per song, so varying dataset size and users
#   per song will change the average relatedness of songs

import random
import datetime
import string
import sys

def genPool(pool):
	'''
	generates a random list of unique usernames of length (pool)
	'''
	assert type(pool)==type(1)
	assert pool>0
	assert pool<4097

	adjs = ["autumn", "hidden", "bitter", "misty", "silent", "empty", "dry", "dark", "summer", "icy", "delicate", "quiet", "white", "cool", "spring", "winter", "patient", "twilight", "dawn", "crimson", "wispy", "weathered", "blue", "billowing", "broken", "cold", "damp", "falling", "frosty", "green", "long", "late", "lingering", "bold", "little", "morning", "muddy", "old", "red", "rough", "still", "small", "sparkling", "throbbing", "shy", "wandering", "withered", "wild", "black", "young", "holy", "solitary", "fragrant", "aged", "snowy", "proud", "floral", "restless", "divine", "polished", "ancient", "purple", "lively", "nameless"]
	nouns = ["waterfall", "river", "breeze", "moon", "rain", "wind", "sea", "morning", "snow", "lake", "sunset", "pine", "shadow", "leaf", "dawn", "glitter", "forest", "hill", "cloud", "meadow", "sun", "glade", "bird", "brook", "butterfly", "bush", "dew", "dust", "field", "fire", "flower", "firefly", "feather", "grass", "haze", "mountain", "night", "pond", "darkness", "snowflake", "silence", "sound", "sky", "shape", "surf", "thunder", "violet", "water", "wildflower", "wave", "water", "resonance", "sun", "wood", "dream", "cherry", "tree", "fog", "frost", "voice", "paper", "frog", "smoke", "star"]
	users = []
	for a in adjs:
		for n in nouns:
			users.append(a+"_"+n)
	
	userPool = []
	for t in xrange(pool):
		userPool.append(users.pop(random.randrange(len(users))))

	return userPool

def userGen(width, userPool):
	'''
	return list of unique usernames to a max of 64 (until someone makes
	this more clever)
	'''
	assert type(width)==type(1)
	assert type(userPool)==type([])
	assert width>0
	assert width<65
	assert len(userPool)>0
	
	users = []
	for t in xrange(width):
		users.append(userPool[random.randrange(len(userPool))])

	return users

def timeStamp():
	'''
	custom timestamp unique minute-to-minute
	'''
	now = datetime.datetime.now()

	return str(now.hour)+"-"+str(now.minute)

def ratePick(userList):
	'''
	returns a dictionary of integer ratings in the interval [0,10] where
	the keys are the users in the list passed to the function
	'''
	assert type(userList)==type([])

	ratings = {}
	for user in userList:
		ratings[user] = random.randrange(1,11)

	return ratings

def songMeta(songID):
	'''
	returns a formatted string:
	[<sid>],[s<sid> <random title string>],[<random artist string>]
	as per the assignment spec
	'''
	assert type(songID)==type(1)
	assert songID>0

	sid = str(songID)

	chars = string.ascii_uppercase+string.digits
	artLength = random.randrange(1,30)
	lLength = random.randrange(1,50)
	title = "".join(random.choice(chars) for x in xrange(lLength))
	artist = "".join(random.choice(chars) for x in xrange(artLength))
	
	return "["+sid+"],[s"+sid+" "+title+"],["+artist+"]"

def songRate(raterDict):
	'''
	from the passed dictionary of usernames, returns a formatted string:
	[(<username>,<rating>),(<username>,<rating>,...,(<username>,<rating>)]
	'''
	assert type(raterDict)==type({})
	assert len(raterDict)>0

	temp = ""
	firstIter = True
	for k,v in raterDict.iteritems():
		if not firstIter:
			temp += ","
		temp += "("+k+","+str(v)+")"
		firstIter = False
	
	return "["+temp+"]"
	
def writeSongs(length, width, pool, stamped=False):
	'''
	write a .txt file to disk containing (length) number of songs and
	(width) number of users drawn from a user pool the size of (pool).
	song ids range from 1 to (length), ascending order in file.  
	'''
	assert type(length)==type(1)
	assert type(width)==type(1)
	assert type(pool)==type(1)
	assert length>0
	assert width>0
	assert width<65
	assert pool>=width

	userPool = genPool(pool)
	
	if stamped:
		f = open(str(length)+"Lx"+str(width)+"Wx"+str(pool)+"U"+timeStamp(),"w")
	else:
		f = open(str(length)+"Lx"+str(width)+"Wx"+str(pool)+"U","w")

	for songID in xrange(1, length+1):
		userList = userGen(random.randrange(1,width+1), userPool)
		raterDict = ratePick(userList)
		preString = songMeta(songID)
		postString = songRate(raterDict)
		f.write("{"+preString+","+postString+"}\n")
	f.close()

if __name__ == "__main__":
	length = sys.argv[1]
	width = sys.argv[2]
	pool = sys.argv[3]
	try:
		length = int(length)
		width = int(width)
		pool = int(pool)
		assert length>0
		assert width>0
		assert pool>=width
		
	except:
		print "<length>, <max users per song>, <max users> should be integers > 0, where <max users> > <max users per song>"
	
	writeSongs(length,width,pool)
