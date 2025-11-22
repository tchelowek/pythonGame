import pygame
from random import uniform as func

pygame.init()
WIDTH, HEIGHT = 400, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")

clock = pygame.time.Clock()

# constants
bound = 5
c2s = 30
white = (255, 255, 255)
black = (0, 0, 0)
color = (0, 255, 0)  # green ball

# ball
x, y = WIDTH // 2, HEIGHT // 2
radius = 10
velocity = 8
vx = velocity * func(-1, 1)
vy = velocity * func(-1, 1)

# borders (only 3 walls, no bottom)
border_l = radius + bound
border_r = WIDTH - radius - bound
border_u = radius + bound
border_d = HEIGHT  # for losing

# platform
height = 10
width = 80
xp = (WIDTH - width) // 2
yp = HEIGHT - height - bound
vp = 10

# speed increase factor
num = 1.5

# ----- SCORE -----
score = 0
pygame.font.init()
font = pygame.font.SysFont("Arial", 32, True)


def drawWindow():
    win.fill(black)
    # рамка
    pygame.draw.rect(win, white, (0, 0, WIDTH, bound))              # up
    pygame.draw.rect(win, white, (0, 0, bound, HEIGHT))             # left
    pygame.draw.rect(win, white, (WIDTH - bound, 0, bound, HEIGHT)) # right
    # м'яч
    pygame.draw.circle(win, color, (int(x), int(y)), radius)
    # платформа
    pygame.draw.rect(win, white, (xp, yp, width, height))
    pygame.display.update()


def drawScore(final_score: int):
    """Показати фінальний рахунок після закінчення гри."""
    win.fill(black)
    text = font.render(f"Your score: {final_score}", True, white)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    win.blit(text, text_rect)
    pygame.display.update()


run = True
while run:
    clock.tick(c2s)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # move platform
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and xp > bound:
        xp -= vp
    if keys[pygame.K_RIGHT] and xp < WIDTH - bound - width:
        xp += vp

    # reflect from side walls
    if x + vx < border_l or x + vx > border_r:
        vx = -vx

    # reflect from top
    if y + vy < border_u:
        vy = -vy

    # check bottom (lose)
    if y + vy > border_d:
        run = False
    else:
        # check platform hit (м'яч летить донизу і досягає рівня платформи)
        if y + vy + radius >= yp and vy > 0:
            # перевіряємо, чи м'яч над платформою
            if xp <= x + vx <= xp + width:
                vy = -vy
                vx *= num
                vy *= num
                score += 1          # ← додаємо очко за відбиття
            else:
                run = False

    # move ball
    x += vx
    y += vy

    drawWindow()

# після виходу з гри показуємо фінальний рахунок
drawScore(score)

# чекаємо, поки користувач закриє вікно
end_screen = True
while end_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_screen = False

pygame.quit()
