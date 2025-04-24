import itertools
import numpy as np
import networkx as net
import matplotlib.pyplot as plt

class Knot:
     def __init__(self, dowker):
        self.dowker = dowker  
    
     def typeI(self):
          zeroes = 0 # tracks how many entries have been removed (set to 0)

          for x in range(len(self.dowker)):
               even = np.abs(self.dowker[x]) # stores magnitude of index
               
               if even == 0:
                    zeroes += 1
                    continue
               
               # calculate the corresponding odd number based on current index, adjusted for removed entries
               odd = 2 * (x - zeroes) + 1

               # check for Type I Reidemeister move
               if even == odd + 1 or even == odd - 1 and even != 0: # crossing pair consists of consecutive integers
                    # remove crossing
                    self.dowker[x] = 0
                    zeroes += 1
                    
                    # adjust the dowker code for the removed crossing
                    for x in range(len(self.dowker)):
                         if np.abs(self.dowker[x]) > even: 
                              self.dowker[x] = Knot.reidreadjust(self.dowker[x])

          return self.dowker
    
     def typeII(self):
          zeroes_x = 0 # tracks removed entries in primary loop

          for x in range(len(self.dowker)):
               even_x = np.abs(self.dowker[x])

               # adjust odd part for skipped (zeroed) entries
               odd_x = 2 * (x - zeroes_x) + 1
               zeroes_y = 0 # tracks removed entries in nested loop

               for y in range(len(self.dowker)):
                    even_y = np.abs(self.dowker[y])
                    if even_y == 0:
                         zeroes_y += 1
                         continue
                    
                    # adjust odd part for skipped entries
                    odd_y = 2 * (y - zeroes_y) + 1

                    # check for valid Type II move (two adjacent opposite crossings)
                    flag1, flag2 = False, False
                    if odd_y == even_x - 1 and even_y == odd_x + 1 and even_y != even_x and self.dowker[x] * self.dowker[y] < 0 and even_x != 0 and even_y != 0:
                         flag1 = True         
                    if odd_y == even_x + 1 and even_y == odd_x - 1 and even_y != even_x and self.dowker[x] * self.dowker[y] < 0 and even_x != 0 and even_y != 0:
                         flag2 = True
                    
                    if flag1 or flag2: 
                         self.dowker[x] = 0 
                         self.dowker[y] = 0
                         zeroes_y += 1  
                         zeroes_x += 1

                         # adjust the dowker code for the removed crossings
                         for z in range(len(self.dowker)):
                              even_z = np.abs(self.dowker[z])
                              if even_x > even_y:        
                                   if even_z > even_x:
                                        self.dowker[z] = Knot.reidreadjust(self.dowker[z])              
                                   if even_z > even_y:
                                        self.dowker[z] = Knot.reidreadjust(self.dowker[z])
                                        
                              else:
                                   if even_z > even_y:
                                        self.dowker[z] = Knot.reidreadjust(self.dowker[z])
                                   if even_z > even_x:
                                        self.dowker[z] = Knot.reidreadjust(self.dowker[z])
                         
                         # update even_x after removal
                         even_x = self.dowker[x]
          
          return self.dowker
    
     def typeIII(self):
          self.dowker = Knot.typeII(Knot(self.dowker))           #Performs type I, II moves to simplify knot first
          self.dowker = Knot.typeI(Knot(self.dowker))
          self.dowker = Knot.zeroremove(Knot(self.dowker))
          for x in range(len(self.dowker)):            #Primary iteration through knot
               even_x = np.abs(self.dowker[x])               #Stores primary even # magnitude
               odd_x = 2 * x + 1              #Stores primary odd #
               for y in range(len(self.dowker)):            #Secondary iteration through knot
                    even_y = np.abs(self.dowker[y])               #Stores secondary even # magnitude
                    odd_y = 2 * y + 1              #Stores secondary odd #
                    for z in range(len(self.dowker)):            #Tertiary iteration through knot
                         even_z = np.abs(self.dowker[z])               #Stores tertiary even # magnitude
                         odd_z = 2 * z + 1              #Stores tertiary odd #
                         flag, dir = Knot.typeIIIflag(odd_x, odd_y, odd_z, self.dowker[x], self.dowker[y], self.dowker[z])             #Checks for type III criterion
                         if flag and Knot.typeIIIindex(even_x, even_y, even_z):              #Handles 0s and same indexes on iterations
                              lenbf = len(Knot.zeroremove(Knot(self.dowker)))             #Checks length of code with 0s removed
                              dowkerIII = []
                              for i in range(len(self.dowker)):
                                   dowkerIII.append(self.dowker[i])
                              #print(dowkerIII)
                              if dir == True:
                                   #print("dir True")
                                   dowkerIII[x] = self.dowker[z]           #Swapping of three crossings to perform type III
                                   #print(dowkerIII, self.dowker)
                                   dowkerIII[y] = self.dowker[x]
                                   #print(dowkerIII, self.dowker)
                                   dowkerIII[z] = self.dowker[y]
                                   #print(dowkerIII, self.dowker)
                              else:
                                   #print("dir False")
                                   dowkerIII[x] = self.dowker[y]           #Swapping of three crossings to perform type III
                                   dowkerIII[y] = self.dowker[z]
                                   dowkerIII[z] = self.dowker[x]
                              #print("Final III:", dowkerIII)
                              #print("x:", x, "y:", y, "z:", z)
                              dowkerIII = Knot.typeIIIsigns(x, y, z, dowkerIII)           #Handles sign swapping for type III
                              #print("signs:", dowkerIII)
                              dowkerIII = Knot.typeII(Knot(dowkerIII))               #Performs types I and II on knot after type III
                              #print("II:", dowkerIII)
                              dowkerIII = Knot.typeI(Knot(dowkerIII))
                              #print("I:", dowkerIII)
                              dowker_store = []
                              for i in range(len(dowkerIII)):
                                   dowker_store.append(dowkerIII[i])
                              dowkerIII = Knot.zeroremove(Knot(dowkerIII))           #Removes zeroes from code after type I, II move
                              lenaf = len(Knot.zeroremove(Knot(dowkerIII)))               #Checks if type III move resulted in more opportunities for type II, II
                              if lenaf < lenbf:             #If type III move resulted in more opportunities, assign new code to self.dowker
                                   self.dowker = dowker_store
          return self.dowker

     def typeIIIflag(odd_x, odd_y, odd_z, even_x, even_y, even_z):
          dir = True  # direction flag for how to rotate the three crossings

          # take absolute values of even parts for comparison
          abs_even_x = np.abs(even_x)
          abs_even_y = np.abs(even_y)
          abs_even_z = np.abs(even_z)

          # require at least one crossing to differ in sign (Type III needs mix of over/under)
          if even_x * even_y < 0 or even_y * even_x < 0 or even_z * even_x < 0:
               # check first valid configuration for adjacent values
               if (
                    np.abs(odd_x - abs_even_y) == 1 and
                    np.abs(odd_y - abs_even_z) == 1 and
                    np.abs(odd_z - abs_even_x) == 1
               ):
                    return True, dir  # valid move in standard direction

               # check second valid configuration (reverse rotation)
               elif (
                    np.abs(odd_x - abs_even_z) == 1 and
                    np.abs(odd_y - abs_even_x) == 1 and
                    np.abs(odd_z - abs_even_y) == 1
               ):
                    dir = False
                    return True, dir  # valid move in reverse direction

               # pattern doesn't match any valid Type III setup
               else:
                    return False, dir
          else:
               return False, dir  # all crossings have the same sign, invalid
              
     def typeIIIindex(even_x, even_y, even_z): # handles same iteration indexes and zeroes
          # ensure all three crossings are at distinct indices
          if even_x != even_y and even_y != even_z and even_z != even_x:
               # ensure none of the crossings are removed (i.e., not zeroed)
               if even_x != 0 and even_y != 0 and even_z != 0:
                    return True
          return False
     
     def typeIIIsigns(x, y, z, dowker): # handles swapping of signs
               #print(dowker[x], dowker[y], dowker[z])
               if dowker[x] * dowker[y] < 0:           #If x, y diff sign, then opposite z crossing sign
                    dowker[z] = dowker[z] * -1
               elif dowker[y] * dowker[z] < 0:              #If y, z diff sign, then opposite x crossing sign
                    dowker[x] = dowker[x] * -1
               else:               #If x, z diff sign, then opposite y crossing sign
                    dowker[y] = dowker[y] * -1
               return dowker                 
    
     def reidreadjust(entry):       #Helper to readjust dowker code appropriately for signage after reid move
          if entry > 0:
               entry = entry - 2
          else:
               entry = entry + 2
          return entry

     def colorability(self):
          matrix = []
          for x in range(len(self.dowker) - 1):           #Iterate through dowker code
               understrand1 = x           #First understrand assignment determined by index in dowker code       
               understrand2 = x - 1       #Second understrand assignment is understrand before it
               if understrand2 == -1:         #Sets understrand 0 back to n - 1
                    understrand2 = len(self.dowker) - 1    
               crossing = 2 * x + 2          
               overstrand = self.dowker.index(crossing) - 1           #Locates index in dowker code where strand containing odd part of dowker code is, sets overstrand assignment
               if overstrand == -1:           #Sets overstrand 0 back to n -1
                    overstrand = len(self.dowker) - 1
               equation = []
               for x in range(len(self.dowker) - 1):          #Iterates elements to matrix row
                    if x == understrand1 or x == understrand2:            #Inserts 1 for understrands in correct position
                         equation.append(1)       
                    elif x == overstrand:
                         equation.append(-2)          #Inserts -2 for overstrand in correct position
                    else:
                         equation.append(0)           #Inserts 0 when position matches neither understrands or overstrand
               matrix.append(equation)            #Adds row to matrix
          det = np.linalg.det(np.matrix(matrix)) 
          det = int(np.abs(det))    
          return det
    
     def listremove(lst):
         lst = [n for n in lst if len(n) != 0]
         return lst
    
     def zeroremove(self):               #Removes 0s from dowker codes
         self.dowker = [n for n in self.dowker if n != 0]
         return self.dowker
    
     def signflip(self):       #Used when all crossings on knot are negative
         flip = True
         for n in range(len(self.dowker)):
              if self.dowker[n] > 0:
                   flip = False
         if flip == True:
              for n in range(len(self.dowker)):
                   self.dowker[n] = self.dowker[n] * -1
         return self.dowker
    
     def dowkerpossible(self):      #Tests for impossible dowker codes, returning False for impossible dowker codes
         G = Knot.graphifydowker(self)
         var = net.is_planar(G)              #Checks for planarity
         return var
    
     def DowkerIsLexographic(self):
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
    
     def prime(self):
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
    
     def flypedetect(self):
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
                              flag, crossing = Knot.flypecrossing(self, sequence1[0] - 1, sequence1, sequence2)         #Finds a crossing before start of first sequence
                              flypes.append(Knot.flypeappendage(flag, flypes, crossing, sequence1, sequence2))          #Appends tangle and crossing if possible flype
                              flag, crossing = Knot.flypecrossing(self, sequence2[0] - 1, sequence1, sequence2)         #Finds a crossing before start of second sequence
                              flypes.append(Knot.flypeappendage(flag, flypes, crossing, sequence1, sequence2))               
                              flag, crossing = Knot.flypecrossing(self, sequence1[len(sequence1) - 1] + 1, sequence1, sequence2)            #Finds a crossing after end of first sequence
                              flypes.append(Knot.flypeappendage(flag, flypes, crossing, sequence1, sequence2))
                              flag, crossing = Knot.flypecrossing(self, sequence2[len(sequence2) - 1] + 1, sequence1, sequence2)            #Finds a crossing after end of second sequence
                              flypes.append(Knot.flypeappendage(flag, flypes, crossing, sequence1, sequence2))
                              flypes = Knot.listremove(flypes)             #Removes all lists added through flypeappendage()
         for i in range(len(flypes)):             #Removes the case of crossing for flype detected inside tangle
              if flypes[i][2] in flypes[i][0] or flypes[i][2] in flypes[i][1]:
                    flypes[i] = 0
              elif len(flypes[i][0]) == len(self.dowker) - 1:
                    flypes[i] = 0
         flypes = Knot(flypes).zeroremove()            #For formatting
         return flypes
     
     def flypecrossing(self, x, sequence1, sequence2):
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

     def flypeappendage(flag, flypes, crossing, sequence1, sequence2):
          newflype = []            #Creates a list of a flype to add to list of flypes
          if flag == True:         #Checks if flype is to be added
               if len(flypes) == 0:               #Always adds flype if one to be added and none yet in list
                    newflype.append(sequence1)              #Adds two sequences and crossing to newflype
                    newflype.append(sequence2)
                    newflype.append(crossing)
               else:
                    flypes = Knot.listremove(flypes)
                    for flype in flypes:            #Avoids adding two duplicate flypes to list when x and y indices are flipped in flypedetect()
                         if sequence1 == flype[0] or sequence1 == flype[1]:
                              if sequence2 ==flype[0] or sequence2 == flype[1]:
                                   if crossing == flype[2]:
                                        return newflype
                    newflype.append(sequence1)              #Adds two sequences and crossing to new flype
                    newflype.append(sequence2)
                    newflype.append(crossing)
          return newflype     

     def flypelexographic(self, flypeddowker, permutations):
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
    
     def makelexographic(self):
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
    
     def performflype(self, flype):
         startingdowker = self.dowker
         G = Knot.graphifydowker(self)
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
         tangleedgeedit.append(Knot.edgeidentification(self, sequence1min, False))
         tangleedgeedit.append(Knot.edgeidentification(self, sequence2min, False))
         tangleedgeedit.append(Knot.edgeidentification(self, sequence1max, True))
         tangleedgeedit.append(Knot.edgeidentification(self, sequence2max, True))
         crossingedgeedit.append(Knot.edgeidentification(self, crossingodd, True))
         crossingedgeedit.append(Knot.edgeidentification(self, crossingodd, False))
         crossingedgeedit.append(Knot.edgeidentification(self, crossingeven, True))
         crossingedgeedit.append(Knot.edgeidentification(self, crossingeven, False))
         for edgecross in crossingedgeedit:
              for edgetang in tangleedgeedit:
                   if edgetang == 0 or edgecross == 0:
                        pass
                   elif set(edgecross) == set(edgetang):
                        index = crossingedgeedit.index(edgecross)
                        crossingedgeedit[index] = 0
                        index = tangleedgeedit.index(edgetang)
                        tangleedgeedit[index] = 0
         crossingedgeedit = Knot(crossingedgeedit).zeroremove()
         tangleedgeedit = Knot(tangleedgeedit).zeroremove()
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
         dowker = Knot.dowkerifygraph(self, G)
         dowker = Knot.makelexographic(Knot(dowker))
         return dowker   

     def edgeidentification(self, number, max):
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
     
    
     def graphifydowker(self):
         G = net.Graph()
         crossings = len(self.dowker) # # of crossings for indexing
         for x in range(4 * crossings):
              G.add_node(x + 1)         #Replicates the four vertices of each crossing
         for y in range(crossings):          #Creates the edges of each of the crossings
              for z in range(4):
                   if z != 3:
                         node1 = (4 * y) + z + 1
                         node2 = (4 * y) + z + 2
                         #print("Crossing square:", node1, node2)
                         G.add_edge(node1, node2)
                   else:           #For edge (4, 1) for example (see attached image)
                         node1 = (4 * y) + z + 1
                         node2 = (4 * y) + 1
                         #print("Crossing square:", node1, node2)
                         G.add_edge(node1, node2)
         for w in range(crossings):
              node1 = 4 * (w + 1)       #Starts at odd node
              odd = (2 * w) + 1         #Replicates odd number at index in dowker code
              evenindex = self.dowker.index(odd + 1)           #Finds next even's index in dowker code
              node2 = (evenindex * 4) + 1         #Finds next even in dowker codes node based on index
              #print("Odd to even:", node1, node2)
              G.add_edge(node1, node2)       #Handles odd to even edges of dowker code
              even = self.dowker[w]          #Finds even number at index
              node1 = (4 * w) + 3            #Starts at even node of index
              if even != crossings * 2:
                    node2 = (even * 2) + 2             #Finds next odd node
              else:
                    node2 = 2
              #print("Even to odd:", node1, node2)
              G.add_edge(node1, node2)            #Handles even to odd edges of dowker code
         return G
    
     def dowkerifygraph(self, G):
         node = 4
         dowker = []
         dowkeroddindex = []
         dowkerevenindex = []
         for x in self.dowker:
              dowker.append(0)
              dowkeroddindex.append(0)
              dowkerevenindex.append(0)
         for x in range(len(self.dowker)):
              for y in range(2):
                    edges = G.edges(node)
                    for edge in edges:
                         if edge[0] == node:
                              if (edge[1] - 1)//4 != (node - 1)//4:
                                   node = edge[1]
                         else: 
                              if (edge[0] - 1)//4 != (node - 1)//4:
                                   node = edge[0]
                    if node % 4 == 0 or node % 4 == 3:
                         node -= 2
                    else: 
                         node += 2
                    if y == 0:
                         dowkerevenindex[x] = (node -1)//4
                    else:
                         if x != len(self.dowker) - 1:
                              dowkeroddindex[x + 1] = (node - 1)//4
         #print(dowkerevenindex)
         #print(dowkeroddindex)
         for x in range(len(self.dowker)):
              oddindex = dowkeroddindex[x]
              evenindex = dowkerevenindex.index(oddindex)
              even = 2 * (evenindex + 1)
              dowker[x] = even
         return dowker
    
     def findflypeclass(self, oldcheckedcodes):
          flypes = Knot.flypedetect(self)
          checked = []
          checked = checked + oldcheckedcodes
          checked.append(self.dowker)
          checked = [x for n,x in enumerate(checked) if x not in checked[:n]]
          codesfromflypes = []
          for flype in flypes:
               newcode = Knot.performflype(self, flype)
               codesfromflypes.append(newcode)
          codesfromflypes = [x for n,x in enumerate(codesfromflypes) if x not in codesfromflypes[:n]]
          comparison = checked + codesfromflypes
          comparison = [x for n,x in enumerate(comparison) if x not in comparison[:n]]
          if comparison == checked:
               return checked
          else:
               for code in codesfromflypes:
                    if code not in checked:
                         checked = Knot.findflypeclass(Knot(code), checked)
               return checked
          
def gendowkers(crossings):   #Generates all the possible dowker codes with up to n crossings
     numbers = []           #Used as a list of even numbers in dowker code up to n crossings
     #permut = []              #Used for all permutations of even numbers
     permutneg = []           #Used for all permutations of even numbers w signs included
     for x in range(crossings):         #Iterates through each # of crossings
          number = 2 * (x + 1)               #Generates even number to add to list
          numbers.append(number)                  #Appends even number to list of even #s
          if x > 1:           #Excludes dowker codes with length less than 3
               permutstor = list(itertools.permutations(numbers))          #Generates the permnutations using the list of even numbers for # of crossings
               for i in range(len(permutstor)):
                    permutneg.append(permutstor[i])            #Adds to list of permutations of each # of crossings
     for y in range(len(permutneg)):
          permutneg[y] = list(permutneg[y])
     #for dowkers in permut:             #Iterates over all dowker codes generated
          #permutstor = []
          #for num in dowkers:
               #permutstor.append(num)             #Stores each dowker code in format for itertools.product            
          #permutneg.append(list(itertools.product(*([y, -y] for y in permutstor))))            #Uses dot product to generate neg and positive permutations
     return permutneg              #Returns list of permutations w signs included