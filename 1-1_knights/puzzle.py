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
    Or(AKnight,AKnave),
    Implication(Not(And(AKnave,AKnight)),AKnave)
)


# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnight,AKnave),
    Or(BKnave,BKnight),
    Implication(AKnave,Not(And(AKnave,BKnave))),
    Implication(Not(And(AKnave,BKnave)),BKnight),
    Implication(AKnight, And(AKnave,BKnave)),
    Implication(And(AKnave,BKnave),BKnave)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
same_kind = Or(And(AKnight,BKnight),And(AKnave,BKnave))
different_kind = Or(And(AKnight,BKnave),And(AKnave,BKnight))

knowledge2 = And(
    Or(AKnight,AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnave,BKnight),
    Not(And(BKnight, BKnave)),

    Implication(AKnight, same_kind),
    Implication(AKnave, Not(same_kind)),

    Implication(BKnight, different_kind),
    Implication(BKnave, Not(different_kind)),

)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

a_said_knight = AKnight
a_said_knave = AKnave

knowledge3 = And(
    Or(AKnight,AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnave,BKnight),
    Not(And(BKnight, BKnave)),
    Or(CKnave,CKnight),
    Not(And(CKnight, CKnave)),

    Implication(AKnight,a_said_knight),
    Implication(AKnave,a_said_knight),

    Implication(BKnight,a_said_knave),
    Implication(BKnave, a_said_knight),


    # B says "C is a knave."
    Implication(BKnight, CKnave),
    Implication(BKnave, CKnight),

    # C says "A is a knight.
    Implication(CKnight,AKnight),
    Implication(CKnave, AKnave)
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
