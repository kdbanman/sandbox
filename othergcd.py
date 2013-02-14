def gcd(y,x):
	iterations = 0
	mult = 0
	tablevals = []

	tablevals.append([y,0])
	while x > 0:
		mult = int(y/x)
		tablevals.append([x, mult])
		t = x
		x = y % x
		y = t

	tablevals.reverse()
	tablevals[0].append(0)
	tablevals[1].append(1)
	k = 2
	while k < len(tablevals):
		comb = tablevals[k-1][1]*tablevals[k-1][2]+tablevals[k-2][2]
		tablevals[k].append(comb)
		k += 1

	k = 2
	while k < len(tablevals):
		if k%2 ==0:
			tablevals[k][2] = tablevals[k][2]*-1
		k += 1

	tablevals.reverse()
	print ""
	for row in tablevals:
		first = str(row[0])
		second = str(row[1])
		third = str(row[2])
		print "  " + first + " "*(23-len(first)) + second + " "*(10-len(second)) + third
	
	print ""
gcd(307095137419153426,87639017365627)
