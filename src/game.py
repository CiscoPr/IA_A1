import pygame
from enum import Enum
from dataclasses import dataclass
from collections import deque




def position_is_0(board, position):
    return board[position[1]][position[0]] == 0

class PieceState(Enum):
    UP = 1
    HORIZONTAL = 2
    VERTICAL = 3

class MoveDirection(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

@dataclass
class Piece:
    def __init__(self,position, piece_state, height):
        self.position= position
        self.piece_state = piece_state
        self.height = height

class TreeNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self


class GameState:

    def __init__(self, board, piece):
        self.board = board
        self.piece = piece
        

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False


def MoveUp(gamestate):
        if gamestate.piece.piece_state == PieceState.VERTICAL:
            piece = Piece((gamestate.piece.position[0],gamestate.piece.position[1]-1), PieceState.UP, gamestate.piece.height)
            return GameState(gamestate.board, piece)
        elif gamestate.piece.piece_state == PieceState.HORIZONTAL:
            piece = Piece((gamestate.piece.position[0],gamestate.piece.position[1]-1), PieceState.HORIZONTAL, gamestate.piece.height)
            return GameState(gamestate.board, piece)
        elif gamestate.piece.piece_state == PieceState.UP:
            piece = Piece((gamestate.piece.position[0],gamestate.piece.position[1]-gamestate.piece.height), PieceState.VERTICAL, gamestate.piece.height)
            return GameState(gamestate.board, piece)
        return None

def MoveDown(gamestate):
        if gamestate.piece.piece_state == PieceState.VERTICAL:
            piece = Piece((gamestate.piece.position[0],gamestate.piece.position[1]+gamestate.piece.height), PieceState.UP, gamestate.piece.height)
            return GameState(gamestate.board, piece)
        elif gamestate.piece.piece_state == PieceState.HORIZONTAL:
            piece = Piece((gamestate.piece.position[0],gamestate.piece.position[1]+1), PieceState.HORIZONTAL, gamestate.piece.height)
            return GameState(gamestate.board, piece)
        elif gamestate.piece.piece_state == PieceState.UP:
            piece = Piece((gamestate.piece.position[0],gamestate.piece.position[1]+1), PieceState.VERTICAL, gamestate.piece.height)
            return GameState(gamestate.board, piece)
        return None

def MoveLeft(gamestate):
        if gamestate.piece.piece_state == PieceState.VERTICAL:
            piece = Piece ((gamestate.piece.position[0]-1,gamestate.piece.position[1]), PieceState.VERTICAL, gamestate.piece.height)
            return GameState(gamestate.board, piece)
        elif gamestate.piece.piece_state == PieceState.HORIZONTAL:
            piece = Piece ((gamestate.piece.position[0]-1,gamestate.piece.position[1]), PieceState.UP, gamestate.piece.height)
            return GameState(gamestate.board, piece)
        elif gamestate.piece.piece_state == PieceState.UP:
            piece = Piece ((gamestate.piece.position[0]-gamestate.piece.height,gamestate.piece.position[1]), PieceState.HORIZONTAL, gamestate.piece.height)
            return GameState(gamestate.board, piece)
        return None

def MoveRight(gamestate):
        if gamestate.piece.piece_state == PieceState.VERTICAL:
            piece = Piece ((gamestate.piece.position[0]+1,gamestate.piece.position[1]), PieceState.VERTICAL, gamestate.piece.height)
            return GameState(gamestate.board, piece)
        elif gamestate.piece.piece_state == PieceState.HORIZONTAL:
            piece = Piece ((gamestate.piece.position[0]+gamestate.piece.height,gamestate.piece.position[1]), PieceState.UP, gamestate.piece.height)
            return GameState(gamestate.board, piece)
        elif gamestate.piece.piece_state == PieceState.UP:
            piece = Piece((gamestate.piece.position[0]+1,gamestate.piece.position[1]), PieceState.HORIZONTAL, gamestate.piece.height)
            return GameState(gamestate.board, piece)

def Victory(gamestate):

        if gamestate.piece.piece_state == PieceState.UP and gamestate.board[gamestate.piece.position[1]][gamestate.piece.position[0]] == 3:
            return True
        else:
            return False


def Defeat(gamestate):
        head_position = gamestate.piece.position
        tail_position = (0,0)

        if gamestate.piece.piece_state == PieceState.UP:
            tail_position = gamestate.piece.position
        elif gamestate.piece.piece_state == PieceState.HORIZONTAL:
            tail_position = (gamestate.piece.position[0] + gamestate.piece.height - 1, gamestate.piece.position[1])
        else:
            tail_position = (gamestate.piece.position[0], gamestate.piece.position[1] + gamestate.piece.height - 1)
        print (head_position)
        print (tail_position)
        if position_is_0(gamestate.board, head_position) or position_is_0(gamestate.board, tail_position):
            return True
        else:
            return False

    # Breadth-first Search

def breadth_first_search(initial_state, goal_state_func, operators_func):
    root = TreeNode(initial_state)   # create the root node in the search tree
    queue = deque([root])   # initialize the queue to store the nodes
    visited = set([initial_state])


    while queue:
        node = queue.popleft()   # get first element in the queue
        if goal_state_func(node.state):   # check goal state
            return node

        for state in operators_func(node.state):   # go through next states
            visited.add(node.state)
            # create tree node with the new state
            newChild = TreeNode(state=state)

            # link child node to its parent in the tree
            if newChild not in visited:
              node.add_child(newChild)
              queue.append(newChild)
    return None

def depth_first_search(initial_state, goal_state_func, operators_func):
    root = TreeNode(initial_state)   # create the root node in the search tree
    queue = deque([root])   # initialize the queue to store the nodes
    visited = set([initial_state])

    while queue:
        node = queue.popleft()   # get first element in the queue
        visited.add(node.state)
        if goal_state_func(node.state):   # check goal state
            return node

        for state in operators_func(node.state):   # go through next states
            # create tree node with the new state
            newChild = TreeNode(state=state)

            # link child node to its parent in the tree
            if state not in visited:
              node.add_child(newChild)
              queue.appendleft(newChild)
    return None

def execute_move(State: GameState, Move: MoveDirection):
    if (Move == MoveDirection.UP):
        State = MoveUp(State)
    elif (Move == MoveDirection.RIGHT):
        State = MoveRight(State)
    elif (Move == MoveDirection.DOWN):
        State = MoveDown(State)
    else:
        State = MoveLeft(State)
    return State


def child_gamestates(state):
    new_states = []
    if(not state.MoveUp.Defeat):
        new_states.append()


