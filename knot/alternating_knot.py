from knot.knot import Knot
import numpy as np
import networkx as net

class AlternatingKnot(Knot):
    def is_lexographic(self):
        """
        Determines whether the current Dowker code is lexicographically minimal.

        Returns:
            bool: True if the Dowker code is lexographically minimal, False otherwise.
        """
        n = len(self.dowker)
        start = self.dowker[0] - 1    #Stores the difference of the first crossing numbers
        if start > n:        #If reversing traversal direction would make a smaller diff, return False
            return False
        for crossing in range(n):   #Iterates thru code, checks if crossings are same distance or less
            odd = 2 * crossing + 1                #Odd part of dowker code
            even  = self.dowker[crossing]            #Even part of dowker code
            diff = np.abs(odd - even)           #Checks difference of each crossing in dowker code
            if diff < start:               #If difference less than first crossing difference return false
                return False
        return True               #Returns true if escaped all flagging
    
    def is_prime(self):
        """
        Determines whether the knot is prime based on its Dowker code.

        A composite knot will contain a nontrivial consecutive subsequence that does not span the full code.

        Returns:
            bool: True if the knot is prime, False if it's composite.
        """
        n = len(self.dowker)
        sequence = []             #List for consecutive subsequence that indicates composite knot
        for x in range(n):             #Iterates thru dowker code
            for y in (range(n - x)):           #At each index in dowker code, iterates through remainder of code
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
                if consecutive == True and len(sequence) != 2 * n:               #If consecutive subsequence that is not entire dowker code, return composite
                    return False
            sequence = []            #Resets subsequence for next index in dowker code
        return True               #If no consecutive subsequences found, return prime
    
    # unused function
    def is_composite(self):
        """
        Heuristic check to determine if the Dowker code can be partitioned 
        into two non-interacting crossing blocks (suggesting a composite knot).

        Returns:
            bool: True if a decomposition into two blocks is found, False otherwise.
        """
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

    def is_possible(self): 
        """
        Checks whether the Dowker code represents a planar knot diagram.

        Uses NetworkX's planarity check on the constructed knot graph.

        Returns:
            bool: True if the Dowker code corresponds to a planar graph, False otherwise.
        """
        try:
            G = Knot.graphify_dowker(self)
            var = net.is_planar(G) # planarity check
            return var
        except Exception as e:
            return False
    
    def flype_detect(self):
        """
        Detects all valid order-1 flypes in the current knot.

        Iterates over all potential tangle regions and finds sequences 
        where flypes can be applied, returning the corresponding tangle 
        segments and their adjacent crossing.

        Returns:
            list: A list of flypes, each represented as [sequence1, sequence2, crossing].
        """
        n = len(self.dowker)
        flypes = []

        for x in range(2 * n): # iterate 1 through 2n (all possible starting points)
            sequence1 = []           # Two sequences that make up tangle
            sequence2 = []
            consecutive = True            #Variable for consecutiveness indicating two strands

            for y in range(n-1):             #Looking at the string up to y away from number dictated by x
                number = x + y + 1            #Numbers in sequence 1
                if number > 2 * n:            #If number is greater than largest number in dowker code, wraps back around
                    number = number - 2 * n
                sequence1.append(number)           #Adds number to sequence1
                if (number) % 2 == 0: #If sequence1 element is even
                    index = self.dowker.index(number)            #Finds index of number in sequence1 in dowker code
                    sequence2.append(2 * index + 1)              #Adds corresponding odd number to sequence2
                else:               #If sequence1 element is odd
                    even = self.dowker[int((number - 1)/2)]      #Finds corresponding even number of odd # in sequence1 in dowker code
                    sequence2.append(even)             #Adds corresponding even number to sequence2
                if y > 0:           #Begins checking consecutiveness of sequence2 if length of it greater than equal to 2
                    latest = sequence2[-1]              #Stores most recently added element to sequence
                    sequence2.sort()              #Sorts the second sequence to find start and end of it
                    start = sequence2[0]           #Stores smallest number in subsequence
                    for z in range(len(sequence2)):               #Iterates through subsequence
                        if start + z not in sequence2:           #Checks if each consecutive number is in not subsequence
                            consecutive = False
                    if not consecutive:
                        sequence1.pop()          #Avoids flypes changing when sequence changes
                        sequence2.remove(latest)             #Avoids flypes changing when sequence changes
                        break               #Rest of sequence2 wont be consecutive if this part isnt
                    else:               #If consecutive, finds crossings around tangle, then appends to flypes appropriately
                        flag, crossing = AlternatingKnot.flype_crossing(self, sequence1[0] - 1, sequence1, sequence2)         #Finds a crossing before start of first sequence
                        flypes.append(AlternatingKnot.flype_appendage(flag, flypes, crossing, sequence1, sequence2))          #Appends tangle and crossing if possible flype
                        flag, crossing = AlternatingKnot.flype_crossing(self, sequence2[0] - 1, sequence1, sequence2)         #Finds a crossing before start of second sequence
                        flypes.append(AlternatingKnot.flype_appendage(flag, flypes, crossing, sequence1, sequence2))               
                        flag, crossing = AlternatingKnot.flype_crossing(self, sequence1[-1] + 1, sequence1, sequence2)            #Finds a crossing after end of first sequence
                        flypes.append(AlternatingKnot.flype_appendage(flag, flypes, crossing, sequence1, sequence2))
                        flag, crossing = AlternatingKnot.flype_crossing(self, sequence2[-1] + 1, sequence1, sequence2)            #Finds a crossing after end of second sequence
                        flypes.append(AlternatingKnot.flype_appendage(flag, flypes, crossing, sequence1, sequence2))
                        flypes = [flype for flype in flypes if len(flype) != 0] #Removes all lists added through flype_appendage()
        
        for i in range(len(flypes)):             #Removes the case of crossing for flype detected inside tangle
            if flypes[i][2] in flypes[i][0] or flypes[i][2] in flypes[i][1]:
                flypes[i] = 0
            elif len(flypes[i][0]) == n - 1:
                flypes[i] = 0
        flypes = Knot(flypes).zero_remove() # remove all zeroed flypes
        return flypes
    
    def flype_crossing(self, x, sequence1, sequence2):
        """
        Checks whether a crossing adjacent to a given tangle is a valid flype crossing.

        Args:
            x (int): The crossing number to check (can be outside 1–2n, will wrap).
            sequence1 (list): The first half of the tangle.
            sequence2 (list): The second half of the tangle.

        Returns:
            tuple: (bool, int) — True and the crossing number if valid, 
                otherwise False and the candidate crossing.
        """
        n = len(self.dowker)

        if x < 1:            #If crossing being checked is below 1, wraps to top of dowker code
            x = 2 * n + x
        elif x >  2 * n:               #If crossing being checked above biggest # in dowker code, wraps back to 1
            x = x - 2 * n
        if x % 2 == 0:       #If x is even
            index = self.dowker.index(x)             #Finds index of even number in dowker code
            odd = 2 * index + 1            #Constructs odd number corresponding to the even x    
            if sequence1[0] - 1 == odd:              #Checks if before sequence1 matches crossing
                return True, odd
            elif sequence2[0] - 1 == odd:            #Checks if before sequence2 matches crossing
                return True, odd
            elif sequence1[-1] + 1 == odd:               #Checks if after sequence1 matches crossing
                return True, odd
            elif sequence2[-1] + 1 == odd:               #Checks if after sequence2 matches crossing
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
            elif sequence1[-1] + 1 == self.dowker[index]:            #Checks if after sequence1 matches crossing
                return True, odd
            elif sequence2[-1] + 1 == self.dowker[index]:          #Checks if after sequence2 matches crossing
                return True, odd
            else:
                return False, odd              #If no matches return false

    def flype_appendage(flag, flypes, crossing, sequence1, sequence2):
        """
        Builds a flype triple if the given crossing is valid and not already recorded.

        Args:
            flag (bool): Whether the crossing is valid.
            flypes (list): Existing list of flypes.
            crossing (int): The adjacent crossing to the tangle.
            sequence1 (list): First half of the tangle.
            sequence2 (list): Second half of the tangle.

        Returns:
            list: A flype [sequence1, sequence2, crossing] if valid, 
                otherwise an empty list.
        """
        newflype = []            #Creates a list of a flype to add to list of flypes
        if flag:         #Checks if flype is to be added
            if len(flypes) == 0:               #Always adds flype if one to be added and none yet in list
                newflype.append(sequence1)              #Adds two sequences and crossing to newflype
                newflype.append(sequence2)
                newflype.append(crossing)
            else:
                flypes = [flype for flype in flypes if len(flype) != 0]
                for flype in flypes:            #Avoids adding two duplicate flypes to list when x and y indices are flipped in flype_detect()
                        if sequence1 == flype[0] or sequence1 == flype[1]:
                            if sequence2 ==flype[0] or sequence2 == flype[1]:
                                if crossing == flype[2]:
                                    return newflype
                newflype.append(sequence1)              #Adds two sequences and crossing to new flype
                newflype.append(sequence2)
                newflype.append(crossing)
        return newflype     

    def make_lexographic(self):
        """
        Converts the Dowker code into its lexicographically minimal form by rotating and correcting traversal direction.

        Returns:
            list: A new Dowker code representing the canonical form.
        """
        n = len(self.dowker)
        distances = []
        dowker = []

        for crossing in range(n):
            odd = 2 * crossing + 1
            even = self.dowker[crossing]
            diffforward = np.abs(odd - even)
            diffbackward = 2 * n - diffforward
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
        
        for crossing in range(n):
            oldodd = 2 * crossing + 1
            newfromodd = oldodd - correction
            if newfromodd < 1:
                newfromodd = 2 * n - np.abs(newfromodd)
            oldeven = self.dowker[crossing]
            newfromeven = oldeven - correction
            if newfromeven < 1:
                newfromeven = 2 * n - np.abs(newfromeven)
            newfromodds.append(newfromodd)
            newfromevens.append(newfromeven)
        
        for crossing in range(n):
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
        """
        Applies a flype transformation to the current knot graph.

        Edits the underlying graph to swap tangle segments around a valid 
        flype crossing, and reconstructs the Dowker code.

        Args:
            flype (list): A flype triple [sequence1, sequence2, crossing].

        Returns:
            list: The Dowker code after the flype is performed and re-normalized.
        """
        G = Knot.graphify_dowker(self)
        #net.draw(G, with_labels = True)
        #plt.show()
        tangle_edge_edit = []
        crossing_edge_edit = []
        sequence1min = flype[0][0]
        sequence2min = flype[1][0]
        sequence1max = flype[0][len(flype[1]) - 1]
        sequence2max = flype[1][len(flype[1]) - 1]
        crossing_odd = flype[2]
        index_odd = int((crossing_odd - 1)/2)
        crossing_even = self.dowker[index_odd]
        tangle_edge_edit.append(AlternatingKnot.edge_identification(self, sequence1min, False))
        tangle_edge_edit.append(AlternatingKnot.edge_identification(self, sequence2min, False))
        tangle_edge_edit.append(AlternatingKnot.edge_identification(self, sequence1max, True))
        tangle_edge_edit.append(AlternatingKnot.edge_identification(self, sequence2max, True))
        crossing_edge_edit.append(AlternatingKnot.edge_identification(self, crossing_odd, True))
        crossing_edge_edit.append(AlternatingKnot.edge_identification(self, crossing_odd, False))
        crossing_edge_edit.append(AlternatingKnot.edge_identification(self, crossing_even, True))
        crossing_edge_edit.append(AlternatingKnot.edge_identification(self, crossing_even, False))
        for edgecross in crossing_edge_edit:
            for edgetang in tangle_edge_edit:
                if edgetang == 0 or edgecross == 0:
                    pass
                elif set(edgecross) == set(edgetang):
                    index = crossing_edge_edit.index(edgecross)
                    crossing_edge_edit[index] = 0
                    index = tangle_edge_edit.index(edgetang)
                    tangle_edge_edit[index] = 0
        crossing_edge_edit = Knot(crossing_edge_edit).zero_remove()
        tangle_edge_edit = Knot(tangle_edge_edit).zero_remove()
        for edge in tangle_edge_edit:
                edgetuple = (edge[0], edge[1])
                if edgetuple in G.edges and edge not in crossing_edge_edit:
                        G.remove_edge(edge[0], edge[1])
        for edge in crossing_edge_edit:
            edgetuple = (edge[0], edge[1])
            if edgetuple in G.edges:
                G.remove_edge(edge[0], edge[1])
        #net.draw(G, with_labels = True)
        #plt.show()
        if len(flype[0]) % 2 == 0: # If there are an even number of crossings inside flype
            if crossing_edge_edit[0][0] % 2 == tangle_edge_edit[0][0] % 2:
                G.add_edge(crossing_edge_edit[0][0], tangle_edge_edit[0][1])
                G.add_edge(tangle_edge_edit[0][0], crossing_edge_edit[0][1])
                G.add_edge(crossing_edge_edit[1][0], tangle_edge_edit[1][1])
                G.add_edge(tangle_edge_edit[1][0], crossing_edge_edit[1][1])
            else:
                G.add_edge(crossing_edge_edit[0][0], tangle_edge_edit[1][1])
                G.add_edge(tangle_edge_edit[0][0], crossing_edge_edit[1][1])
                G.add_edge(crossing_edge_edit[1][0], tangle_edge_edit[0][1])
                G.add_edge(tangle_edge_edit[1][0], crossing_edge_edit[0][1])
        else:
            if crossing_edge_edit[0][0] % 2 == tangle_edge_edit[0][0] % 2:
                G.add_edge(crossing_edge_edit[0][0], tangle_edge_edit[1][1])
                G.add_edge(tangle_edge_edit[0][0], crossing_edge_edit[1][1])
                G.add_edge(crossing_edge_edit[1][0], tangle_edge_edit[0][1])
                G.add_edge(tangle_edge_edit[1][0], crossing_edge_edit[0][1])
            else:
                G.add_edge(crossing_edge_edit[0][0], tangle_edge_edit[0][1])
                G.add_edge(tangle_edge_edit[0][0], crossing_edge_edit[0][1])
                G.add_edge(crossing_edge_edit[1][0], tangle_edge_edit[1][1])
                G.add_edge(tangle_edge_edit[1][0], crossing_edge_edit[1][1])
        #net.draw(G, with_labels = True)
        #plt.show()
        dowker = Knot.dowkerify_graph(self, G)
        dowker = AlternatingKnot.make_lexographic(Knot(dowker))
        return dowker   

    def edge_identification(self, number, max):
        """
        Identifies the graph edge corresponding to a given crossing.

        Args:
            number (int): The crossing number (odd or even).
            is_end_of_tangle (bool): Whether this is the trailing end of a tangle.

        Returns:
            list: A two-element list representing the edge as [node1, node2].
        """
        n = len(self.dowker)
        edge = []

        if number % 2 == 0: 
            index = self.dowker.index(number)
            if max:
                node1 = (4 * index) + 3
                next = number + 1
                if next > 2 * n:
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
            if max:
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
                        before = 2 * n
                beforeindex = self.dowker.index(before)
                node2 = (4 * beforeindex) + 3
                edge.append(node1)
                edge.append(node2)
        return edge

    def find_flype_class(self, oldcheckedcodes):
        """
        Recursively computes the flype equivalence class of a knot.

        Applies all valid flypes to the current knot and gathers all 
        Dowker codes reachable through flypes.

        Args:
            oldcheckedcodes (list): A list of Dowker codes already known 
                                    to be in the same flype class.

        Returns:
            list: A complete list of Dowker codes in the flype class.
        """
        # created checked list, adding current knot
        checked = oldcheckedcodes + [self.dowker]
        checked = [x for n,x in enumerate(checked) if x not in checked[:n]] # removes duplicates
        
        # find all flypes and flype codes
        flypes = AlternatingKnot.flype_detect(self)

        flype_codes = []
        for flype in flypes:
            flype_codes.append(AlternatingKnot.perform_flype(self, flype))
        flype_codes = [x for n,x in enumerate(flype_codes) if x not in flype_codes[:n]] # removes duplicates


        # check if flype codes are already in checked list
        comparison = checked + flype_codes
        comparison = [x for n,x in enumerate(comparison) if x not in comparison[:n]] # removes duplicates
        
        if comparison == checked: # no new flype codes
            return checked
        else: # new flype codes found
            for code in flype_codes:
                if code not in checked:
                    checked = AlternatingKnot.find_flype_class(Knot(code), checked) # recursively compute flype class of new codes
            return checked
        
    def compute_flype_minimals(permutations):
        final_list = []

        for permutation in permutations:
            if permutation in permutations:
                flypeclass = AlternatingKnot.find_flype_class(AlternatingKnot(permutation), [permutation]) 
                permutations = [perm for perm in permutations if perm not in flypeclass] # removes all permutations that are in the flypeclass
                
                # deletes all flypes in flype class and finds the lexographically minimal code, stored in AlternatingKnot(flypeclass)[0]???
                for x in range(len(permutation)):
                        integers = []
                        for flype in flypeclass:
                            if flype != 0:
                                integers.append(flype[x])
                            else:
                                integers.append(2 * len(permutation) + 1)
                        minimum = min(integers)
                        for y in range(len(integers)):
                            if flypeclass[y] != 0:
                                if integers[y] != minimum:
                                    flypeclass[y] = 0

                final_list.append(AlternatingKnot.zero_remove(AlternatingKnot(flypeclass))[0]) # append the lexographically minimal code of its flype class to the final list
        
        final_list = [x for n, x in enumerate(final_list) if x not in final_list[:n]] # removes duplicates

        return final_list