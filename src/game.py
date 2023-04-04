from enum import Enum
from dataclasses import dataclass
from collections import deque
import heapq
import time
import sys
from typing import Callable
from memory_profiler import memory_usage

instruction_count=0

def position_is_0(board: list[list[int]], position: tuple[int, int]) -> bool:
    """Checks if there's a 0 in the board at the spicified position

    Args:
        board: The game's board
        position: A tuple containing the position that is to be checked
    
    Returns:
        A boolean indicating the result
    """
    if position[0] < 0 or position[0] >= len(board[0]) or position[1] < 0 or position[1] >= len(board):
        return True
    else:
        return board[position[1]][position[0]] == 0

def funcTime(fun: Callable, *args) -> None:
    """Function to measure time of execution of a given function, printing it to the standard output

    Args:
        fun: function to be timed
        args: arguments that will be passed to the function
    
    Returns:
        Nothing.
    """
    start = time.time()
    res = fun(*args)
    end = time.time()
    print (round(end-start,6))


def maxMemory(fun: Callable, *args) -> None:
    """Function to measure max memory usage of a given function, printing it to the standard output

    Args:
        fun: function to be measured
        args: arguments that will be passed to the function
        
    Returns:
        Nothing.
    """
    list=[arg for arg in args]
    mem_usage = memory_usage((fun, list))
    print('Maximum memory usage: %s' % max(mem_usage))        


def tracefunc(frame, event: str, arg) -> Callable:
    """Function to measure number of instructions of a given function and increase global counter

    Args:
        event: Name of the event we wish to measure

    Returns: ? From chatgpt 
    """
    if event == "line":
        global instruction_count
        instruction_count += 1
    return tracefunc


class PieceState(Enum):
    """ Enum that defines the state that the piece is in
    """
    UP = 1
    HORIZONTAL = 2
    VERTICAL = 3


class AiLevel(Enum):
    """ Enum that defines the diferent bot algorithms
    """

    BFS = 0
    DFS = 1
    GREEDY = 2
    ASTAR = 3
    WASTAR = 4


class MoveDirection(Enum):
    """ Enum that defines in which direction a move was done
    """
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


@dataclass
class Piece:
    """ Class that contains the piece's position, state (PieceState) and height.
    
    Fields:
        position: tuple[int, int] - The coordinate of the piece's part closest to (0, 0)
        piece_state: PieceState - Current state of the piece
        height: The piece's height
    """
    def __init__(self, position: tuple[int, int], piece_state: PieceState, height: int):
        self.position: tuple[int, int] = position
        self.piece_state: PieceState = piece_state
        self.height: int = height

    def __hash__(self):
        return hash((self.piece_state, self.position))


class TreeNode:
    """ Class that defines the tree node to be used by the algorithms
    
    Fields:
        state: Gamestate corresponding to the node
        parent: parent node
        move: operator that generated this node
    """
    def __init__(self, state, parent=None, move: MoveDirection | None = None):
        self.state: GameState = state
        self.parent = parent
        self.children = []
        self.move: MoveDirection | None = move

    def add_child(self, child_node) -> None:
        self.children.append(child_node)
        child_node.parent = self

    def cost(self) -> int:
        counter: int = 0
        node = self
        while (node.parent):
            counter += 1
            node = node.parent
        return counter


class GameState:
    """
       Class that defines the game state to be used by the functions along the program
       
    Fields:
        board: a list of lists corresponding to the game board
        piece: an object representing a player piece
        portals: a dictionary which represents the portals and their coordinates
        isAi: a boolean to determine if the player chose AI mode or not
        aiLevel: sets the value of the AI
        aiMoves: a list that will contain all the moves for the AI
    """
    def __init__(self, board: list[list[int]], piece: Piece, portals: dict[tuple[int, int], tuple[int, int]], isAi: bool = False, aiLevel: AiLevel = AiLevel.BFS, aiMoves: list[MoveDirection]=[]):
        self.board: list[list[int]] = board
        self.piece: Piece = piece
        self.isAi: bool = isAi
        self.aiMoves: list[MoveDirection] = aiMoves
        self.aiLevel: AiLevel = aiLevel
        self.portals: dict[tuple[int, int], tuple[int, int]] = portals

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __hash__(self) -> int:
        return hash(self.piece)
    ''' - '''

    def __str__(self) -> str:
        return "(" + str(self.piece) + ")"


    # Commented the performance tests
    def setAiMoves(self) -> None:
        global instruction_count

        if (self.aiLevel == AiLevel.BFS.value):
            #funcTime(breadth_first_search,self,Victory,child_gamestates)
            #maxMemory(breadth_first_search,self,Victory,child_gamestates) # Only tested in linux, may crash in other OS
            #sys.settrace(tracefunc)
            initial_node = breadth_first_search(
                self, Victory, child_gamestates)
            if (initial_node is None):
                print("Error: initialNode from breadth_first_search was None")
                sys.exit(1)
            #sys.settrace(None)
            #print(f"Number of instructions executed: {instruction_count}")
            #instruction_count=0
            self.aiMoves = solution_moves(initial_node)
        elif (self.aiLevel == AiLevel.DFS.value):
            #funcTime(depth_first_search,self,Victory,child_gamestates)
            #maxMemory(depth_first_search,self,Victory,child_gamestates)
            #sys.settrace(tracefunc)
            initial_node = depth_first_search(
                self, Victory, child_gamestates)
            #sys.settrace(None)
            #print(f"Number of instructions executed: {instruction_count}")
            #instruction_count=0
            if initial_node is None:
                print("Error: initialNode from DFS was None")
                sys.exit(1)

            self.aiMoves = solution_moves(initial_node)

        elif (self.aiLevel == AiLevel.GREEDY.value):
            #funcTime(greedy_search,self,Victory,child_gamestates,h1)
            #maxMemory(greedy_search,self,Victory,child_gamestates,h1)
            #sys.settrace(tracefunc)
            initial_node = greedy_search(self, Victory, child_gamestates, h1)
            #sys.settrace(None)
            #print(f"Number of instructions executed: {instruction_count}")
            #instruction_count=0
            if (initial_node is None):
                print("Error: initialNode from greedy was None")
                sys.exit(1)
            self.aiMoves = solution_moves(initial_node)

        elif (self.aiLevel == AiLevel.ASTAR.value):
            #funcTime(a_star_search,self,h1)
            #maxMemory(a_star_search, self, h1)
            #sys.settrace(tracefunc)
            initial_node = a_star_search(self, h1)
            #sys.settrace(None)
            #print(f"Number of instructions executed: {instruction_count}")
            #instruction_count=0
            if (initial_node is None):
                print("Error: initialNode from Astar was None")
                sys.exit(1)
            self.aiMoves = solution_moves(initial_node)
        elif (self.aiLevel == AiLevel.WASTAR.value):
            #funcTime(weighted_a_star_search,self,h1)
            #maxMemory(weighted_a_star_search,self,h1)
            #sys.settrace(tracefunc)
            initial_node = weighted_a_star_search(self, h1)
            #sys.settrace(None)
            #print(f"Number of instructions executed: {instruction_count}")
            #instruction_count=0
            if (initial_node is None):
                print("Error: initialNode from Weighted Astar was None")
                sys.exit(1)
            self.aiMoves = solution_moves(initial_node)
        

    def getAiMove(self) -> MoveDirection:
        return self.aiMoves.pop(0)


def MoveUp(gamestate: GameState) -> GameState:
    """ Creates a new GameState based on the input GameState, in which the piece has moved up once
    
    Args:
        gamestate: GameState - Input gamestate

    Returns:
        Transformed GameState
    """
    piece = None
    if gamestate.piece.piece_state == PieceState.VERTICAL:
        piece = Piece(
            (gamestate.piece.position[0], gamestate.piece.position[1]-1), PieceState.UP, gamestate.piece.height)
    elif gamestate.piece.piece_state == PieceState.HORIZONTAL:
        piece = Piece((gamestate.piece.position[0], gamestate.piece.position[1]-1),
                      PieceState.HORIZONTAL, gamestate.piece.height)
    else:
        piece = Piece((gamestate.piece.position[0], gamestate.piece.position[1] -
                      gamestate.piece.height), PieceState.VERTICAL, gamestate.piece.height)

    stateBeforeTP = GameState(gamestate.board, piece, gamestate.portals, isAi=gamestate.isAi, aiLevel=gamestate.aiLevel, aiMoves=gamestate.aiMoves)
    return Teleport(stateBeforeTP)


def MoveDown(gamestate: GameState) -> GameState:
    """ Creates a new GameState based on the input GameState, in which the piece has moved dpwn once
    
    Args:
        gamestate: GameState - Input gamestate

    Returns:
        Transformed GameState
    """
    piece = None

    if gamestate.piece.piece_state == PieceState.VERTICAL:
        piece = Piece((gamestate.piece.position[0], gamestate.piece.position[1] +
                      gamestate.piece.height), PieceState.UP, gamestate.piece.height)
    elif gamestate.piece.piece_state == PieceState.HORIZONTAL:
        piece = Piece((gamestate.piece.position[0], gamestate.piece.position[1]+1),
                      PieceState.HORIZONTAL, gamestate.piece.height)
    else:
        piece = Piece(
            (gamestate.piece.position[0], gamestate.piece.position[1]+1), PieceState.VERTICAL, gamestate.piece.height)

    stateBeforeTP = GameState(gamestate.board, piece, gamestate.portals, isAi=gamestate.isAi, aiLevel=gamestate.aiLevel, aiMoves=gamestate.aiMoves)
    return Teleport(stateBeforeTP)



def MoveLeft(gamestate: GameState) -> GameState:
    """ Creates a new GameState based on the input GameState, in which the piece has moved left once
    
    Args:
        gamestate: GameState - Input gamestate

    Returns:
        Transformed GameState
    """
    piece = None
    if gamestate.piece.piece_state == PieceState.VERTICAL:
        piece = Piece(
            (gamestate.piece.position[0]-1, gamestate.piece.position[1]), PieceState.VERTICAL, gamestate.piece.height)
    elif gamestate.piece.piece_state == PieceState.HORIZONTAL:
        piece = Piece(
            (gamestate.piece.position[0]-1, gamestate.piece.position[1]), PieceState.UP, gamestate.piece.height)
    else:
        piece = Piece((gamestate.piece.position[0]-gamestate.piece.height,
                      gamestate.piece.position[1]), PieceState.HORIZONTAL, gamestate.piece.height)

    stateBeforeTP = GameState(gamestate.board, piece, gamestate.portals, isAi=gamestate.isAi, aiLevel=gamestate.aiLevel, aiMoves=gamestate.aiMoves)
    return Teleport(stateBeforeTP)



def MoveRight(gamestate: GameState) -> GameState:
    """ Creates a new GameState based on the input GameState, in which the piece has moved right once
    
    Args:
        gamestate: GameState - Input gamestate

    Returns:
        Transformed GameState
    """
    piece = None
    if gamestate.piece.piece_state == PieceState.VERTICAL:
        piece = Piece(
            (gamestate.piece.position[0]+1, gamestate.piece.position[1]), PieceState.VERTICAL, gamestate.piece.height)
    elif gamestate.piece.piece_state == PieceState.HORIZONTAL:
        piece = Piece((gamestate.piece.position[0]+gamestate.piece.height,
                      gamestate.piece.position[1]), PieceState.UP, gamestate.piece.height)
    else:
        piece = Piece((gamestate.piece.position[0]+1, gamestate.piece.position[1]),
                      PieceState.HORIZONTAL, gamestate.piece.height)

    stateBeforeTP = GameState(gamestate.board, piece, gamestate.portals, isAi=gamestate.isAi, aiLevel=gamestate.aiLevel, aiMoves=gamestate.aiMoves)
    return Teleport(stateBeforeTP)


def Victory(gamestate: GameState) -> bool:
    """ Checks if the current GameState is a winning one, aka if the player is at the exit and upright. 
    
    Args:
        gamestate: GameState - Input gamestate

    Returns:
        Bool indicating the result
    """
    if gamestate.piece.piece_state == PieceState.UP and gamestate.board[gamestate.piece.position[1]][gamestate.piece.position[0]] == 3:
        return True
    else:
        return False


def Defeat(gamestate: GameState) -> bool:
    """ Checks if the current GameState is a losing one, aka if one of the edges of the piece is not on stable ground. 

    Args:
        gamestate: GameState - Input gamestate

    Returns:
        Bool indicating the result
    """

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
    """ Checks if the player is standing in a portal, and if it is execute the teleportation and update the gamestate. 
    
    Args:
        gamestate: GameState - Input GameState

    Returns:
        The updated (or not) GameState
    """

    if (gamestate.piece.piece_state == PieceState.UP) and (gamestate.piece.position in gamestate.portals.keys()):
        gamestate.piece.position = gamestate.portals[gamestate.piece.position]
    return gamestate




def get_exit(gamestate: GameState) -> tuple[int, int]:
    """ Finds the exit in a given GameState's board 
    
    Args:
        gamestate: GameState - Input gamestate

    Returns:
        Tuple with the exit's coordinates
    """

    for y in range(len(gamestate.board)):
        for x in range(len(gamestate.board[y])):
            if gamestate.board[y][x] == 3:
                return (x, y)
    return (-1, -1)


def h1(node: TreeNode) -> float:
    """ Evaluates how good the current state is based on manhattan distance, taking into account the existing portals.
    Returns the "distance", so the lower the better
    
    Args:
        node: TreeNode - The node with the GameState to be evaluated

    Returns:
        A float with the calculated "distance"
    """

    exit: tuple[int, int] = get_exit(node.state)
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
def breadth_first_search(initial_state: GameState, goal_state_func: Callable, operators_func: Callable) -> TreeNode | None:
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
def depth_first_search(initial_state: GameState, goal_state_func: Callable, operators_func: Callable) -> TreeNode | None:
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
def greedy_search(initial_state: GameState, goal_state_func: Callable, operators_func: Callable, heuristic: Callable) -> TreeNode | None:
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

 # A* 
def a_star_search(initial_state: GameState, heuristic: Callable) -> TreeNode | None:
    return greedy_search(initial_state, Victory, child_gamestates, lambda node: node.cost() + heuristic(node))


# Weighted A* with coeficient 3 
def weighted_a_star_search(initial_state, heuristic: Callable) -> TreeNode | None:
    return greedy_search(initial_state, Victory, child_gamestates, lambda node: node.cost() + 3*heuristic(node))



def execute_move(State: GameState, Move: MoveDirection, isAi) -> tuple[GameState, MoveDirection]:
    """ Executes a move and updates GameState based on it and the input move by using MoveUp, MoveLeft... 
    
    Args:
        State: GameState - Input gamestate
        Move: MoveDirection - Direction in which the piece will move
        isAI: Boolean - If it is AI do sleep as the move is instantaneous

    Returns:
        Updated GameState
    """

  
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


def child_gamestates(gamestate: GameState) -> list[tuple[GameState, MoveDirection]]:
    
    """ Function to generate all the moves that don't lead to defeat
    
    Args:
        gamestate: GameState - Input gamestate

    Returns:
        newstates: tuple of the new game state and the operator used to generate it 
    """

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


def solution_moves(baseNode: TreeNode) -> list[MoveDirection]:
    """ Uses the tree's nodes' information to get the list of moves that
    the algorithm determined and returns them 
    
    Args:
        baseNode: TreeNode - The node corresponding to the last
        move we want to check, usually the node corresponding to the winning state.

    Returns:
        A list of all the moves used to reach the input node, in order.
    """

    moves = [baseNode.move]
    currNode = baseNode
    while (currNode.parent):
        if (currNode.parent.move):
            moves.append(currNode.parent.move)
        currNode = currNode.parent
    moves.reverse()
    return moves

