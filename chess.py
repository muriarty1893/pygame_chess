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
SELECTED_COLOR = (100, 100, 255)
MOVE_COLOR = (0, 255, 0)

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

def draw_board(screen, selected_square=None, possible_moves=[]):
    colors = [WHITE, BLACK]
    for row in range(ROWS):
        for col in range(COLS):
            color = colors[(row + col) % 2]
            if selected_square and (row, col) == selected_square:
                color = SELECTED_COLOR
            elif (row, col) in possible_moves:
                color = MOVE_COLOR
            pygame.draw.rect(screen, color, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(screen, board):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != '--':
                screen.blit(PIECES[piece], (col*SQUARE_SIZE, row*SQUARE_SIZE))

def is_path_clear(board, start_pos, end_pos):
    direction = (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
    step_row = 0 if direction[0] == 0 else direction[0] // abs(direction[0])
    step_col = 0 if direction[1] == 0 else direction[1] // abs(direction[1])
    
    current_pos = (start_pos[0] + step_row, start_pos[1] + step_col)
    while current_pos != end_pos:
        if board[current_pos[0]][current_pos[1]] != '--':
            return False
        current_pos = (current_pos[0] + step_row, current_pos[1] + step_col)
    return True

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
        if (direction[0] == 0 or direction[1] == 0) and is_path_clear(board, start_pos, end_pos):
            return True
    elif piece[1] == 'N':  # Knight
        if abs(direction[0] * direction[1]) == 2:
            return True
    elif piece[1] == 'B':  # Bishop
        if abs(direction[0]) == abs(direction[1]) and is_path_clear(board, start_pos, end_pos):
            return True
    elif piece[1] == 'Q':  # Queen
        if (direction[0] == 0 or direction[1] == 0 or abs(direction[0]) == abs(direction[1])) and is_path_clear(board, start_pos, end_pos):
            return True
    elif piece[1] == 'K':  # King
        if max(abs(direction[0]), abs(direction[1])) == 1:
            return True
    return False

def get_possible_moves(board, start_pos):
    possible_moves = []
    for row in range(ROWS):
        for col in range(COLS):
            if is_valid_move(board, start_pos, (row, col)):
                possible_moves.append((row, col))
    return possible_moves

def move_piece(board, start_pos, end_pos):
    piece = board[start_pos[0]][start_pos[1]]
    board[start_pos[0]][start_pos[1]] = '--'
    board[end_pos[0]][end_pos[1]] = piece

def check_game_over(board):
    kings = [piece for row in board for piece in row if piece[1] == 'K']
    return len(kings) < 2

def is_in_check(board, player):
    king_pos = None
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == f'{player}K':
                king_pos = (row, col)
                break
        if king_pos:
            break

    opponent = 'b' if player == 'w' else 'w'
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col].startswith(opponent):
                if is_valid_move(board, (row, col), king_pos):
                    return True
    return False

def show_check_alert(player):
    pygame.display.set_caption(f"Check! {player} King is in danger!")
    check_alert = pygame.Surface((200, 100))
    check_alert.fill((255, 0, 0))
    font = pygame.font.Font(None, 36)
    text = font.render(f"{player} King is in check!", True, (255, 255, 255))
    check_alert.blit(text, (10, 30))
    screen.blit(check_alert, (WIDTH//2 - 100, HEIGHT//2 - 50))
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.display.set_caption('Chess')

def show_invalid_move_alert():
    pygame.display.set_caption("Invalid Move!")
    alert = pygame.Surface((200, 100))
    alert.fill((255, 0, 0))
    font = pygame.font.Font(None, 36)
    text = font.render("Invalid Move!", True, (255, 255, 255))
    alert.blit(text, (10, 30))
    screen.blit(alert, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
    pygame.display.update()
    pygame.time.delay(1000)
    pygame.display.set_caption('Chess')

def draw_button(screen, text, x, y, width, height):
    font = pygame.font.Font(None, 36)
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, (100, 100, 100), button_rect)
    button_text = font.render(text, True, (255, 255, 255))
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)
    return button_rect

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
    
    move_history = []
    selected_square = None
    possible_moves = []
    player_turn = 'w'  # 'w' for white's turn, 'b' for black's turn

    def undo_last_move():
        if move_history:
            last_move = move_history.pop()
            move_piece(board, last_move[1], last_move[0])  # Undo the move
            return last_move[2]  # Return the player turn before the last move

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if undo_button.collidepoint(pos):
                    player_turn = undo_last_move()
                else:
                    row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE
                    if selected_square:
                        if is_valid_move(board, selected_square, (row, col)):
                            move_history.append((selected_square, (row, col), player_turn))
                            move_piece(board, selected_square, (row, col))
                            if check_game_over(board):
                                print(f"Game over! {player_turn} wins!")
                                pygame.quit()
                                sys.exit()
                            if is_in_check(board, 'b'):
                                show_check_alert('Black')
                            if is_in_check(board, 'w'):
                                show_check_alert('White')
                            selected_square = None
                            possible_moves = []
                            player_turn = 'b' if player_turn == 'w' else 'w'
                        else:
                            show_invalid_move_alert()
                            selected_square = None
                            possible_moves = []
                    else:
                        if board[row][col] != '--' and board[row][col][0] == player_turn:
                            selected_square = (row, col)
                            possible_moves = get_possible_moves(board, selected_square)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:  # Press 'u' to undo the last move
                    player_turn = undo_last_move()

        draw_board(screen, selected_square, possible_moves)
        draw_pieces(screen, board)
        undo_button = draw_button(screen, 'Undo', WIDTH - 100, HEIGHT - 50, 80, 40)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
