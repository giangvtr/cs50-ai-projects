import sys
from asyncio import Queue

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )
        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var, words in self.domains.items():
            for word in words.copy():
                if len(word) != var.length:
                    words.remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.

        The revise function should make the variable x arc consistent with the variable y.
        """
        revised = False
        overlap = self.crossword.overlaps.get((x,y))
        if overlap is None:
            return revised

        i, j = overlap

        for value in self.domains[x].copy():
            satisfies_constraint = any(
                value[i] == y_word[j] for y_word in self.domains[y]
            )
            if not satisfies_constraint:
                self.domains[x].remove(value)
                revised = True
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            arc_queue = []
            for var in self.crossword.variables:
                for neighbor in self.crossword.neighbors(var):
                    arc_queue.append((var, neighbor))
        else: arc_queue = arcs

        while arc_queue:
            x, y = arc_queue.pop()
            if self.revise(x, y):
                if not self.domains[x]:
                    return False
                for z in self.crossword.neighbors(x):
                    if z != y:
                        arc_queue.append((z, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # If the assignment length is lacking sth
        if len(assignment) != len(self.crossword.variables):
            return False

        # If not every crossword variable is assigned to a value
        for var in self.crossword.variables:
            if var not in assignment:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.

        An assignment is consistent if it satisfies all of the constraints of the problem:
        that is to say, all values are distinct, every value is the correct length,
        and there are no conflicts between neighboring variables.
        """
        if not self.assignment_complete(assignment):
            return True

        # Check if all values are unique by making a set and compare the length
        assignment_set = set(assignment.values())
        if len(assignment_set) != len(assignment):
            return False

        for var, word in assignment.items():
            if len(word) != var.length:
                return False
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment:
                    i, j = self.crossword.overlaps.get((var, neighbor), (None, None))
                    if i is not None and j is not None:
                        if word[i] != assignment[neighbor][j]:
                            return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.

        The order_domain_values function should return a list of all of the values in the domain of var, ordered according to the least-constraining values heuristic.

    var will be a Variable object, representing a variable in the puzzle.
    Recall that the least-constraining values heuristic is computed as the number of values ruled out for neighboring unassigned variables. That is to say, if assigning var to a particular value results in eliminating n possible choices for neighboring variables, you should order your results in ascending order of n.
    Note that any variable present in assignment already has a value, and therefore shouldn’t be counted when computing the number of values ruled out for neighboring unassigned variables.
    For domain values that eliminate the same number of possible choices for neighboring variables, any ordering is acceptable.
    Recall that you can access self.crossword.overlaps to get the overlap, if any, between two variables.
    It may be helpful to first implement this function by returning a list of values in any arbitrary order (which should still generate correct crossword puzzles). Once your algorithm is working, you can then go back and ensure that the values are returned in the correct order.
    You may find it helpful to sort a list according to a particular key: Python contains some helpful functions for achieving this.

    In your code, you’re comparing the characters at the overlap positions with the assignment dictionary, but the neighbor is not in the assignment dictionary. Instead, you should be comparing the characters at the overlap positions with the domain of the neighbor.

For example, you can iterate over the words in the domain of the neighbor and compare the characters at the overlap positions. Do you have any ideas on how to implement this in your code?

        """
        value_constraints = []

        for value in self.domains[var]:
            count = 0
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment:
                    continue

                i, j = self.crossword.overlaps.get((var, neighbor), (None, None))
                if i is not None and j is not None:
                    for neighbor_value in self.domains[neighbor]:
                        if value[i] != neighbor_value[j]:
                            count += 1

            value_constraints.append((value, count))

        value_constraints.sort(key=lambda pair: pair[1])

        return [val for val, _ in value_constraints]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned_variables = []

        for variable in self.crossword.variables:
            # If the variable is not already assigned, add it to our list of candidates
            if variable not in assignment:
                unassigned_variables.append(variable)

        # MRV and Degree heuristics
        best_variable = None
        smallest_domain_size = float('inf')  # Start with a very large number
        highest_degree = -1  # Start with a very low number

        for variable in unassigned_variables:
            domain_size = len(self.domains[variable])
            degree = len(self.crossword.neighbors(variable))

            # 1st priority: the variable with the smallest domain
            if domain_size < smallest_domain_size:
                best_variable = variable
                smallest_domain_size = domain_size
                highest_degree = degree  # Update degree as well

            # If there's a tie, apply degree heuristic
            elif domain_size == smallest_domain_size:
                if degree > highest_degree:
                    best_variable = variable
                    highest_degree = degree
        return best_variable

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            local_assignment = assignment.copy()
            local_assignment[var] = value

            if self.consistent(local_assignment):
                original_domains = {
                    var: set(values) for var, values in self.domains.items()
                }
                if self.ac3([(neighbor, var) for neighbor in self.crossword.neighbors(var)]):
                    result = self.backtrack(local_assignment)
                    if result is not None:
                        return result
                self.domains = original_domains
        return None

def main():
    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
