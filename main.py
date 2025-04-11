import itertools
from knot import Knot

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

#####TESTS#####

trefoil = Knot([6, -10, 12, 4, -8, 2, 14])
square = Knot([6, 8, 2, 4])
falsesquare = Knot([6, -8, -2, -4])
typeIIItrefoil = Knot([12, -16, -18, -14, 6, 4, 8, 2, -10])
impossible1 = Knot([4, 6, 8, 2])
lexographic1 = Knot([10, 6, 2, 4, 8, 12])
lexographic2 = Knot([4, 6, 2, 10, 12, 8])
comptrefoils = Knot([4, 12, 2, 10, 6, 8])
typeItrefoil = Knot([6, 4, 8, 2])
sixthree = Knot([4, 8, 10, 2, 12, 6])
sixone = Knot([4, 8, 12, 10, 2, 6])

print("#####TESTS#####\n")
print("Dowker Generation 3 crossings:\n", gendowkers(3))
print("\n")
print("Trefoil:", trefoil.dowker)
print("trefoilI:", trefoil.typeI())
print("trefoilII:", trefoil.typeII())
print("Trefoil:", trefoil.zeroremove())
print("\n")
print("Square:", square.dowker)
print("SquareI:", square.typeI())
print("SquareII:", square.typeII())
print("Square:", square.zeroremove())
print("\n")
print("False Sqaure:", falsesquare.dowker)
print("False SquareI:", falsesquare.typeI())
print("False SquareII:", falsesquare.typeII())
print("False Square:", falsesquare.zeroremove())
print("\n")
print("TypeIIItrefoil:", typeIIItrefoil.dowker)
print("TypeIIItrefoil III:", Knot.signflip(Knot(typeIIItrefoil.typeIII())))
print("TypeIIItrefoil:", typeIIItrefoil.zeroremove())
print("\n")
print("Impossible1:", impossible1.dowker)
var = impossible1.dowkerpossible()
if var == True:
     print("SquarePoss: True")
else:
     print("SquarePoss: False")
print("\n")
print("Lexographic1:", lexographic1.dowker)
var = lexographic1.DowkerIsLexographic()
if var == True:
     print("Lexographic1: True")
else:
     print("Lexographic1: False")
print("Lexographic2:", lexographic2.dowker)
var = lexographic2.DowkerIsLexographic()
if var == True:
     print("Lexographic2: True")
else:
     print("Lexographic2: False")
print("\n")
var = comptrefoils.prime()
if var == True:
     print("Comptrefoils: Prime")
else:
     print("Comptrefoils: Composite")
var = typeItrefoil.prime()
if var == True:
     print("TypeItrefoil: Prime")
else:
     print("TypeItrefoil: Composite")
var = square.prime()
if var == True:
     print("Square: Prime")
else:
     print("Square: Composite")
print("\n")
print("Square:", square.dowker)
print("SquareColor:", square.colorability())
print("\n")
print("6:3 knot flypes:", sixthree.flypedetect())
print("6:1 knot flypes:", sixone.flypedetect())
print("\n")
print("Make lexo:", [6, 8, 10, 2, 12, 4], "to", Knot.makelexographic(Knot([6, 8, 10, 2, 12, 4])))
print("\n")
print("**Six Three Flyping Tangle [2, 3], [7, 8] and Crossing 1**")
print("Six Three Before:")
print(sixthree.dowker)
print("Six Three After:")
print(Knot.performflype(sixthree, [[2, 3], [7, 8], 1]))


###MAIN###

def main():
     print("\n\n#####MAIN#####\n\n")
     permutations = gendowkers(7) #AT 8 THERE ARE 17 non prime knots included atm
     for i in range(len(permutations)):
          if Knot(permutations[i]).DowkerIsLexographic() == False:
               permutations[i] = 0
          elif Knot(permutations[i]).prime() == False:
               permutations[i] = 0 
          elif Knot(permutations[i]).dowkerpossible() == False:
               permutations[i] = 0
     permutations = Knot(permutations).zeroremove()
     finallist = []
     flypes = []
     for permutation in permutations:
          if permutation in permutations:
               flypeclass = Knot.findflypeclass(Knot(permutation), [permutation])
               permutations = [perm for perm in permutations if perm not in flypeclass] 
               lexographic = []
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
               finallist.append(Knot.zeroremove(Knot(flypeclass))[0]) 
     finallist = [x for n,x in enumerate(finallist) if x not in finallist[:n]]  
     print("FINAL LIST:")
     for knot in range(len(finallist)):
          print(finallist[knot])
     print(len(finallist), "Knots")

if __name__ == "__main__":
    main()



    #flypes = Knot.flypedetect(Knot(permutation))
    #flypeclass = []
    #for flype in flypes:
          #newcode = Knot.performflype(Knot(permutation), flype)
          #flypeclass.append(newcode)
    #print(permutation, "... CODES:", flypeclass, "\n\n")



#Find order 1 flype permutations from given permutation, then see if self contained, keep going
#Check only the permutations that are not self contained
#Check each "tree" from each dowker code
#Use sorting algorithm to determine lexographically minimal code
#Eliminate self contained list of flypes from permutatiohs, add lexographically minimal code to a list (Final list)

#### More testing ####