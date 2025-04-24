from knot import Knot, genDowkers
from alternating_knot import AlternatingKnot

trefoil = AlternatingKnot([6, -10, 12, 4, -8, 2, 14])
square = AlternatingKnot([6, 8, 2, 4])
falsesquare = AlternatingKnot([6, -8, -2, -4])
typeIIItrefoil = AlternatingKnot([12, -16, -18, -14, 6, 4, 8, 2, -10])
impossible1 = AlternatingKnot([4, 6, 8, 2])
lexographic1 = AlternatingKnot([10, 6, 2, 4, 8, 12])
lexographic2 = AlternatingKnot([4, 6, 2, 10, 12, 8])
comptrefoils = AlternatingKnot([4, 12, 2, 10, 6, 8])
typeItrefoil = AlternatingKnot([6, 4, 8, 2])
sixthree = AlternatingKnot([4, 8, 10, 2, 12, 6])
sixone = AlternatingKnot([4, 8, 12, 10, 2, 6])

print("Dowker Generation 3 crossings:\n", genDowkers(3))
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
print("TypeIIItrefoil III:", AlternatingKnot.signflip(Knot(typeIIItrefoil.typeIII())))
print("TypeIIItrefoil:", typeIIItrefoil.zeroremove())
print("\n")
print("Impossible1:", impossible1.dowker)
var = impossible1.isPossible()
if var == True:
     print("SquarePoss: True")
else:
     print("SquarePoss: False")
print("\n")
print("Lexographic1:", lexographic1.dowker)
var = lexographic1.isLexographic()
if var == True:
     print("Lexographic1: True")
else:
     print("Lexographic1: False")
print("Lexographic2:", lexographic2.dowker)
var = lexographic2.isLexographic()
if var == True:
     print("Lexographic2: True")
else:
     print("Lexographic2: False")
print("\n")
var = comptrefoils.isPrime()
if var == True:
     print("Comptrefoils: Prime")
else:
     print("Comptrefoils: Composite")
var = typeItrefoil.isPrime()
if var == True:
     print("TypeItrefoil: Prime")
else:
     print("TypeItrefoil: Composite")
var = square.isPrime()
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
print("Make lexo:", [6, 8, 10, 2, 12, 4], "to", AlternatingKnot.makelexographic(Knot([6, 8, 10, 2, 12, 4])))
print("\n")
print("**Six Three Flyping Tangle [2, 3], [7, 8] and Crossing 1**")
print("Six Three Before:")
print(sixthree.dowker)
print("Six Three After:")
print(AlternatingKnot.performflype(sixthree, [[2, 3], [7, 8], 1]))

# performflype() manual testing

# flypes = AlternatingKnot.flypedetect(AlternatingKnot(permutation))
# flypeclass = []
# for flype in flypes:
     # newcode = AlternatingKnot.performflype(AlternatingKnot(permutation), flype)
     # flypeclass.append(newcode)
# print(permutation, "... CODES:", flypeclass, "\n\n")