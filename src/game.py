import pygame
from enum import Enum
from dataclasses import dataclass
from collections import deque
import heapq
import time
from memory_profiler import memory_usage


def position_is_0(board, position):
    if position[0] < 0 or position[0] >= len(board[0]) or position[1] < 0 or position[1] >= len(board):
        return True
    else:
        return board[position[1]][position[0]] == 0


class PieceState(Enum):
    UP = 1
    HORIZONTAL = 2
    VERTICAL = 3


class AiLevel(Enum):
    BFS = 0
    DFS = 1
    GREEDY = 2
    ASTAR = 3
    WASTAR = 4    


class MoveDirection(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


@dataclass
class Piece:
    def __init__(self, position, piece_state, height):
        self.position = position
        self.piece_state = piece_state
        self.height = height

    def __hash__(self):
        return hash((self.piece_state, self.position))


class TreeNode:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.move = move

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self

    def cost(self):
        counter = 0
        #print(counter)
        node = self
        while (node.parent):
            counter += 1
            node = node.parent
        return counter


class GameState:

    def __init__(self, board, piece, portals: dict[tuple[int, int], tuple[int, int]], isAi=False, aiLevel=0, aiMoves=[]):
        self.board: list[int] = board
        self.piece: Piece = piece
        self.isAi: bool = isAi
        self.aiMoves = aiMoves
        self.aiLevel = aiLevel
        self.portals: dict[tuple[int, int], tuple[int, int]] = portals

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __hash__(self):
        return hash(self.piece)
    ''' - '''

    def __str__(self):
        return "(" + str(self.piece) + ")"

    def setAiMoves(self):
        if (self.aiLevel == AiLevel.BFS.value):
            initial_node = breadth_first_search(
                self, Victory, child_gamestates)
            self.aiMoves = solution_moves(initial_node)
        elif (self.aiLevel == AiLevel.DFS.value):
            initial_node = depth_first_search(
                self, Victory, child_gamestates)
            self.aiMoves = solution_moves(initial_node)
        elif (self.aiLevel == AiLevel.GREEDY.value):
            initial_node = greedy_search(self, Victory, child_gamestates, h1)
            self.aiMoves = solution_moves(initial_node)
        elif (self.aiLevel == AiLevel.ASTAR.value):
            initial_node = a_star_search(self, h1)
            self.aiMoves = solution_moves(initial_node)
        elif (self.aiLevel == AiLevel.WASTAR.value):
            initial_node = weighted_a_star_search(self, h1)
            self.aiMoves = solution_moves(initial_node)    
        

    def getAiMove(self):

        return self.aiMoves.pop(0)


def MoveUp(gamestate):
    piece = None
    if gamestate.piece.piece_state == PieceState.VERTICAL:
        piece = Piece(
            (gamestate.piece.position[0], gamestate.piece.position[1]-1), PieceState.UP, gamestate.piece.height)
    elif gamestate.piece.piece_state == PieceState.HORIZONTAL:
        piece = Piece((gamestate.piece.position[0], gamestate.piece.position[1]-1),
                      PieceState.HORIZONTAL, gamestate.piece.height)
    elif gamestate.piece.piece_state == PieceState.UP:
        piece = Piece((gamestate.piece.position[0], gamestate.piece.position[1] -
                      gamestate.piece.height), PieceState.VERTICAL, gamestate.piece.height)

    stateBeforeTP = GameState(gamestate.board, piece, gamestate.portals, isAi=gamestate.isAi, aiLevel=gamestate.aiLevel, aiMoves=gamestate.aiMoves)
    return Teleport(stateBeforeTP)


def MoveDown(gamestate):
    piece = None

    if gamestate.piece.piece_state == PieceState.VERTICAL:
        piece = Piece((gamestate.piece.position[0], gamestate.piece.position[1] +
                      gamestate.piece.height), PieceState.UP, gamestate.piece.height)
    elif gamestate.piece.piece_state == PieceState.HORIZONTAL:
        piece = Piece((gamestate.piece.position[0], gamestate.piece.position[1]+1),
                      PieceState.HORIZONTAL, gamestate.piece.height)
    elif gamestate.piece.piece_state == PieceState.UP:
        piece = Piece(
            (gamestate.piece.position[0], gamestate.piece.position[1]+1), PieceState.VERTICAL, gamestate.piece.height)

    stateBeforeTP = GameState(gamestate.board, piece, gamestate.portals, isAi=gamestate.isAi, aiLevel=gamestate.aiLevel, aiMoves=gamestate.aiMoves)
    return Teleport(stateBeforeTP)



def MoveLeft(gamestate):
    piece = None
    if gamestate.piece.piece_state == PieceState.VERTICAL:
        piece = Piece(
            (gamestate.piece.position[0]-1, gamestate.piece.position[1]), PieceState.VERTICAL, gamestate.piece.height)
    elif gamestate.piece.piece_state == PieceState.HORIZONTAL:
        piece = Piece(
            (gamestate.piece.position[0]-1, gamestate.piece.position[1]), PieceState.UP, gamestate.piece.height)
    elif gamestate.piece.piece_state == PieceState.UP:
        piece = Piece((gamestate.piece.position[0]-gamestate.piece.height,
                      gamestate.piece.position[1]), PieceState.HORIZONTAL, gamestate.piece.height)

    stateBeforeTP = GameState(gamestate.board, piece, gamestate.portals, isAi=gamestate.isAi, aiLevel=gamestate.aiLevel, aiMoves=gamestate.aiMoves)
    return Teleport(stateBeforeTP)



def MoveRight(gamestate):
    piece = None
    if gamestate.piece.piece_state == PieceState.VERTICAL:
        piece = Piece(
            (gamestate.piece.position[0]+1, gamestate.piece.position[1]), PieceState.VERTICAL, gamestate.piece.height)
    elif gamestate.piece.piece_state == PieceState.HORIZONTAL:
        piece = Piece((gamestate.piece.position[0]+gamestate.piece.height,
                      gamestate.piece.position[1]), PieceState.UP, gamestate.piece.height)
    elif gamestate.piece.piece_state == PieceState.UP:
        piece = Piece((gamestate.piece.position[0]+1, gamestate.piece.position[1]),
                      PieceState.HORIZONTAL, gamestate.piece.height)

    stateBeforeTP = GameState(gamestate.board, piece, gamestate.portals, isAi=gamestate.isAi, aiLevel=gamestate.aiLevel, aiMoves=gamestate.aiMoves)
    return Teleport(stateBeforeTP)


def Victory(gamestate: GameState):
    if gamestate.piece.piece_state == PieceState.UP and gamestate.board[gamestate.piece.position[1]][gamestate.piece.position[0]] == 3:
        return True
    else:
        return False


def Defeat(gamestate: GameState):
    head_position = gamestate.piece.position
    tail_position = (0, 0)

    if gamestate.piece.piece_state == PieceState.UP:
        tail_position = gamestate.piece.position
    elif gamestate.piece.piece_state == PieceState.HORIZONTAL:
        tail_position = (
            gamestate.piece.position[0] + gamestate.piece.height - 1, gamestate.piece.position[1])
    else:
        tail_position = (
            gamestate.piece.position[0], gamestate.piece.position[1] + gamestate.piece.height - 1)
    if position_is_0(gamestate.board, head_position) or position_is_0(gamestate.board, tail_position):
        return True
    else:
        return False


def Teleport(gamestate: GameState) -> GameState:
    if (gamestate.piece.piece_state == PieceState.UP) and (gamestate.piece.position in gamestate.portals.keys()):
        gamestate.piece.position = gamestate.portals[gamestate.piece.position]
    return gamestate




def get_exit(gamestate: GameState):
    for y in range(len(gamestate.board)):
        for x in range(len(gamestate.board[y])):
            if gamestate.board[y][x] == 3:
                return (x, y)


def h1(node: TreeNode):
    exit = get_exit(node.state)
    distance = (abs(node.state.piece.position[0] - exit[0]) + \
        abs(node.state.piece.position[1] - exit[1])) / ((node.state.piece.height+1)/2)
    portalKeys = list(node.state.portals.keys())

    if len(portalKeys) > 0:
        portal1_pos = portalKeys[0]
        portal2_pos = portalKeys[1]
        distance_from_p1_to_exit = abs(portal1_pos[0] - exit[0]) + \
        abs(portal1_pos[1] - exit[1])

        distance_from_p2_to_exit = abs(portal2_pos[0] - exit[0]) + \
        abs(portal2_pos[1] - exit[1])

        distance_from_player_to_p1 = abs(portal1_pos[0] - node.state.piece.position[0]) + \
        abs(portal1_pos[1] - node.state.piece.position[1])

        distance_from_player_to_p2 = abs(portal2_pos[0] - node.state.piece.position[0]) + \
        abs(portal2_pos[1] - node.state.piece.position[1])

        distance_to_exit_through_p1 = (distance_from_p2_to_exit + distance_from_player_to_p1) * ((node.state.piece.height+1)/2)
        distance_to_exit_through_p2 = (distance_from_p1_to_exit + distance_from_player_to_p2) * ((node.state.piece.height+1)/2)

        return min(distance, distance_to_exit_through_p1, distance_to_exit_through_p2)

    return distance #height+1/2


# Breadth-first Search
def breadth_first_search(initial_state, goal_state_func, operators_func):
    # create the root node in the search tree
    root = TreeNode(state=initial_state, move=None)
    queue = deque([root])   # initialize the queue to store the nodes
    visited = set([initial_state])

    while queue:
        node = queue.popleft()   # get first element in the queue
        if goal_state_func(node.state):   # check goal state
            return node

        # go through next states
        for state, moveDir in operators_func(node.state):
            visited.add(node.state)
            # create tree node with the new state
            newChild = TreeNode(state=state, parent=node.state, move=moveDir)

            # link child node to its parent in the tree
            if newChild not in visited:
                node.add_child(newChild)
                queue.append(newChild)
    return None

# Depth First Search
def depth_first_search(initial_state, goal_state_func, operators_func):
    root = TreeNode(initial_state)   # create the root node in the search tree
    queue = deque([root])   # initialize the queue to store the nodes
    visited = set([initial_state])

    while queue:
        node = queue.popleft()   # get first element in the queue
        visited.add(node.state)
        if goal_state_func(node.state):   # check goal state
            return node

        # go through next states
        for state, moveDir in operators_func(node.state):
            # create tree node with the new state
            newChild = TreeNode(state=state, parent=node.state, move=moveDir)
            # link child node to its parent in the tree
            if state not in visited:
                node.add_child(newChild)
                queue.appendleft(newChild)
    return None

# Greedy search
def greedy_search(initial_state, goal_state_func, operators_func, heuristic):
    setattr(TreeNode, "__lt__", lambda self,
            other: heuristic(self) < heuristic(other))
    root = TreeNode(initial_state)
    states = [root]
    visited = set()
    while states:

        node = heapq.heappop(states)
        visited.add(node.state)
        if goal_state_func(node.state):   # check goal state
            return node
        # go through next states
        for state, moveDir in operators_func(node.state):
            # create tree node with the new state
            newChild = TreeNode(state=state, parent=node.state, move=moveDir)
            # link child node to its parent in the tree
            if state not in visited:
                node.add_child(newChild)
                heapq.heappush(states, newChild)

    return None


def a_star_search(initial_state, heuristic):
    return greedy_search(initial_state, Victory, child_gamestates, lambda node: node.cost() + heuristic(node))

def weighted_a_star_search(initial_state, heuristic):
    return greedy_search(initial_state, Victory, child_gamestates, lambda node: node.cost() + 3*heuristic(node))

def execute_move(State: GameState, Move: MoveDirection, isAi):
    if (Move == MoveDirection.UP):
        if (isAi):
            time.sleep(1)
        return MoveUp(State), MoveDirection.UP
    elif (Move == MoveDirection.RIGHT):
        if (isAi):
            time.sleep(1)
        return MoveRight(State), MoveDirection.RIGHT
    elif (Move == MoveDirection.DOWN):
        if (isAi):
            time.sleep(1)
        return MoveDown(State), MoveDirection.DOWN
    else:
        if (isAi):
            time.sleep(1)
        return MoveLeft(State), MoveDirection.LEFT


def child_gamestates(gamestate):
    new_states = []
    if (not Defeat(MoveUp(gamestate))):
        new_states.append((MoveUp(gamestate), MoveDirection.UP))
    if (not Defeat(MoveRight(gamestate))):
        new_states.append((MoveRight(gamestate), MoveDirection.RIGHT))
    if (not Defeat(MoveDown(gamestate))):
        new_states.append((MoveDown(gamestate), MoveDirection.DOWN))
    if (not Defeat(MoveLeft(gamestate))):
        new_states.append((MoveLeft(gamestate), MoveDirection.LEFT))
    return new_states


def solution_moves(baseNode):
    moves = [baseNode.move]
    currNode = baseNode
    while (currNode.parent):
        if (currNode.parent.move):
            moves.append(currNode.parent.move)
        currNode = currNode.parent
    moves.reverse()
    return moves
