# 🎬 Degrees of Separation

This project implements a program that determines the number of “degrees of separation” between two actors based on the movies they’ve starred in, using **Breadth-First Search (BFS)** to compute the shortest path. It’s inspired by the classic _Six Degrees of Kevin Bacon_ game.

---

## 📌 Project Description

Given a database of actors and the movies they’ve appeared in, the program answers questions like:

> How many connections (via shared movies) exist between Emma Watson and Jennifer Lawrence?

Example:

```bash
$ python degrees.py large
Loading data...
Data loaded.
Name: Emma Watson
Name: Jennifer Lawrence
3 degrees of separation.
1: Emma Watson and Brendan Gleeson starred in Harry Potter and the Order of the Phoenix
2: Brendan Gleeson and Michael Fassbender starred in Trespass Against Us
3: Michael Fassbender and Jennifer Lawrence starred in X-Men: First Class
```
---
The underlying task is framed as a graph search problem:
* States = actors (nodes)
* Actions = movies (edges connecting nodes)
* Goal = shortest path between two given actors

---
## Concepts Applied
* Breadth-First Search (BFS)
* Graph traversal
* Data parsing from CSV
* Basic CLI interaction

---
##Project Structure
pbset0-1_degrees
├── degrees.py           # Main driver script
├── util.py              # Search utilities (Node, QueueFrontier)
├── large/               # Full dataset
│   ├── people.csv
│   ├── movies.csv
│   └── stars.csv
├── small/               # Smaller test dataset
│   ├── people.csv
│   ├── movies.csv
│   └── stars.csv
└── README.md            # You're reading it!

---
## Credits
This project is part of the (CS50’s Introduction to Artificial Intelligence with Python 2024)[https://cs50.harvard.edu/ai/2024/] course.
