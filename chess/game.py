# chess/game.py

import pygame
from .board.py import Board
from .utils import draw_board, draw_button, show_check_alert, show_invalid_move_alert

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.selected_square = None
        self.possible_moves = []
        self.move_history = []
        self.player_turn = 'w'

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_down(event.pos)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                self.undo_last_move()

    def handle_mouse_down(self, pos):
        if self.undo_button.collidepoint(pos):
            self.player_turn = self.undo_last_move()
        else:
            row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE
            if self.selected_square:
                if self.board.is_valid_move(self.selected_square, (row, col)):
                    self.move_history.append((self.selected_square, (row, col), self.player_turn))
                    self.board.move_piece(self.selected_square, (row, col))
                    if self.board.check_game_over():
                        print(f"Game over! {self.player_turn} wins!")
                        pygame.quit()
                        sys.exit()
                    if self.board.is_in_check('b'):
                        show_check_alert('Black')
                    if self.board.is_in_check('w'):
                        show_check_alert('White')
                    self.selected_square = None
                    self.possible_moves = []
                    self.player_turn = 'b' if self.player_turn == 'w' else 'w'
                else:
                    show_invalid_move_alert()
                    self.selected_square = None
                    self.possible_moves = []
            else:
                if self.board.is_own_piece((row, col), self.player_turn):
                    self.selected_square = (row, col)
                    self.possible_moves = self.board.get_possible_moves(self.selected_square)

    def undo_last_move(self):
        if self.move_history:
            last_move = self.move_history.pop()
            self.board.move_piece(last_move[1], last_move[0])  # Undo the move
            return last_move[2]  # Return the player turn before the last move

    def update(self):
        self.undo_button = draw_button(self.screen, 'Undo', WIDTH - 100, HEIGHT - 50, 80, 40)

    def render(self):
        draw_board(self.screen, self.selected_square, self.possible_moves)
        self.board.draw(self.screen)
        pygame.display.flip()
