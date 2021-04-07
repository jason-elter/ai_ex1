"""
In search.py, you will implement generic search algorithms
"""

import util


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

	print("Start:", problem.get_start_state().state)
    print("Is the start a goal?", problem.is_goal_state(problem.get_start_state()))
    print("Start's successors:", problem.get_successors(problem.get_start_state()))
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    Fringe is  queue of triples (successor, action, stepCost).
    """
    "*** YOUR CODE HERE ***"
    STATE = 0
    ACTION = 1
    # STEP_COST = 2

    fringe = util.Queue()
    cur_state = problem.get_start_state()
    visited = {cur_state}
    tracker = 0
    backtrack = [(cur_state, 0)]
    fringe.push((cur_state, None, 0))

    while True:
        cur_state = fringe.pop()
        if problem.is_goal_state(cur_state[STATE]):
            break
        successors = problem.get_successors(cur_state[STATE])
        for triple in successors:
            if triple[STATE] not in visited:
                visited.add(triple[STATE])
                fringe.push(triple)
                backtrack.append((triple, tracker))
        tracker += 1

    path = []
    while tracker != 0:
        path.append(backtrack[tracker][0][ACTION])
        tracker = backtrack[tracker][1]
    path.reverse()
    return path

    # util.raiseNotDefined()


def uniform_cost_search(problem):
    """
    Search the node of least total cost first.
    Fringe is a priority queue of tuples: (successor, action, action cost, parent ID)
    """
    "*** YOUR CODE HERE ***"
    STATE = 0
    ACTION = 1
    STEP_COST = 2
    COST_FROM_ROOT = 2
    PARENT_ID = 3

    fringe = util.PriorityQueue()
    cur_state = problem.get_start_state()
    visited = {cur_state}
    counter = 0
    backtrack = {}
    fringe.push((cur_state, None, 0, 0), 0)

    while True:
        cur_state = fringe.pop()
        backtrack[counter] = cur_state
        if problem.is_goal_state(cur_state[STATE]):
            break
        successors = problem.get_successors(cur_state[STATE])
        for triple in successors:
            if triple[STATE] not in visited:
                visited.add(triple[STATE])
                fringe.push((triple[STATE], triple[ACTION], triple[STEP_COST] + cur_state[COST_FROM_ROOT], counter),
                            triple[STEP_COST] + cur_state[COST_FROM_ROOT])
        counter += 1

    path = []
    tracker = counter
    while tracker != 0:
        path.append(backtrack[tracker][ACTION])
        tracker = backtrack[tracker][PARENT_ID]
    path.reverse()
    return path
    # util.raiseNotDefined()


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
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
