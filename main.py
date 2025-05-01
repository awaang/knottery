from knot.alternating_knot import gen_alternating_knots
from knot.non_alternating_knot import gen_non_alternating_knots

# Notes:
# - Find order 1 flype permutations from given permutation, then see if self contained, keep going
# - Check only the permutations that are not self contained
# - Check each "tree" from each dowker code
# - Use sorting algorithm to determine lexographically minimal code
# - Eliminate self contained list of flypes from permutations, add lexographically minimal code to final_list

# - at 8 crossings, there are 17 non prime knots included atm ????????

def main():
     AlternatingList = gen_alternating_knots(8)
     NonAlternatingList = gen_non_alternating_knots(8)

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