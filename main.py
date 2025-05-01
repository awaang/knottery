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

     permutations = AlternatingKnot.compute_flype_minimals(permutations) # criteria 4: checks if the dowker code is minimal with respect to flyping

     return permutations

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