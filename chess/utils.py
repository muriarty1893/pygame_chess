# chess/utils.py

import pygame

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

def draw_button(screen, text, x, y, width, height):
    font = pygame.font.Font(None, 36)
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, (100, 100, 100), button_rect)
    button_text = font.render(text, True, (255, 255, 255))
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)
    return button_rect

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
