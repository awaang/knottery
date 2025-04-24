import itertools
import numpy as np
import networkx as net

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
          
     def __str__(self):
          return f"{self.dowker}"
          
def genDowkers(crossings):   #Generates all the possible dowker codes with up to n crossings
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