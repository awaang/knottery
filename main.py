from knot import Knot, gendowkers

# Notes:
# - Find order 1 flype permutations from given permutation, then see if self contained, keep going
# - Check only the permutations that are not self contained
# - Check each "tree" from each dowker code
# - Use sorting algorithm to determine lexographically minimal code
# - Eliminate self contained list of flypes from permutations, add lexographically minimal code to a list (Final list)

# - at 8 crossings, there are 17 non prime knots included atm

def main():
     permutations = gendowkers(8)
     
     for i in range(len(permutations)):
          if Knot(permutations[i]).DowkerIsLexographic() == False: # criteria 1: checks if the dowker code is lexographically minimal
               permutations[i] = 0
          elif Knot(permutations[i]).prime() == False: # criteria 2: checks if the dowker code is prime
               permutations[i] = 0 
          elif Knot(permutations[i]).dowkerpossible() == False: # criteria 3: checks if the dowker code is possible
               permutations[i] = 0
     
     permutations = Knot(permutations).zeroremove() # remove all zeroed permutations

     finallist = []
     flypes = []

     # criteria 4: checks if the dowker code is minimal with respect to flyping
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
     
     finallist = [x for n,x in enumerate(finallist) if x not in finallist[:n]] # removes duplicates
     
     for knot in range(len(finallist)):
          print(finallist[knot])
     print(len(finallist), "Knots")

if __name__ == "__main__":
    main()

# performflype() manual testing

# flypes = Knot.flypedetect(Knot(permutation))
# flypeclass = []
# for flype in flypes:
     # newcode = Knot.performflype(Knot(permutation), flype)
     # flypeclass.append(newcode)
# print(permutation, "... CODES:", flypeclass, "\n\n")