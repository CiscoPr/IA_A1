import pygame
from enum import Enum
from dataclasses import dataclass
from collections import deque

import time


def position_is_0(board, position):
    if position[0] < 0 or position[0] >= len(board[0]) or position[1] < 0 or position[1] >= len(board):
        return True
    else: return board[position[1]][position[0]] == 0

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
    def __init__(self, position, piece_state, height):
        self.position= position
        self.piece_state = piece_state
        self.height = height
    
    def __hash__(self):
        return hash((self.piece_state, self.position))

class TreeNode:
    def __init__(self, state, parent=None, move = None):
        self.state = state
        self.parent = parent
        self.children = []
        self.move = move

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self
    


class GameState:

    def __init__(self, board, piece, isAi = False, aiLevel=0, aiMoves=[]):
        self.board = board
        self.piece = piece
        self.isAi = isAi
        self.aiMoves = aiMoves
        self.aiLevel=aiLevel
        

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
        if (self.aiLevel == 0):
            initial_node = breadth_first_search(self, Victory, child_gamestates)
            self.aiMoves = solution_moves(initial_node)
        elif (self.aiLevel == 1):
            initial_node = depth_first_search(self, Victory, child_gamestates) #TODO add more modes
            self.aiMoves = solution_moves(initial_node)


    def getAiMove(self):
        print(self.aiMoves)
        return self.aiMoves.pop(0)
       


def MoveUp(gamestate):
        if gamestate.piece.piece_state == PieceState.VERTICAL:
            piece = Piece((gamestate.piece.position[0],gamestate.piece.position[1]-1), PieceState.UP, gamestate.piece.height)
            return GameState(gamestate.board, piece, isAi=gamestate.isAi, aiLevel=gamestate.aiLevel, aiMoves=gamestate.aiMoves)
        elif gamestate.piece.piece_state == PieceState.HORIZONTAL:
            piece = Piece((gamestate.piece.position[0],gamestate.piece.position[1]-1), PieceState.HORIZONTAL, gamestate.piece.height)
            return GameState(gamestate.board, piece, isAi=gamestate.isAi, aiLevel=gamestate.aiLevel, aiMoves=gamestate.aiMoves)
        elif gamestate.piece.piece_state == PieceState.UP:
            piece = Piece((gamestate.piece.position[0],gamestate.piece.position[1]-gamestate.piece.height), PieceState.VERTICAL, gamestate.piece.height)
            return GameState(gamestate.board, piece, isAi=gamestate.isAi, aiLevel=gamestate.aiLevel, aiMoves=gamestate.aiMoves)
        return None

def MoveDown(gamestate):
        if gamestate.piece.piece_state == PieceState.VERTICAL:
            piece = Piece((gamestate.piece.position[0],gamestate.piece.position[1]+gamestate.piece.height), PieceState.UP, gamestate.piece.height)
            return GameState(gamestate.board, piece, isAi=gamestate.isAi, aiLevel=gamestate.aiLevel, aiMoves=gamestate.aiMoves)
        elif gamestate.piece.piece_state == PieceState.HORIZONTAL:
            piece = Piece((gamestate.piece.position[0],gamestate.piece.position[1]+1), PieceState.HORIZONTAL, gamestate.piece.height)
            return GameState(gamestate.board, piece, isAi=gamestate.isAi, aiLevel=gamestate.aiLevel, aiMoves=gamestate.aiMoves)
        elif gamestate.piece.piece_state == PieceState.UP:
            piece = Piece((gamestate.piece.position[0],gamestate.piece.position[1]+1), PieceState.VERTICAL, gamestate.piece.height)
            return GameState(gamestate.board, piece, isAi=gamestate.isAi, aiLevel=gamestate.aiLevel, aiMoves=gamestate.aiMoves)
        return None

def MoveLeft(gamestate):
        if gamestate.piece.piece_state == PieceState.VERTICAL:
            piece = Piece ((gamestate.piece.position[0]-1,gamestate.piece.position[1]), PieceState.VERTICAL, gamestate.piece.height)
            return GameState(gamestate.board, piece, isAi=gamestate.isAi, aiLevel=gamestate.aiLevel, aiMoves=gamestate.aiMoves)
        elif gamestate.piece.piece_state == PieceState.HORIZONTAL:
            piece = Piece ((gamestate.piece.position[0]-1,gamestate.piece.position[1]), PieceState.UP, gamestate.piece.height)
            return GameState(gamestate.board, piece, isAi=gamestate.isAi, aiLevel=gamestate.aiLevel, aiMoves=gamestate.aiMoves)
        elif gamestate.piece.piece_state == PieceState.UP:
            piece = Piece ((gamestate.piece.position[0]-gamestate.piece.height,gamestate.piece.position[1]), PieceState.HORIZONTAL, gamestate.piece.height)
            return GameState(gamestate.board, piece, isAi=gamestate.isAi, aiLevel=gamestate.aiLevel, aiMoves=gamestate.aiMoves)
        return None

def MoveRight(gamestate):
        if gamestate.piece.piece_state == PieceState.VERTICAL:
            piece = Piece ((gamestate.piece.position[0]+1,gamestate.piece.position[1]), PieceState.VERTICAL, gamestate.piece.height)
            return GameState(gamestate.board, piece, isAi=gamestate.isAi, aiLevel=gamestate.aiLevel, aiMoves=gamestate.aiMoves)
        elif gamestate.piece.piece_state == PieceState.HORIZONTAL:
            piece = Piece ((gamestate.piece.position[0]+gamestate.piece.height,gamestate.piece.position[1]), PieceState.UP, gamestate.piece.height)
            return GameState(gamestate.board, piece, isAi=gamestate.isAi, aiLevel=gamestate.aiLevel, aiMoves=gamestate.aiMoves)
        elif gamestate.piece.piece_state == PieceState.UP:
            piece = Piece((gamestate.piece.position[0]+1,gamestate.piece.position[1]), PieceState.HORIZONTAL, gamestate.piece.height)
            return GameState(gamestate.board, piece, isAi=gamestate.isAi, aiLevel=gamestate.aiLevel, aiMoves=gamestate.aiMoves)

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
        if position_is_0(gamestate.board, head_position) or position_is_0(gamestate.board, tail_position):
            return True
        else:
            return False

    # Breadth-first Search

def breadth_first_search(initial_state, goal_state_func, operators_func):
    root = TreeNode(state=initial_state, move=None)   # create the root node in the search tree
    queue = deque([root])   # initialize the queue to store the nodes
    visited = set([initial_state])


    while queue:
        node = queue.popleft()   # get first element in the queue
        if goal_state_func(node.state):   # check goal state
            return node

        for state, moveDir in operators_func(node.state):   # go through next states
            visited.add(node.state)
            # create tree node with the new state
            newChild = TreeNode(state=state, parent=node.state, move=moveDir)

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

        for state, moveDir in operators_func(node.state):   # go through next states
            # create tree node with the new state
            newChild = TreeNode(state=state, parent=node.state, move=moveDir)
            # link child node to its parent in the tree
            if state not in visited:
              node.add_child(newChild)
              queue.appendleft(newChild)
    return None

def execute_move(State: GameState, Move: MoveDirection, isAi):
    if (Move == MoveDirection.UP):
        if(isAi):
            time.sleep(0.2)
        return MoveUp(State), MoveDirection.UP 
    elif (Move == MoveDirection.RIGHT):
        if(isAi):
            time.sleep(0.2)
        return MoveRight(State), MoveDirection.RIGHT
    elif (Move == MoveDirection.DOWN):
        if(isAi):
            time.sleep(0.2)
        return MoveDown(State), MoveDirection.DOWN
    else:
        if(isAi):
            time.sleep(0.2)
        return MoveLeft(State), MoveDirection.LEFT


def child_gamestates(gamestate):
    new_states = []
    if(not Defeat(MoveUp(gamestate))):
        new_states.append((MoveUp(gamestate), MoveDirection.UP))
    if(not Defeat(MoveRight(gamestate))):
        new_states.append((MoveRight(gamestate), MoveDirection.RIGHT))
    if(not Defeat(MoveDown(gamestate))):
        new_states.append((MoveDown(gamestate), MoveDirection.DOWN))
    if(not Defeat(MoveLeft(gamestate))):
        new_states.append((MoveLeft(gamestate), MoveDirection.LEFT))
    return new_states

def solution_moves(baseNode):
    moves = [baseNode.move]
    currNode = baseNode
    while(currNode.parent):
        if (currNode.parent.move):
            moves.append(currNode.parent.move)
        currNode = currNode.parent
    moves.reverse()
    return moves
    

