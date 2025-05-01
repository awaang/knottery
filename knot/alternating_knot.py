from knot.knot import Knot
import numpy as np
import networkx as net

class AlternatingKnot(Knot):
    # checks if dowker code is lexicographically minimal
    def is_lexographic(self):
        start = self.dowker[0] - 1    #Stores the difference of the first crossing numbers
        if start > len(self.dowker):        #If reversing traversal direction would make a smaller diff, return False
            return False
        for crossing in range(len(self.dowker)):   #Iterates thru code, checks if crossings are same distance or less
            odd = 2 * crossing + 1                #Odd part of dowker code
            even  = self.dowker[crossing]            #Even part of dowker code
            diff = np.abs(odd - even)           #Checks difference of each crossing in dowker code
            if diff < start:               #If difference less than first crossing difference return false
                return False
        return True               #Returns true if escaped all flagging
    
    # checks if dowker code is prime
    def is_prime(self):
        sequence = []             #List for consecutive subsequence that indicates composite knot
        for x in range(len(self.dowker)):             #Iterates thru dowker code
            for y in (range(len(self.dowker) - x)):           #At each index in dowker code, iterates through remainder of code
                consecutive = True            #Variable for consecutiveness of subsequence
                odd = 2 * (x + y) + 1              #Stores odd part of dowker code adjusting for the starting index for subsequence
                even = self.dowker[x + y]          #Stores even part of dowker code adjusting for even part of subsequence 
                sequence.append(odd)               #Appends odd part to subsequence
                sequence.append(even)              #Appends even part to subsequence
                sequence.sort()               #Sorts to get smallest crossing number at start of subsequence
                #print(sequence)
                start = sequence[0]           #Stores smallest number in subsequence
                for z in range(len(sequence)):               #Iterates through subsequence
                    if start + z not in sequence:           #Checks if each consecutive number is in not subsequence
                        consecutive = False           #Flags for non consecutive subsequences
                #print("Start:", start)
                if consecutive == True and len(sequence) != len(self.dowker) * 2:               #If consecutive subsequence that is not entire dowker code, return composite
                    return False
            sequence = []            #Resets subsequence for next index in dowker code
        return True               #If no consecutive subsequences found, return prime
    
    # unused function
    def is_composite(self):
        n = len(self.dowker)

        for cut in range(2, n, 2):  # try splitting between cut and n-cut crossings
            block1_vals = set(range(2, 2 * cut + 2, 2))
            block2_vals = set(range(2 * cut + 2, 2 * n + 2, 2))

            # Check if the code can be split into two clean blocks
            block1 = []
            block2 = []
            for i, val in enumerate(self.dowker):
                if val in block1_vals and (2 * i + 2) in block1_vals:
                    block1.append(val)
                elif val in block2_vals and (2 * i + 2) in block2_vals:
                    block2.append(val)
                else:
                    break  # Crossing links outside its own block
            else:
                if len(block1) > 0 and len(block2) > 0:
                    print("block1:", block1)
                    print("block2:", block2)
                    return True  # Found a valid decomposition
        return False

    # checks if dowker code is possible
    def is_possible(self): 
        try:
            G = Knot.graphify_dowker(self)
            var = net.is_planar(G) # planarity check
            return var
        except Exception as e:
            return False
    
    # detects all order-1 flypes (flypable tangles) in the knot, returning data structures to describe the sequences involved and the crossing location.
    def flype_detect(self):
        flypes = []
        dowker = self.dowker
        for x in range(2 * len(self.dowker)):              #Iterates through each number in dowker code
            sequence1 = []           #Two sequences that make up tangle
            sequence2 = []
            consecutive = True            #Variable for consecutiveness indicating two strands
            for y in range(len(self.dowker) - 1):             #Looking at the string up to y away from number dictated by x
                number = x + y + 1            #Numbers in sequence 1
                if number > 2 * len(self.dowker):            #If number is greater than largest number in dowker code, wraps back around
                    number = number - 2 * len(self.dowker)
                sequence1.append(number)           #Adds number to sequence1
                if (number) % 2 == 0: #If sequence1 element is even
                    index = self.dowker.index(number)            #Finds index of number in sequence1 in dowker code
                    sequence2.append(2 * index + 1)              #Adds corresponding odd number to sequence2
                else:               #If sequence1 element is odd
                    even = self.dowker[int((number - 1)/2)]      #Finds corresponding even number of odd # in sequence1 in dowker code
                    sequence2.append(even)             #Adds corresponding even number to sequence2
                if y > 0:           #Begins checking consecutiveness of sequence2 if length of it greater than equal to 2
                    latest = sequence2[len(sequence2) - 1]              #Stores most recently added element to sequence
                    sequence2.sort()              #Sorts the second sequence to find start and end of it
                    start = sequence2[0]           #Stores smallest number in subsequence
                    for z in range(len(sequence2)):               #Iterates through subsequence
                        if start + z not in sequence2:           #Checks if each consecutive number is in not subsequence
                            consecutive = False
                    if consecutive == False:
                        sequence1.pop()          #Avoids flypes changing when sequence changes
                        sequence2.remove(latest)             #Avoids flypes changing when sequence changes
                        break               #Rest of sequence2 wont be consecutive if this part isnt
                    else:               #If consecutive, finds crossings around tangle, then appends to flypes appropriately
                        flag, crossing = AlternatingKnot.flype_crossing(self, sequence1[0] - 1, sequence1, sequence2)         #Finds a crossing before start of first sequence
                        flypes.append(AlternatingKnot.flype_appendage(flag, flypes, crossing, sequence1, sequence2))          #Appends tangle and crossing if possible flype
                        flag, crossing = AlternatingKnot.flype_crossing(self, sequence2[0] - 1, sequence1, sequence2)         #Finds a crossing before start of second sequence
                        flypes.append(AlternatingKnot.flype_appendage(flag, flypes, crossing, sequence1, sequence2))               
                        flag, crossing = AlternatingKnot.flype_crossing(self, sequence1[len(sequence1) - 1] + 1, sequence1, sequence2)            #Finds a crossing after end of first sequence
                        flypes.append(AlternatingKnot.flype_appendage(flag, flypes, crossing, sequence1, sequence2))
                        flag, crossing = AlternatingKnot.flype_crossing(self, sequence2[len(sequence2) - 1] + 1, sequence1, sequence2)            #Finds a crossing after end of second sequence
                        flypes.append(AlternatingKnot.flype_appendage(flag, flypes, crossing, sequence1, sequence2))
                        flypes = Knot.list_remove(flypes)             #Removes all lists added through flype_appendage()
        for i in range(len(flypes)):             #Removes the case of crossing for flype detected inside tangle
            if flypes[i][2] in flypes[i][0] or flypes[i][2] in flypes[i][1]:
                flypes[i] = 0
            elif len(flypes[i][0]) == len(self.dowker) - 1:
                flypes[i] = 0
        flypes = Knot(flypes).zero_remove()            #For formatting
        return flypes
    
    def flype_crossing(self, x, sequence1, sequence2):
        if x < 1:            #If crossing being checked is below 1, wraps to top of dowker code
            x = 2 * len(self.dowker) + x
        elif x >  2 * len(self.dowker):               #If crossing being checked above biggest # in dowker code, wraps back to 1
            x = x - 2 * len(self.dowker)
        if x % 2 == 0:       #If x is even
            index = self.dowker.index(x)             #Finds index of even number in dowker code
            odd = 2 * index + 1            #Constructs odd number corresponding to the even x    
            if sequence1[0] - 1 == odd:              #Checks if before sequence1 matches crossing
                return True, odd
            elif sequence2[0] - 1 == odd:            #Checks if before sequence2 matches crossing
                return True, odd
            elif sequence1[len(sequence1) - 1] + 1 == odd:               #Checks if after sequence1 matches crossing
                return True, odd
            elif sequence2[len(sequence2) - 1] + 1 == odd:               #Checks if after sequence2 matches crossing
                return True, odd
            else:
                return False, odd              #If no matches return false
        else:           #If x is odd
            odd = x
            index = int((x - 1)/2)              #Constructs index of odd number in dowker code
            if sequence1[0] - 1 == self.dowker[index]:              #Checks if before sequence1 matches crossing
                return True, odd
            elif sequence2[0] - 1 == self.dowker[index]:            #Checks if before sequence2 matches crossing
                return True, odd
            elif sequence1[len(sequence1) - 1] + 1 == self.dowker[index]:            #Checks if after sequence1 matches crossing
                return True, odd
            elif sequence2[len(sequence2) - 1] + 1 == self.dowker[index]:          #Checks if after sequence2 matches crossing
                return True, odd
            else:
                return False, odd              #If no matches return false

    def flype_appendage(flag, flypes, crossing, sequence1, sequence2):
        newflype = []            #Creates a list of a flype to add to list of flypes
        if flag == True:         #Checks if flype is to be added
            if len(flypes) == 0:               #Always adds flype if one to be added and none yet in list
                newflype.append(sequence1)              #Adds two sequences and crossing to newflype
                newflype.append(sequence2)
                newflype.append(crossing)
            else:
                flypes = Knot.list_remove(flypes)
                for flype in flypes:            #Avoids adding two duplicate flypes to list when x and y indices are flipped in flype_detect()
                        if sequence1 == flype[0] or sequence1 == flype[1]:
                            if sequence2 ==flype[0] or sequence2 == flype[1]:
                                if crossing == flype[2]:
                                    return newflype
                newflype.append(sequence1)              #Adds two sequences and crossing to new flype
                newflype.append(sequence2)
                newflype.append(crossing)
        return newflype     

    # this function is not used anywhere
    def flype_lexographic(self, flypeddowker, permutations):
        if flypeddowker in permutations and self.dowker != flypeddowker:
            for i in range(len(flypeddowker)):
                if self.dowker[i] > flypeddowker[i]:
                        index = permutations.index(self.dowker)
                        permutations[index] = 0
                        return permutations
                elif self.dowker[i] < flypeddowker[i]:
                        index = permutations.index(flypeddowker)
                        permutations[index] = 0
                        return permutations
        return permutations

    def make_lexographic(self):
        predowker = self.dowker
        distances = []
        dowker = []
        for crossing in range(len(self.dowker)):
            odd = 2 * crossing + 1
            even = self.dowker[crossing]
            diffforward = np.abs(odd - even)
            diffbackward = 2 * len(self.dowker) - diffforward
            distances.append(diffforward)
            distances.append(diffbackward)
        minimum = min(distances)
        index = distances.index(minimum)
        startindex = index // 2
        odd = 2 * startindex + 1
        even = self.dowker[startindex]
        if index % 2 == 0:
            correction = min(odd, even) - 1
        else:
            correction = max(odd, even) - 1
        newfromodds = []
        newfromevens = []
        for crossing in range(len(self.dowker)):
            oldodd = 2 * crossing + 1
            newfromodd = oldodd - correction
            if newfromodd < 1:
                newfromodd = 2 * len(self.dowker) - np.abs(newfromodd)
            oldeven = self.dowker[crossing]
            newfromeven = oldeven - correction
            if newfromeven < 1:
                newfromeven = 2 * len(self.dowker) - np.abs(newfromeven)
            newfromodds.append(newfromodd)
            newfromevens.append(newfromeven)
        for crossing in range(len(self.dowker)):
            odd = 2 * crossing + 1
            if correction % 2 == 0:
                index = newfromodds.index(odd)
                even = newfromevens[index]
            else:
                index = newfromevens.index(odd)
                even = newfromodds[index]
            dowker.append(even)
        return dowker

    def perform_flype(self, flype):
        startingdowker = self.dowker
        G = Knot.graphify_dowker(self)
        #net.draw(G, with_labels = True)
        #plt.show()
        tangleedgeedit = []
        crossingedgeedit = []
        sequence1min = flype[0][0]
        sequence2min = flype[1][0]
        sequence1max = flype[0][len(flype[1]) - 1]
        sequence2max = flype[1][len(flype[1]) - 1]
        crossingodd = flype[2]
        indexodd = int((crossingodd - 1)/2)
        crossingeven = self.dowker[indexodd]
        tangleedgeedit.append(AlternatingKnot.edge_identification(self, sequence1min, False))
        tangleedgeedit.append(AlternatingKnot.edge_identification(self, sequence2min, False))
        tangleedgeedit.append(AlternatingKnot.edge_identification(self, sequence1max, True))
        tangleedgeedit.append(AlternatingKnot.edge_identification(self, sequence2max, True))
        crossingedgeedit.append(AlternatingKnot.edge_identification(self, crossingodd, True))
        crossingedgeedit.append(AlternatingKnot.edge_identification(self, crossingodd, False))
        crossingedgeedit.append(AlternatingKnot.edge_identification(self, crossingeven, True))
        crossingedgeedit.append(AlternatingKnot.edge_identification(self, crossingeven, False))
        for edgecross in crossingedgeedit:
            for edgetang in tangleedgeedit:
                if edgetang == 0 or edgecross == 0:
                        pass
                elif set(edgecross) == set(edgetang):
                        index = crossingedgeedit.index(edgecross)
                        crossingedgeedit[index] = 0
                        index = tangleedgeedit.index(edgetang)
                        tangleedgeedit[index] = 0
        crossingedgeedit = Knot(crossingedgeedit).zero_remove()
        tangleedgeedit = Knot(tangleedgeedit).zero_remove()
        for edge in tangleedgeedit:
                edgetuple = (edge[0], edge[1])
                if edgetuple in G.edges and edge not in crossingedgeedit:
                        G.remove_edge(edge[0], edge[1])
        for edge in crossingedgeedit:
            edgetuple = (edge[0], edge[1])
            if edgetuple in G.edges:
                G.remove_edge(edge[0], edge[1])
        #net.draw(G, with_labels = True)
        #plt.show()
        if len(flype[0]) % 2 == 0: # If there are an even number of crossings inside flype
                if crossingedgeedit[0][0] % 2 == tangleedgeedit[0][0] % 2:
                        G.add_edge(crossingedgeedit[0][0], tangleedgeedit[0][1])
                        G.add_edge(tangleedgeedit[0][0], crossingedgeedit[0][1])
                        G.add_edge(crossingedgeedit[1][0], tangleedgeedit[1][1])
                        G.add_edge(tangleedgeedit[1][0], crossingedgeedit[1][1])
                else:
                        G.add_edge(crossingedgeedit[0][0], tangleedgeedit[1][1])
                        G.add_edge(tangleedgeedit[0][0], crossingedgeedit[1][1])
                        G.add_edge(crossingedgeedit[1][0], tangleedgeedit[0][1])
                        G.add_edge(tangleedgeedit[1][0], crossingedgeedit[0][1])
        else:
            if crossingedgeedit[0][0] % 2 == tangleedgeedit[0][0] % 2:
                G.add_edge(crossingedgeedit[0][0], tangleedgeedit[1][1])
                G.add_edge(tangleedgeedit[0][0], crossingedgeedit[1][1])
                G.add_edge(crossingedgeedit[1][0], tangleedgeedit[0][1])
                G.add_edge(tangleedgeedit[1][0], crossingedgeedit[0][1])
            else:
                G.add_edge(crossingedgeedit[0][0], tangleedgeedit[0][1])
                G.add_edge(tangleedgeedit[0][0], crossingedgeedit[0][1])
                G.add_edge(crossingedgeedit[1][0], tangleedgeedit[1][1])
                G.add_edge(tangleedgeedit[1][0], crossingedgeedit[1][1])
        #net.draw(G, with_labels = True)
        #plt.show()
        dowker = Knot.dowkerify_graph(self, G)
        dowker = AlternatingKnot.make_lexographic(Knot(dowker))
        return dowker   

    def edge_identification(self, number, max):
        edge = []
        if number % 2 == 0: 
            index = self.dowker.index(number)
            if max == True:
                node1 = (4 * index) + 3
                next = number + 1
                if next > 2 * len(self.dowker):
                        next = 1
                nextindex = int((next - 1)/2)
                node2 = (4 * nextindex) + 2
                edge.append(node1)
                edge.append(node2)
            else:
                node1 = (4 * index) + 1
                before = number - 1
                beforeindex = int((before - 1)/2)
                node2 = (4 * beforeindex) + 4
                edge.append(node1)
                edge.append(node2)
        else:
            index = int((number - 1)/2)
            if max == True:
                node1 = (4 * index) + 4
                next = number + 1
                nextindex = self.dowker.index(next)
                node2 = (4 * nextindex) + 1
                edge.append(node1)
                edge.append(node2)
            else:
                node1 = (4 * index) + 2
                before = number - 1
                if before < 1: 
                        before = 2 * len(self.dowker)
                beforeindex = self.dowker.index(before)
                node2 = (4 * beforeindex) + 3
                edge.append(node1)
                edge.append(node2)
        return edge

    def find_flype_class(self, oldcheckedcodes):
        flypes = AlternatingKnot.flype_detect(self)
        checked = []
        checked = checked + oldcheckedcodes
        checked.append(self.dowker)
        checked = [x for n,x in enumerate(checked) if x not in checked[:n]]
        codesfromflypes = []
        for flype in flypes:
            newcode = AlternatingKnot.perform_flype(self, flype)
            codesfromflypes.append(newcode)
        codesfromflypes = [x for n,x in enumerate(codesfromflypes) if x not in codesfromflypes[:n]]
        comparison = checked + codesfromflypes
        comparison = [x for n,x in enumerate(comparison) if x not in comparison[:n]]
        if comparison == checked:
            return checked
        else:
            for code in codesfromflypes:
                if code not in checked:
                    checked = AlternatingKnot.find_flype_class(Knot(code), checked)
            return checked