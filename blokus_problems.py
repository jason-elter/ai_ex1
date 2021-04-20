import util
import math
from board import Board
from search import astar
from search import SearchProblem

EMPTY_TILE = -1


class BlokusFillProblem(SearchProblem):
    """
    A one-player Blokus game as a search problem.
    This problem is implemented for you. You should NOT change it!
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.expanded = 0

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        """
        state: Search state
        Returns True if and only if the state is a valid goal state
        """
        return not any(state.pieces[0])

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, 1) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)


#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################
class BlokusCornersProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        self.expanded = 0
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        board = state.state
        right = state.board_w - 1
        top = state.board_h - 1
        return board[0, right] != EMPTY_TILE and board[top, 0] != EMPTY_TILE and board[top, right] != EMPTY_TILE

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        cost_sum = 0
        for move in actions:
            cost_sum += move.piece.get_num_tiles()
        return cost_sum


def blokus_corners_heuristic(state, problem):
    """
    Your heuristic for the BlokusCornersProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come up
    with an admissible heuristic; almost all admissible heuristics will be consistent
    as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the other hand,
    inadmissible or inconsistent heuristics may find optimal solutions, so be careful.
    """
    "*** YOUR CODE HERE ***"
    # Sum corners that haven't been reached yet
    corners_left = -state.state[0, state.board_w - 1] - state.state[state.board_h - 1, 0] - state.state[
        state.board_h - 1, state.board_w - 1]

    pieces_left = sorted(
        [state.piece_list.get_piece(i).get_num_tiles() + state.board_w + state.board_h for i in
         range(state.piece_list.get_num_pieces()) if
         state.pieces[0, i]])
    ans = sum(pieces_left[:corners_left])
    if ans >= min(state.board_w, state.board_h) and corners_left < 2:
        return pieces_left[0]
    return ans


class BlokusCoverProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=[(0, 0)]):
        self.targets = targets.copy()
        self.expanded = 0
        self.starting_point = starting_point
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """
        board = state.state
        for target in self.targets:
            if board[target] == EMPTY_TILE:
                return False
        return True

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        cost_sum = 0
        for move in actions:
            cost_sum += move.piece.get_num_tiles()
        return cost_sum


def blokus_cover_heuristic(state, problem):
    "*** YOUR CODE HERE ***"
    targets_left = 0
    max_dist = 0
    for t in problem.targets:
        if state.state[t] == -1:
            targets_left += 1
            dist = distance(problem.starting_point, t)

            if dist > max_dist:
                max_dist = dist

    piece_limit = targets_left
    pieces_left = []
    ans = 0
    for i in range(state.piece_list.get_num_pieces()):
        if state.pieces[0, i]:
            pieces_left.append(state.piece_list.get_piece(i).get_num_tiles())
            ans += state.piece_list.get_piece(i).get_num_tiles()
            piece_limit -= 1
            if piece_limit == 0:
                break

    pieces_left = sorted(pieces_left[:3])
    pieces_left.append(problem.board.board_w * problem.board.board_h)
    result = 0
    for i in range(targets_left):
        result += pieces_left[i]
        if result >= max_dist:
            if targets_left >= 2:
                return result
            else:
                return pieces_left[0]
    return result
    # util.raiseNotDefined()


class ClosestLocationSearch:
    """
    In this problem you have to cover all given positions on the board,
    but the objective is speed, not optimality.
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=(0, 0)):
        self.expanded = 0
        self.targets = targets
        "*** YOUR CODE HERE ***"
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.starting_point = starting_point

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def solve(self):
        """
        This method should return a sequence of actions that covers all target locations on the board.
        This time we trade optimality for speed.
        Therefore, your agent should try and cover one target location at a time. Each time, aiming for the closest uncovered location.
        You may define helpful functions as you wish.

        Probably a good way to start, would be something like this --

        current_state = self.board.__copy__()
        backtrace = []

        while ....

            actions = set of actions that covers the closets uncovered target location
            add actions to backtrace

        return backtrace
        """
        "*** YOUR CODE HERE ***"
        current_state = self.board.__copy__()
        backtrace = []

        if len(self.targets) == 0:
            return []
        if self.targets[0] == self.starting_point:
            return []

        targets_remaining = util.PriorityQueue()
        for target in self.targets:
            targets_remaining.push(target, distance(self.starting_point, target))

        for t in range(len(self.targets)):
            cur_target = targets_remaining.pop()

            sub_problem = BlokusSubProblem(current_state, cur_target)
            moves = astar(sub_problem)
            backtrace.extend(moves)

            for m in moves:
                current_state = current_state.do_move(0, m)
            self.expanded += sub_problem.expanded

        return backtrace
        # util.raiseNotDefined()


class BlokusSubProblem(SearchProblem):

    def __init__(self, state, target=(0, 0)):
        self.expanded = 0
        self.starting_state = state
        self.target = target

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.starting_state

    def is_goal_state(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """
        return state.state[self.target] != EMPTY_TILE

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        cost_sum = 0
        for move in actions:
            cost_sum += move.piece.get_num_tiles()
        return cost_sum


class MiniContestSearch:
    """
    Implement your contest entry here
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=(0, 0)):
        self.targets = targets.copy()
        "*** YOUR CODE HERE ***"

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def solve(self):
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


def distance(xy1, xy2):
    x_dist = xy1[0] - xy2[0]
    y_dist = xy1[1] - xy2[1]
    return int(math.sqrt((x_dist ** 2) + (y_dist ** 2)))
