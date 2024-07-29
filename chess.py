import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT_COLOR = (200, 200, 0)

# Load and scale images
PIECES = {
    'bR': pygame.transform.scale(pygame.image.load('images/bR.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'bN': pygame.transform.scale(pygame.image.load('images/bN.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'bB': pygame.transform.scale(pygame.image.load('images/bB.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'bQ': pygame.transform.scale(pygame.image.load('images/bQ.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'bK': pygame.transform.scale(pygame.image.load('images/bK.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'bP': pygame.transform.scale(pygame.image.load('images/bP.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'wR': pygame.transform.scale(pygame.image.load('images/wR.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'wN': pygame.transform.scale(pygame.image.load('images/wN.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'wB': pygame.transform.scale(pygame.image.load('images/wB.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'wQ': pygame.transform.scale(pygame.image.load('images/wQ.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'wK': pygame.transform.scale(pygame.image.load('images/wK.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'wP': pygame.transform.scale(pygame.image.load('images/wP.png'), (SQUARE_SIZE, SQUARE_SIZE)),
}

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess')

def draw_board(screen, selected_square=None):
    colors = [WHITE, BLACK]
    for row in range(ROWS):
        for col in range(COLS):
            color = colors[(row + col) % 2]
            if selected_square and (row, col) == selected_square:
                color = HIGHLIGHT_COLOR
            pygame.draw.rect(screen, color, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(screen, board):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != '--':
                screen.blit(PIECES[piece], (col*SQUARE_SIZE, row*SQUARE_SIZE))

def move_piece(board, start_pos, end_pos):
    piece = board[start_pos[0]][start_pos[1]]
    board[start_pos[0]][start_pos[1]] = '--'
    board[end_pos[0]][end_pos[1]] = piece

def main():
    clock = pygame.time.Clock()
    board = [
        ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
        ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
        ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
    ]

    selected_square = None
    player_turn = 'w'  # 'w' for white's turn, 'b' for black's turn

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE
                if selected_square:
                    move_piece(board, selected_square, (row, col))
                    selected_square = None
                    player_turn = 'b' if player_turn == 'w' else 'w'
                else:
                    if board[row][col] != '--' and board[row][col][0] == player_turn:
                        selected_square = (row, col)

        draw_board(screen, selected_square)
        draw_pieces(screen, board)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
