from board import Board
from search import SearchProblem, ucs
import util
import heapq

from search import dfs
from search import SearchProblem, BoardSearch

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
    pieces_left = []

    corners_left = 0
    if not state.connected[0, 0, state.board_w - 1]:
        corners_left += 1
    if not state.connected[0, state.board_h - 1, 0]:
        corners_left += 1
    if not state.connected[0, state.board_h - 1, state.board_w - 1]:
        corners_left += 1

    c = corners_left

    for i in range(state.piece_list.get_num_pieces()):
        if state.pieces[0, i]:
            heapq.heappush(pieces_left, state.piece_list.get_piece(i).get_num_tiles())
            c -= 1
            if c == 0:
                break

    ans = sum(pieces_left)
    if ans >= state.board_w or ans >= state.board_h:
        if corners_left >= 2:
            return ans
        else:
            return heapq.heappop(pieces_left)
    return ans

    #
    # for i in range(3):
    #     heapq.heappush(pieces_left, state.board_h * state.board_w)   # why is this ok? or needed?

    # answer = 0
    # smallest = 0
    # for i in range(corners_left):
    #     if i == 0:
    #         smallest = heapq.heappop(pieces_left)
    #         answer = smallest
    #     else:
    #         answer += heapq.heappop(pieces_left)
    #
    #     if answer >= state.board_w or answer >= state.board_h:    # what does this mean about the search problem?
    #         if corners_left >= 2:
    #             return answer
    #         else:
    #             return smallest
    # return answer


class BlokusCoverProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=[(0, 0)]):
        self.targets = targets.copy()
        self.expanded = 0
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
    util.raiseNotDefined()


class ClosestLocationSearch:
    """
    In this problem you have to cover all given positions on the board,
    but the objective is speed, not optimality.
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=(0, 0)):
        self.expanded = 0
        self.targets = targets.copy()
        "*** YOUR CODE HERE ***"
        self.board = Board(board_w, board_h, 1, piece_list)
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
        targets_remaining = set(self.targets)
        acquired = {self.starting_point}

        targets_remaining1 = util.PriorityQueue()
        for t in self.targets:
            targets_remaining1.push(t, util.manhattanDistance(self.starting_point, t))
        # find closest target:
        # closest = float('inf')
        # first_target = self.targets[0]
        # for target in self.targets:
        #     manhattan_dist = util.manhattanDistance(target, self.starting_point)
        #     if manhattan_dist < closest:
        #         first_target = target
        #         closest = manhattan_dist
        # cur_target = self.next_target(acquired, targets_remaining)
        # cur_target = targets_remaining1.pop()

        # while targets_remaining1:
        for t in range(len(self.targets)):
            cur_target = targets_remaining1.pop()

            sub_problem = BlokusCoverProblem(self.board.board_w, self.board.board_h, self.board.piece_list,
                                             self.starting_point, [cur_target])
            backtrace.extend(ucs(sub_problem))
            acquired.add(cur_target)


            # targets_remaining.remove(cur_target)
            targets_remaining1 = self.update_targets(acquired, targets_remaining1)
            # cur_target = targets_remaining1.pop()
            # cur_target = self.next_target(acquired, targets_remaining)

        return backtrace
        # util.raiseNotDefined()

    def update_targets(self, acquired, targets_remaining):
        assert len(acquired) > 0
        # closest = float('inf')
        new_targets = util.PriorityQueue()

        while not targets_remaining.isEmpty():
            target = targets_remaining.pop()
            for point in acquired:
                manhattan_dist = util.manhattanDistance(target, point)
                new_targets.push(target, manhattan_dist)
        return new_targets

    # def next_target(self, acquired, targets_remaining):
    #     assert len(acquired) > 0
    #     assert len(targets_remaining) > 0
    #     closest = float('inf')
    #     for target in targets_remaining:
    #         for point in acquired:
    #             manhattan_dist = util.manhattanDistance(target, point)
    #             if manhattan_dist < closest:
    #                 cur_target = target
    #                 closest = manhattan_dist
    #     return cur_target


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
