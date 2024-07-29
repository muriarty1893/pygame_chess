# chess/pieces.py

import pygame

class Piece:
    def __init__(self, color, image, position):
        self.color = color
        self.image = image
        self.position = position

    def get_possible_moves(self, board):
        raise NotImplementedError("This method should be overridden by subclasses")

    def is_valid_move(self, start_pos, end_pos, board):
        raise NotImplementedError("This method should be overridden by subclasses")


class Pawn(Piece):
    def get_possible_moves(self, board):
        moves = []
        row, col = self.position
        if self.color == 'w':
            if row > 0 and board[row-1][col] == '--':
                moves.append((row-1, col))
                if row == 6 and board[row-2][col] == '--':
                    moves.append((row-2, col))
            if row > 0 and col > 0 and board[row-1][col-1].startswith('b'):
                moves.append((row-1, col-1))
            if row > 0 and col < 7 and board[row-1][col+1].startswith('b'):
                moves.append((row-1, col+1))
        else:
            if row < 7 and board[row+1][col] == '--':
                moves.append((row+1, col))
                if row == 1 and board[row+2][col] == '--':
                    moves.append((row+2, col))
            if row < 7 and col > 0 and board[row+1][col-1].startswith('w'):
                moves.append((row+1, col-1))
            if row < 7 and col < 7 and board[row+1][col+1].startswith('w'):
                moves.append((row+1, col+1))
        return moves


class Rook(Piece):
    def get_possible_moves(self, board):
        moves = []
        row, col = self.position
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] == '--':
                    moves.append((r, c))
                elif board[r][c][0] != self.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc
        return moves


class Knight(Piece):
    def get_possible_moves(self, board):
        moves = []
        row, col = self.position
        knight_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]
        for dr, dc in knight_moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] == '--' or board[r][c][0] != self.color:
                    moves.append((r, c))
        return moves


class Bishop(Piece):
    def get_possible_moves(self, board):
        moves = []
        row, col = self.position
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] == '--':
                    moves.append((r, c))
                elif board[r][c][0] != self.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc
        return moves


class Queen(Piece):
    def get_possible_moves(self, board):
        moves = []
        row, col = self.position
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] == '--':
                    moves.append((r, c))
                elif board[r][c][0] != self.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc
        return moves


class King(Piece):
    def get_possible_moves(self, board):
        moves = []
        row, col = self.position
        king_moves = [
            (1, 0), (1, 1), (1, -1),
            (0, 1), (0, -1),
            (-1, 0), (-1, 1), (-1, -1)
        ]
        for dr, dc in king_moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] == '--' or board[r][c][0] != self.color:
                    moves.append((r, c))
        return moves
