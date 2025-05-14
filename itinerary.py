dowker_example = [12,14,8,10,4,6,2]

# itinerary: N-length list of length-2 tuples for each of N crossings
# crossing_num: first position is a tuple indicating the crossing's numbers
# sign: second position is an integer (-1 or 1) indicating under or over strand
	# over means +1, under means -1

itinerary_example = [((1,12),1), ((2,13),-1), ((3,14),1), ((4,9),-1), ((5,8),1), ((6,11),-1), ((7,10),1), ((8,5),-1), ((9,4),1), ((10,7),-1), ((11,6),1), ((12,1),-1), ((13,2),1), ((14,3),-1)]

def get_paired_num(num, dowker, odds):
	if num in dowker:
		index = dowker.index(num)
		return odds[index]
	elif num in odds:
		index = odds.index(num)
		return dowker[index]
	else: # num not in either list
		return "you've fucked up"

def dowker_to_itinerary(dowker):

	N = len(dowker)
	itinerary = []

	odds = []
	for i in range(N): # make [1,3,...]
		odds.append(i*2+1)

	# for each crossing, times two
	for i in range(2*N):
	
		paired_num = get_paired_num(i+1, dowker, odds)
		crossing_num = (i+1, paired_num)

		# sign info isn't in dowker so uh idk man
		if i%2 == 0: # if i is even
			sign = 1
		else:
			sign = -1

		crossing = (crossing_num, sign)

		itinerary.append(crossing)
	return itinerary


def itinerary_to_dowker(itinerary):

	N = int(len(itinerary)/2)
	dowker = []
	
	for i in range(N): # for each crossing

		# we only need odd-numbered crossings from the itinerary because of the repeating, so index 0, 2, 4, etc.
		crossing_num = itinerary[i*2][0]
		odd_val, dowker_val = crossing_num # unpack tuple

		dowker.append(dowker_val)
	return dowker


print("\n\n\n\nnew round of tests")
dowker_result = itinerary_to_dowker(itinerary_example)
print(dowker_result)
print(dowker_result == dowker_example)

itinerary_result = dowker_to_itinerary(dowker_example)
print(itinerary_result)
print(itinerary_result == itinerary_example)
