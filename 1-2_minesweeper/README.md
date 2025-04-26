# Minesweeper AI

An AI agent that plays the classic **Minesweeper** game using logical inference and propositional knowledge representation.
---

## 📋 Project Overview

This project is a Python implementation of Minesweeper — but instead of relying on luck, I build an AI that uses propositional logic to infer safe moves and locate mines.

The AI dynamically updates its knowledge base as it explores the board, allowing it to make increasingly smarter decisions — much like a slightly less caffeinated version of a real player.

---
## How It Works
The project contains three main components:
* Minesweeper Class: Manages the game board, randomly places mines, and provides information about neighboring mines.
* Sentence Class: Represents logical sentences about the game (e.g., “out of these cells, exactly two are mines”).
* MinesweeperAI Class:
  * Remembers moves made, known safe cells, and known mines.
  * Updates its knowledge base with new information after each move.
  * Makes inferences

---
## 🛠 Setup Instructions
```bash
# Clone the repository or download the project:

git clone <your-repository-url>
cd minesweeper

# Install required dependencies (Only pygame is needed.):
pip install -r requirements.txt

# Run the graphical interface:
python runner.py
```
> You can either play manually or watch the AI flex its brain muscles.
---

## Knowledge Representation
Rather than constructing complex propositional logic formulas, I represent knowledge with a much simpler and scalable form:
`{Cell1, Cell2, Cell3} = 2`

Meaning: "Among Cell1, Cell2, and Cell3, exactly 2 cells are mines."

The AI updates and simplifies its knowledge base by:
* Marking cells as safe when count = 0.
* Marking cells as mines when count = number of unknown cells.
* Performing subset inference:
> If {A, B} = 1 and {A, B, C} = 2, then we infer {C} = 1.

This lightweight knowledge management allows efficient, real-time decision-making, even on larger boards.

---
## Project Structure
```bash
1-2_minesweeper/
├── runner.py        # GUI interface for the game
├── minesweeper.py   # Core gameplay logic and AI reasoning
├── requirements.txt # Required Python packages (pygame)
└── README.md        # This file
```
---
## Key AI Strategies
* Safe Move First: Always select a known safe move if available.
* Random Move Fallback: If no safe moves are known, pick a random unexplored cell (because life is sometimes chaos).
* Iterative Knowledge Expansion: Constantly update known facts as more cells are explored.

---
## Future Improvements
* Implement probabilistic reasoning to make best-guess moves when logic isn't enough.
* Scale to larger boards (Intermediate/Expert Minesweeper).
* Add more graphical enhancements or step-by-step AI move visualization.
