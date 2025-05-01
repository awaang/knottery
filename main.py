from knot.knot import gen_dowkers
from knot.alternating_knot import AlternatingKnot
from knot.non_alternating_knot import NonAlternatingKnot

# Notes:
# - Find order 1 flype permutations from given permutation, then see if self contained, keep going
# - Check only the permutations that are not self contained
# - Check each "tree" from each dowker code
# - Use sorting algorithm to determine lexographically minimal code
# - Eliminate self contained list of flypes from permutations, add lexographically minimal code to a list (Final list)

# - at 8 crossings, there are 17 non prime knots included atm

def gen_alternating_knots():
     permutations = gen_dowkers(8)
     
     for i in range(len(permutations)):
          if AlternatingKnot(permutations[i]).is_lexographic() == False: # criteria 1: checks if the dowker code is lexographically minimal
               permutations[i] = 0
          elif AlternatingKnot(permutations[i]).is_prime() == False: # criteria 2: checks if the dowker code is prime
               permutations[i] = 0 
          elif AlternatingKnot(permutations[i]).is_possible() == False: # criteria 3: checks if the dowker code is possible
               permutations[i] = 0
     
     permutations = AlternatingKnot(permutations).zero_remove() # remove all zeroed permutations

     finallist = []

     # criteria 4: checks if the dowker code is minimal with respect to flyping
     for permutation in permutations:
          if permutation in permutations:
               flypeclass = AlternatingKnot.find_flype_class(AlternatingKnot(permutation), [permutation]) 
               permutations = [perm for perm in permutations if perm not in flypeclass] # removes all permutations that are in the flypeclass

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

               finallist.append(AlternatingKnot.zero_remove(AlternatingKnot(flypeclass))[0]) # append the lexographically minimal code of its flype class to the final list
     
     finallist = [x for n, x in enumerate(finallist) if x not in finallist[:n]] # removes duplicates

     return finallist

def gen_non_alternating_knots():
     return []

def main():
     AlternatingList = gen_alternating_knots()
     NonAlternatingList = gen_non_alternating_knots()

     print("\nAlternating Knots:")
     for knot in AlternatingList:
          print(knot)
     print(len(AlternatingList))

     print("\nNon-Alternating Knots:")
     for knot in NonAlternatingList:
          print(knot)
     print(len(NonAlternatingList))

if __name__ == "__main__":
    main()