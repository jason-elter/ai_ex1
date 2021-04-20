"""
In search.py, you will implement generic search algorithms
"""

import util

STATE = 0
ACTION = 1
STEP_COST = 2
COST_FROM_ROOT = 2
PARENT_ID = 3
FAILURE = []


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def is_goal_state(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches
    the goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    fringe = util.Stack()
    current_state = problem.get_start_state()
    visited = set()
    path = list()
    counter = [1]

    while True:
        # Check if found goal.
        if problem.is_goal_state(current_state):
            return path
        elif current_state not in visited:
            # New unvisited state so add all successors to fringe.
            visited.add(current_state)
            successors = problem.get_successors(current_state)
            num_successors = len(successors)
            if num_successors > 0:
                counter.append(num_successors)
                path.append(None)  # Placeholder for current's successors' moves.
                for triple in successors:
                    fringe.push(triple[:2])

        # Check if we've exhausted the search
        if fringe.isEmpty():
            return FAILURE

        # Proceed to next node.
        current_state, current_move = fringe.pop()
        # Climb back up tree if necessary.
        if counter[-1] == 0:
            i = -1
            while counter[i - 1] == 0:
                i -= 1
            del path[i:]
            del counter[i:]
        # Update breadth counter and change placeholder move with correct one.
        counter[-1] -= 1
        path[-1] = current_move


def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"

    fringe = util.Queue()
    first_state = problem.get_start_state()
    visited = {first_state}
    cur_node = Node((first_state, None, 0), None)
    fringe.push(cur_node)

    while not fringe.isEmpty():
        cur_node = fringe.pop()
        visited.add(cur_node)
        if problem.is_goal_state(cur_node.get_state()):
            return get_path(cur_node)
        successors = problem.get_successors(cur_node.get_state())
        for triple in successors:
            if triple[STATE] not in visited:
                visited.add(triple[STATE])
                fringe.push(Node(triple, cur_node))

    return FAILURE


def uniform_cost_search(problem):
    """
    Search the node of least total cost first.
        Fringe is a priority queue of tuples: (successor, action, action cost, parent ID)
        prioritized by cost from root.
    """
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue()
    first_state = problem.get_start_state()
    visited = {first_state}
    cur_node = Node((first_state, None, 0), None)
    fringe.push(cur_node, 0)
    while not fringe.isEmpty():
        cur_node = fringe.pop()
        if problem.is_goal_state(cur_node.get_state()):
            return get_path(cur_node)
        successors = problem.get_successors(cur_node.get_state())
        for (new_state, action, step_cost) in successors:
            if new_state not in visited:
                visited.add(new_state)
                fringe.push(Node((new_state, action, step_cost + cur_node.get_cost()), cur_node),
                            step_cost + cur_node.get_cost())

    return FAILURE


def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def a_star_search(problem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    # print("Start:", problem.get_start_state().state)
    # print("Is the start a goal?", problem.is_goal_state(problem.get_start_state()))
    # print("Start's successors:", problem.get_successors(problem.get_start_state()))

    fringe = util.PriorityQueue()
    first_state = problem.get_start_state()
    visited = set()
    fringe.push(Node((first_state, None, 0), None), 0)

    while not fringe.isEmpty():
        current_node = fringe.pop()
        current_state = current_node.get_state()
        if current_state not in visited:
            if problem.is_goal_state(current_state):
                return get_path(current_node)

            visited.add(current_state)
            successors = problem.get_successors(current_state)
            for (new_state, action, step_cost) in successors:
                new_cost = step_cost + current_node.get_cost()
                priority = new_cost + heuristic(new_state, problem)
                fringe.push(Node((new_state, action, new_cost), current_node), priority)

    return FAILURE


class Node:
    def __init__(self, data, parent):
        self.data = data  # (state, action, stepCost)
        self.parent = parent

    def __lt__(self, other):
        return True

    def get_state(self):
        return self.data[STATE]

    def get_action(self):
        return self.data[ACTION]

    def get_cost(self):
        return self.data[STEP_COST]

    def get_parent(self):
        return self.parent


def get_path(last_node):
    path = []
    cur_node = last_node
    while cur_node.get_parent() is not None:
        path.append(cur_node.get_action())
        cur_node = cur_node.get_parent()
    path.reverse()
    return path


# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
