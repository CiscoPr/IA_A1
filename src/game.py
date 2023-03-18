import pygame
from enum import Enum
from dataclasses import dataclass
from collections import deque

filepath = "../src/maps/map01"

def position_is_0(board, position):
    return board[position[1][position[0]]] == "0"

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

    def __init__(self, filepath):
        self.board: list(list(int)) = []
        self.piece: Piece = Piece((0,0), PieceState.UP)
        with open(filepath) as f:
            lines = f.read().splitlines()
            for (y, line) in enumerate(lines):
                current_row = []
                #print("Splitted line = " + str(line.split(' ')))
                for (x, char) in enumerate(line.split(' ')):
                    if (char == '3'):
                        #print(f"Found 3: x is {x} and y is {y}")
                        self.piece.position = (x, y)
                        current_row.append(1)
                        continue
                    current_row.append(int(char))
                self.board.append(current_row)

        #print("Finished initializing GameState.")
        #print("Board = " + str(self.board))
        #print("Piece = " + str(self.piece))
    

    def MoveUp(self):
        if self.piece.piece_state == PieceState.VERTICAL:
            self.piece = Piece((self.piece.position[0],self.piece.position[1]-1), PieceState.UP)
        elif self.piece.piece_state == PieceState.HORIZONTAL:
            self.piece = Piece((self.piece.position[0],self.piece.position[1]-1), PieceState.HORIZONTAL)
        elif self.piece.piece_state == PieceState.UP:
            self.piece = Piece((self.piece.position[0],self.piece.position[1]-self.piece.height), PieceState.VERTICAL)
       
    def MoveDown(self):
        if self.piece.piece_state == PieceState.VERTICAL:
            self.piece = Piece((self.piece.position[0],self.piece.position[1]+self.piece.height), PieceState.UP)
        elif self.piece.piece_state == PieceState.HORIZONTAL:
            self.piece = Piece((self.piece.position[0],self.piece.position[1]+1), PieceState.HORIZONTAL)
        elif self.piece.piece_state == PieceState.UP:
            self.piece = Piece((self.piece.position[0],self.piece.position[1]+1), PieceState.VERTICAL)
        
    def MoveLeft(self):
        if self.piece.piece_state == PieceState.VERTICAL:
            self.piece = Piece ((self.piece.position[0]-1,self.piece.position[1]), PieceState.VERTICAL)
        elif self.piece.piece_state == PieceState.HORIZONTAL:
            self.piece = Piece ((self.piece.position[0]-1,self.piece.position[1]), PieceState.UP)
        elif self.piece.piece_state == PieceState.UP:
            self.piece = Piece ((self.piece.position[0]-self.piece.height,self.piece.position[1]), PieceState.HORIZONTAL)
        
    def MoveRight(self):
        if self.piece.piece_state == PieceState.VERTICAL:
            self.piece = Piece ((self.piece.position[0]+1,self.piece.position[1]), PieceState.VERTICAL)
        elif self.piece.piece_state == PieceState.HORIZONTAL:
            self.piece = Piece ((self.piece.position[0]+self.piece.height,self.piece.position[1]), PieceState.UP)
        elif self.piece.piece_state == PieceState.UP:
            self.piece = Piece ((self.piece.position[0]+1,self.piece.position[1]), PieceState.Horizontal)
    
    def Victory(self):
        if self.piece.piece_state == PieceState.UP and self.board[self.piece.position[1]][self.piece.piece_state[0]] == "2":
            return True
        else: 
            return False

    def Defeat(self):
        head_position = self.piece.position
        tail_position = (0,0)

        if self.piece.piece_state == PieceState.UP:
            tail_position = self.piece.position
        elif self.piece.piece_state == PieceState.HORIZONTAL:
            tail_position = (self.piece.position[0] + self.piece.height - 1, self.piece.position[1])
        else:
            tail_position = (self.piece.position[0], self.piece.position[1] + self.piece.height - 1)

        if position_is_0(self.board, head_position) or position_is_0(self.board, tail_position):
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
        State.MoveUp()
    elif (Move == MoveDirection.RIGHT):
        State.MoveRight()
    elif (Move == MoveDirection.DOWN):
        State.MoveDown()
    else:
        State.MoveLeft()
    return State 


        

myGameState = GameState(filepath)
myGameState.MoveDown()
print(myGameState.piece.position)