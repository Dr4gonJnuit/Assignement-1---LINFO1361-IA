"""
Name of the author(s):
- Charles Lohest <charles.lohest@uclouvain.be>
"""
import time
import sys
from search import *
from copy import deepcopy

#################
# Problem class #
#################
dico = {}


class Pacman(Problem):

    def __init__(self, init_state):
        super().__init__(init_state)
        self.pos = (0, 0)
        found_pacman = False
        for row in range(shape[0] + 1):
            for col in range(shape[1] + 1):
                if init_state.grid[row][col] == 'P':
                    self.pos = (row, col)
                    found_pacman = True
                    break
            if found_pacman:
                break

    def actions(self, state):
        # Define the possible actions for a given state
        actions = ["Up", "Down", "Left", "Right"]

        if self.pos[0] == 0 or state.grid[self.pos[0] - 1][self.pos[1]] == "#":
            actions.remove("Up")
        if self.pos[0] == state.shape[0] - 1 or state.grid[self.pos[0] + 1][self.pos[1]] == "#":
            actions.remove("Down")
        if self.pos[1] == 0 or state.grid[self.pos[0]][self.pos[1] - 1] == "#":
            actions.remove("Left")
        if self.pos[1] == state.shape[1] or state.grid[self.pos[0]][self.pos[1] + 1] == "#":
            actions.remove("Right")

        return actions

    def result(self, state, action):

        new_grid = change_grid(self.pos, action, state.grid)

        state.grid = new_grid

        """# Apply the action to the state and return the new state
        new_grid = deepcopy(state.grid)

        # Two tuple have to be changed
        if action == "Up":
            new_pos = self.pos[0] - 1, self.pos[1]  # Take the new position
            new_grid = new_grid[new_pos[0]][:new_pos[1]] + ('P',) + new_grid[new_pos[0]][new_pos[1] + 1:], \
                       new_grid[new_pos[0] + 1][:new_pos[1]] + ('.',) + new_grid[new_pos[0] + 1][new_pos[1] + 1:]
            state.grid = state.grid[:new_pos[0]] + (new_grid[0],) + (new_grid[1],) + state.grid[new_pos[0] + 2:]
        if action == "Down":
            new_pos = self.pos[0] + 1, self.pos[1]  # Take the new position
            new_grid = new_grid[new_pos[0] - 1][:new_pos[1]] + ('.',) + new_grid[new_pos[0] - 1][new_pos[1] + 1:], \
                       new_grid[new_pos[0]][:new_pos[1]] + ('P',) + new_grid[new_pos[0]][new_pos[1] + 1:]
            state.grid = state.grid[:new_pos[0] - 1] + (new_grid[0],) + (new_grid[1],) + state.grid[new_pos[0] + 2:]
        # We change only a tuple
        if action == "Right":
            new_pos = self.pos[0], self.pos[1] + 1  # Take the new position
            new_grid = new_grid[new_pos[0]][:new_pos[1] - 1] + ('.', 'P') + new_grid[new_pos[0]][new_pos[1] + 1:]
            state.grid = state.grid[:new_pos[0]] + (new_grid,) + state.grid[new_pos[0] + 1:]
        if action == "Left":
            new_pos = self.pos[0], self.pos[1] - 1  # Take the new position
            new_grid = new_grid[new_pos[0]][:new_pos[1]] + ('.', 'P') + new_grid[new_pos[0]][new_pos[1] + 2:]
            state.grid = state.grid[:new_pos[0]] + (new_grid,) + state.grid[new_pos[0] + 1:]"""

        return state

    def goal_test(self, state):
        # check for goal state
        return state.answer == 0


###############
# State class #
###############
class State:

    def __init__(self, shape, grid, answer=None, move="Init"):
        self.shape = shape
        self.answer = answer
        self.grid = grid
        self.move = move

    def __str__(self):
        s = self.move + "\n"
        for line in self.grid:
            s += "".join(line) + "\n"
        return s


def read_instance_file(filepath):
    with open(filepath) as fd:
        lines = fd.read().splitlines()
    shape_x, shape_y = tuple(map(int, lines[0].split()))
    initial_grid = [tuple(row) for row in lines[1:1 + shape_x]]
    initial_fruit_count = sum(row.count('F') for row in initial_grid)

    return (shape_x, shape_y), initial_grid, initial_fruit_count


def change_grid(position: tuple, move: tuple, grid: tuple) -> tuple:
    new_pos = move[0], move[1]  # Take the new position

    # Since it's easier to work with list we change the tuple in list
    grid = [list(elem) for elem in grid]

    # We replace the previous position by a '.' and the new by 'P'
    grid[position[0]][position[1]] = '.'
    grid[new_pos[0]][new_pos[1]] = 'P'

    # We change back the list in tuple
    grid = tuple(tuple(elem) for elem in grid)

    return grid


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: ./Pacman.py <path_to_instance_file>")
    filepath = sys.argv[1]

    shape, initial_grid, initial_fruit_count = read_instance_file(filepath)
    init_state = State(shape, tuple(initial_grid), initial_fruit_count, "Init")
    problem = Pacman(init_state)

    # Example of search
    start_timer = time.perf_counter()
    node, nb_explored, remaining_nodes = breadth_first_tree_search(problem)
    end_timer = time.perf_counter()

    # Example of print
    path = node.path()

    for n in path:
        # assuming that the __str__ function of state outputs the correct format
        print(n.state)

    print("* Execution time:\t", str(end_timer - start_timer))
    print("* Path cost to goal:\t", node.depth, "moves")
    print("* #Nodes explored:\t", nb_explored)
    print("* Queue size at goal:\t", remaining_nodes)
