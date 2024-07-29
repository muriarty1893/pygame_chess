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

def is_valid_move(board, start_pos, end_pos):
    piece = board[start_pos[0]][start_pos[1]]
    target = board[end_pos[0]][end_pos[1]]
    if target != '--' and target[0] == piece[0]:
        return False  # Can't capture own piece

    direction = (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
    if piece[1] == 'P':  # Pawn
        if piece[0] == 'w':
            if direction == (-1, 0) and target == '--':
                return True
            if direction == (-2, 0) and start_pos[0] == 6 and target == '--' and board[start_pos[0] - 1][start_pos[1]] == '--':
                return True
            if direction in [(-1, -1), (-1, 1)] and target != '--' and target[0] == 'b':
                return True
        else:
            if direction == (1, 0) and target == '--':
                return True
            if direction == (2, 0) and start_pos[0] == 1 and target == '--' and board[start_pos[0] + 1][start_pos[1]] == '--':
                return True
            if direction in [(1, -1), (1, 1)] and target != '--' and target[0] == 'w':
                return True
    elif piece[1] == 'R':  # Rook
        if direction[0] == 0 or direction[1] == 0:
            return True
    elif piece[1] == 'N':  # Knight
        if abs(direction[0] * direction[1]) == 2:
            return True
    elif piece[1] == 'B':  # Bishop
        if abs(direction[0]) == abs(direction[1]):
            return True
    elif piece[1] == 'Q':  # Queen
        if direction[0] == 0 or direction[1] == 0 or abs(direction[0]) == abs(direction[1]):
            return True
    elif piece[1] == 'K':  # King
        if max(abs(direction[0]), abs(direction[1])) == 1:
            return True
    return False

def move_piece(board, start_pos, end_pos):
    piece = board[start_pos[0]][start_pos[1]]
    board[start_pos[0]][start_pos[1]] = '--'
    board[end_pos[0]][end_pos[1]] = piece

def check_game_over(board):
    kings = [piece for row in board for piece in row if piece[1] == 'K']
    return len(kings) < 2

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
                    if is_valid_move(board, selected_square, (row, col)):
                        move_piece(board, selected_square, (row, col))
                        if check_game_over(board):
                            print(f"Game over! {player_turn} wins!")
                            pygame.quit()
                            sys.exit()
                        selected_square = None
                        player_turn = 'b' if player_turn == 'w' else 'w'
                    else:
                        selected_square = None
                else:
                    if board[row][col] != '--' and board[row][col][0] == player_turn:
                        selected_square = (row, col)

        draw_board(screen, selected_square)
        draw_pieces(screen, board)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
