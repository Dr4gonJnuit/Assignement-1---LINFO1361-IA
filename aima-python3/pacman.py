"""
Name of the author(s):
- Charles Lohest <charles.lohest@uclouvain.be>
"""
import time
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
        actions = []

        i = self.pos[1] - 1
        while i >= 0:
            if(state.grid[self.pos[0]][i] != '#'):
                actions.append("Move to (" + str(self.pos[0]) + "," + str(i) + ")")
            else:
                break
            i -= 1

        i = self.pos[1] + 1
        while i < state.shape[1]:
            if (state.grid[self.pos[0]][i] != '#'):
                actions.append("Move to (" + str(self.pos[0]) + "," + str(i) + ")")
            else:
                break
            i += 1

        i = self.pos[0] - 1
        while i >= 0:
            if (state.grid[i][self.pos[1]] != '#'):
                actions.append("Move to (" + str(i) + "," + str(self.pos[1]) + ")")
            else:
                break
            i -= 1

        i = self.pos[0] + 1
        while i < state.shape[0]:
            if (state.grid[i][self.pos[1]] != '#'):
                actions.append("Move to (" + str(i) + "," + str(self.pos[1]) + ")")
            else:
                break
            i += 1

        return actions

    def result(self, state, action):
        new_grid = deepcopy(state.grid)

        move = action.replace("Move to (", "")
        move = move.replace(")", "")
        move = move.replace(",", " ")
        row, col = tuple(map(int, move.split()))

        # Since it's easier to work with list we change the tuple in list
        new_grid = [list(elem) for elem in new_grid]

        # We replace the previous position by a '.' and the new by 'P'
        new_grid[self.pos[0]][self.pos[1]] = '.'
        # Add a counter for the fruits
        if new_grid[row][col] == 'F':
            state.answer -= 1
        new_grid[row][col] = 'P'
        self.pos = (row, col)

        # We change back the list in tuple
        new_grid = tuple(tuple(elem) for elem in new_grid)

        state.grid = new_grid

        return State(shape, new_grid, state.answer, action)

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


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: ./Pacman.py <path_to_instance_file>")
    filepath = sys.argv[1]

    shape, initial_grid, initial_fruit_count = read_instance_file(filepath)
    init_state = State(shape, tuple(initial_grid), initial_fruit_count, "Init")
    problem = Pacman(init_state)

    # Example of search
    start_timer = time.perf_counter()
    node, nb_explored, remaining_nodes = depth_first_graph_search(problem)
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
