# chess/board.py

import pygame
from .pieces import Pawn, Rook, Knight, Bishop, Queen, King

class Board:
    def __init__(self):
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]
        self.load_pieces()

    def load_pieces(self):
        self.pieces = {}
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != '--':
                    color = piece[0]
                    piece_type = piece[1]
                    self.pieces[(row, col)] = self.create_piece(color, piece_type, (row, col))

    def create_piece(self, color, piece_type, position):
        piece_classes = {
            'P': Pawn,
            'R': Rook,
            'N': Knight,
            'B': Bishop,
            'Q': Queen,
            'K': King
        }
        return piece_classes[piece_type](color, PIECES[color + piece_type], position)
