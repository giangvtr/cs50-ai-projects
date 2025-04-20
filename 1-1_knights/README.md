# Knights

Solve logical puzzles involving knights and knaves using propositional logic and model checking.

## Project Description

In this project, I’ll implement a program that can solve a class of logical puzzles known as **Knights and Knaves** puzzles, originally popularized by Raymond Smullyan. Each character in a puzzle is either a **knight**, who always tells the truth, or a **knave**, who always lies.

My task is to represent each puzzle using **propositional logic**, and use **model checking** to determine, for each character, whether they are a knight or a knave.

## Files

- `logic.py`: Contains logic classes and the `model_check` function.
- `puzzle.py`: Where I define the logical knowledge bases and solve the puzzles.
- `README.md`: This file.

## Puzzles to Implement
Implement logic for the following puzzles in `puzzle.py`:

### Puzzle 0
**Characters**: A  
**Statement**: A says “I am both a knight and a knave.”

### Puzzle 1
**Characters**: A, B  
**Statement**: A says “We are both knaves.”  
**B says nothing.**

### Puzzle 2
**Characters**: A, B  
**Statements**:  
- A says “We are the same kind.”  
- B says “We are of different kinds.”

### Puzzle 3
**Characters**: A, B, C  
**Statements**:  
- A says either “I am a knight.” or “I am a knave.” (but you don’t know which)  
- B says “A said ‘I am a knave.’”  
- B then says “C is a knave.”  
- C says “A is a knight.”

---
## Concepts Covered
* Propositional logic modeling
* Knowledge representation
* Logical inference
* Model checking
* Logical connectives and truth conditions
