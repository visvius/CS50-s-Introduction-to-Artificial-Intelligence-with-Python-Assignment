from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # TODO
    # Implies A is either Knight or Knave
    Biconditional(AKnight, Not(AKnave)),
    # If A is speaking the truth
    Implication(AKnight, And(AKnight, AKnave)),
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # TODO
    # Person is either a Knight or Knave
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    # if A is speaking truth
    Implication(AKnight, And(AKnave, BKnave)),
    # if A is lying
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # TODO
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    # we are of SAME kinds
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
    # we are of DIFFERENT kinds 
    # Biconditional same as AND of 2 conditionals
    Biconditional(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # TODO
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    Biconditional(CKnight, Not(CKnave)),
    # A's statement
    Biconditional(AKnight, Or(AKnave, AKnight)),
    # B's statements
    Biconditional(BKnight, Biconditional(AKnight, AKnave)),
    Biconditional(BKnight, CKnave),
    #  C's statement
    Biconditional(CKnight, AKnight),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
