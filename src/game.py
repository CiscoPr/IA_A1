import pygame
from enum import Enum
from dataclasses import dataclass

filepath = "src\maps\map01"

class PieceState(Enum):
   UP = 1
   HORIZONTAL = 2
   VERTICAL = 3

@dataclass
class Piece:
    position: tuple
    piece_state: PieceState


class GameState:

    def __init__(self, filepath):
        self.board: list(list(int)) = []
        self.piece: Piece = Piece((0,0), PieceState.UP)
        with open(filepath) as f:
            lines = f.read().splitlines()
            for (y, line) in enumerate(lines):
                current_row = []
                print("Splitted line = " + str(line.split(' ')))
                for (x, char) in enumerate(line.split(' ')):
                    if (char == '3'):
                        print(f"Found 3: x is {x} and y is {y}")
                        self.piece.position = (x, y)
                        current_row.append(1)
                        continue
                    current_row.append(int(char))
                self.board.append(current_row)

        print("Finished initializing GameState.")
        print("Board = " + str(self.board))
        print("Piece = " + str(self.piece))

myGameState = GameState(filepath)

