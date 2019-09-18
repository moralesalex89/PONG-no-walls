# Bring rubric to class and piece of paper rubric filled out github link upload code to github
# Quiz on Wed
#file:///C:/Users/moral/Downloads/project1_PONG-no-walls.pdf
#file:///C:/Users/moral/Downloads/inventyourowncomputergameswithpython%20(3).pdf
import pygame, sys, time, random, math
from pygame.locals import *

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
mainClock = pygame.time.Clock()

WINDOWWIDTH = 700
WINDOWHEIGHT = 500

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BORDERSIZE = 50
PAD_LEN = 128
PAD_WID = 20
BALL_RAD = 7

BALL_MOVESPEED = 6
PADDLE_MOVESPEED = 4
SPAWN_DELAY = 20

GAMES = 3
POINTS = 11

windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('PONG+')


class ImgRect:
    def __init__(self, img_str, x_pos, y_pos, len, wid):
        self.rect_ = pygame.Rect(x_pos, y_pos, len, wid)
        self.img_ = pygame.image.load(img_str)
        self.scale_ = pygame.transform.scale(self.img_, (len, wid))

    def grid(self, surface):
        surface.blit(self.scale_, self.rect_)

    def move_x(self, dx):
        self.rect_.left += dx

    def move_y(self, dy):
        self.rect_.top += dy

    def move(self, x, y):
        self.rect_.top = y
        self.rect_.left = x

    def colliderect(self, rect):
        return self.rect_.colliderect(rect)

    # checks if a rect is completely inside another rect
    def collide_in(self, rect):
        return (self.rect_.left >= rect.left) and (self.rect_.right <= rect.right) and (self.rect_.top >= rect.top) and (self.rect_.bottom <= rect.bottom)

    def collide_in_x(self, rect):
        return self.rect_.left >= rect.left and self.rect_.right <= rect.right

    def collide_in_y(self, rect):
        return self.rect_.top >= rect.top and self.rect_.bottom <= rect.bottom

    def get_rect(self):
        return self.rect_

    def get_img(self):
        return self.img_


class TextRect:
    def __init__(self, text, font_size=40, x_pos=0, y_pos=0, text_color=WHITE):
        self.font_ = pygame.font.SysFont(None, font_size)
        self.text_ = text
        self.color_ = text_color
        self.display_ = self.font_.render(text, True, self.color_)
        self.rect_ = self.display_.get_rect()
        self.rect_.left = x_pos
        self.rect_.top = y_pos

    def edit_text(self, text):
        self.text_ = text
        self.display_ = self.font_.render(text, True, self.color_)

    def get_rect(self):
        return self.rect_

    def grid(self, surface):
        surface.blit(self.display_, self.rect_)


p1_score, p2_score, p1_game, p2_game = 0, 0, 0, 0
p1_score_rect = TextRect('Score: %d   Games: %d   ' % (p1_score, p1_game))
p2_score_rect = TextRect('Score: %d   Games: %d   ' % (p2_score, p2_game))
p1_score_rect.get_rect().bottom = WINDOWHEIGHT
p2_score_rect.get_rect().right = WINDOWWIDTH
p2_score_rect.get_rect().bottom = WINDOWHEIGHT

win_rect = TextRect('YOU WIN!', 100, 0, 0, WHITE)
lose_rect = TextRect('YOU LOSE!', 100, 0, 0, WHITE)
win_rect.get_rect().left, win_rect.get_rect().top, lose_rect.get_rect().left, lose_rect.get_rect().top = (WINDOWWIDTH - (win_rect.get_rect().right - win_rect.get_rect().left)) / 2, (WINDOWHEIGHT - (win_rect.get_rect().bottom - win_rect.get_rect().top)) / 2, (WINDOWWIDTH - (lose_rect.get_rect().right - lose_rect.get_rect().left)) / 2, (WINDOWHEIGHT - (lose_rect.get_rect().bottom - lose_rect.get_rect().top)) / 2
replay_msg = TextRect('[Enter] - Replay', 20)
replay_msg.get_rect().left, replay_msg.get_rect().top = (WINDOWWIDTH - replay_msg.get_rect().right - replay_msg.get_rect().left) / 2, win_rect.get_rect().bottom

background = ImgRect('images/play_area.png', 0, 0, WINDOWWIDTH, WINDOWHEIGHT)
p1_area = pygame.Rect(BORDERSIZE, BORDERSIZE, (WINDOWWIDTH - 2 * BORDERSIZE) / 2, WINDOWHEIGHT - 2 * BORDERSIZE)
p2_area = pygame.Rect(BORDERSIZE + (WINDOWWIDTH - 2 * BORDERSIZE) / 2, BORDERSIZE, (WINDOWWIDTH - 2 * BORDERSIZE) / 2, WINDOWHEIGHT - 2 * BORDERSIZE)

# player's paddles
p1_pad_a = ImgRect('images/p1_pad_a.png', BORDERSIZE - PAD_WID + 1, WINDOWHEIGHT / 2 - PAD_LEN / 2, PAD_WID, PAD_LEN)
p1_pad_b = ImgRect('images/p1_pad_b.png', ((WINDOWWIDTH / 2 - BORDERSIZE) / 2) + BORDERSIZE - PAD_LEN / 2, BORDERSIZE - PAD_WID + 1, PAD_LEN, PAD_WID)
p1_pad_c = ImgRect('images/p1_pad_b.png', ((WINDOWWIDTH / 2 - BORDERSIZE) / 2) + BORDERSIZE - PAD_LEN / 2, WINDOWHEIGHT - BORDERSIZE, PAD_LEN, PAD_WID)

# CPU's paddles
p2_pad_a = ImgRect('images/p2_pad_a.png', WINDOWWIDTH - BORDERSIZE, WINDOWHEIGHT / 2 - PAD_LEN / 2, PAD_WID, PAD_LEN)
p2_pad_b = ImgRect('images/p2_pad_b.png', WINDOWWIDTH - ((WINDOWWIDTH / 2 - BORDERSIZE) / 2) + BORDERSIZE - PAD_LEN / 2, BORDERSIZE - PAD_WID + 1, PAD_LEN, PAD_WID)
p2_pad_c = ImgRect('images/p2_pad_b.png', WINDOWWIDTH - ((WINDOWWIDTH / 2 - BORDERSIZE) / 2) + BORDERSIZE - PAD_LEN / 2, WINDOWHEIGHT - BORDERSIZE, PAD_LEN, PAD_WID)

# sound effects
win_sound = pygame.mixer.Sound('sounds/win_sound.wav')
lose_sound = pygame.mixer.Sound('sounds/lose_sound.wav')
bounce_sound = pygame.mixer.Sound('sounds/bounce_sound.wav')
score_sound = pygame.mixer.Sound('sounds/score_sound.wav')
spawn_sound = pygame.mixer.Sound('sounds/spawn_sound.wav')
game_win_sound = pygame.mixer.Sound('sounds/game_win_sound.wav')
game_lose_sound = pygame.mixer.Sound('sounds/game_lose_sound.wav')

# ball and its boundary
ball = ImgRect('images/ball.png', WINDOWWIDTH / 2 - BALL_RAD, WINDOWHEIGHT / 2 - BALL_RAD, 2 * BALL_RAD, 2 * BALL_RAD)
ball_boundary = pygame.Rect(BORDERSIZE - BALL_RAD, BORDERSIZE - BALL_RAD, WINDOWWIDTH - (2 * BORDERSIZE) + 2 * BALL_RAD, WINDOWHEIGHT - (2 * BORDERSIZE) + 2 * BALL_RAD)

def spawn_ball(move_speed):
    # chooses a random angle between 25 and 65 degrees, angles restricted to keep all paddles relevant
    angle = random.randint(25, 65)
    # chooses a random speed within range of the default speed
    start_speed = random.randint(move_speed-1, move_speed+1)
    # uses the speed to calculate velocity in the x and y directions
    vel_x = start_speed * math.cos(math.radians(angle))
    vel_y = start_speed * math.sin(math.radians(angle))
    # chooses a random direction for x and y
    dir_x = random.choice([-1, 1])
    dir_y = random.choice([-1, 1])
    return dir_x * vel_x, dir_y * vel_y


def inc_ball_speed(vel_x, vel_y):
    # increases the ball speed
    vel_x = vel_x * 1.05
    vel_y = vel_y * 1.05
    return vel_x, vel_y


p1_U, p1_D, p1_L, p1_R, p2_U, p2_D, p2_L, p2_R = False, False, False, False, False, False, False, False
ball_vx, ball_vy = spawn_ball(BALL_MOVESPEED)
ball_pause = SPAWN_DELAY
reset = True
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # if any player has reached the winning number of games show appropriate screen
    if p1_game == GAMES or p2_game == GAMES:
        if reset:
            windowSurface.fill(BLACK)
            if p1_game == GAMES:
                win_rect.grid(windowSurface)
                win_sound.play()
            elif p2_game == GAMES:
                lose_rect.grid(windowSurface)
                lose_sound.play()
            replay_msg.grid(windowSurface)

        reset = False

        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                p1_score, p2_score, p1_game, p2_game = 0, 0, 0, 0
                reset = True

        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()


    # if no player has won continue the game as normal
    else:
        if ball_pause > 0:
            ball_pause -= 1
            if ball_pause == 0:
                spawn_sound.play()
        else:
            # if the ball is still in bounds check for paddle collision
            if ball.collide_in(ball_boundary):
                if ball.colliderect(p1_pad_a.get_rect()) or ball.colliderect(p2_pad_a.get_rect()):
                    if ball.colliderect(p1_pad_a.get_rect()):
                        ball.get_rect().left = p1_pad_a.get_rect().right
                    else:
                        ball.get_rect().right = p2_pad_a.get_rect().left
                    ball_vx, ball_vy = inc_ball_speed(ball_vx, ball_vy)
                    ball_vx = -1 * ball_vx
                    bounce_sound.play()

                if ball.colliderect(p1_pad_b.get_rect()) or ball.colliderect(p1_pad_c.get_rect()) or ball.colliderect(p2_pad_b.get_rect()) or ball.colliderect(p2_pad_c.get_rect()):
                    if ball.colliderect(p1_pad_b.get_rect()) or ball.colliderect(p2_pad_b.get_rect()):
                        ball.get_rect().top = p1_pad_b.get_rect().bottom
                    else:
                        ball.get_rect().bottom = p1_pad_c.get_rect().top
                    ball_vx, ball_vy = inc_ball_speed(ball_vx, ball_vy)
                    ball_vy = -1 * ball_vy
                    bounce_sound.play()

            # if the ball is out of bounds check who scored and update score
            else:
                if ball.get_rect().centerx < WINDOWWIDTH / 2:
                    p2_score += 1
                    if p2_score >= POINTS and abs(p2_score - 2) >= p1_score:
                        p2_score = 0
                        p1_score = 0
                        p2_game += 1
                        if p2_game < GAMES:
                            game_lose_sound.play()
                    else:
                        score_sound.play()
                    p2_score_rect.edit_text('Score: %d   Games: %d  ' % (p2_score, p2_game))
                else:
                    p1_score += 1
                    if p1_score >= POINTS and abs(p1_score - 2) >= p2_score:
                        p1_score = 0
                        p2_score = 0
                        p1_game += 1
                        if p1_game < GAMES:
                            game_win_sound.play()
                    else:
                        score_sound.play()
                    p1_score_rect.edit_text('Score: %d   Games: %d  ' % (p1_score, p1_game))
                ball.get_rect().centerx = WINDOWWIDTH / 2
                ball.get_rect().centery = WINDOWHEIGHT / 2
                ball_vx, ball_vy = spawn_ball(BALL_MOVESPEED)
                ball_pause = SPAWN_DELAY
            if ball_pause == 0:
                ball.move_x(ball_vx)
                ball.move_y(ball_vy)

        # key check for player's paddle
        if event.type == KEYDOWN:
            if event.key == K_w or event.key == K_UP:
                p1_D, p1_U = False, True
            if event.key == K_s or event.key == K_DOWN:
                p1_U, p1_D = False, True
            if event.key == K_a or event.key == K_LEFT:
                p1_R, p1_L = False, True
            if event.key == K_d or event.key == K_RIGHT:
                p1_L, p1_R = False, True

        # key release check
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_w or event.key == K_UP:
                p1_U = False
            if event.key == K_s or event.key == K_DOWN:
                p1_D = False
            if event.key == K_a or event.key == K_LEFT:
                p1_L = False
            if event.key == K_d or event.key == K_RIGHT:
                p1_R = False

        # depending on key press and check if paddle is completely in area bound, move the paddle
        if p1_U:
            p1_pad_a.move_y(-PADDLE_MOVESPEED)
            if not p1_pad_a.collide_in_y(p1_area):
                p1_pad_a.get_rect().top = p1_area.top
        if p1_D:
            p1_pad_a.move_y(PADDLE_MOVESPEED)
            if not p1_pad_a.collide_in_y(p1_area):
                p1_pad_a.get_rect().bottom = p1_area.bottom
        if p1_L:
            p1_pad_b.move_x(-PADDLE_MOVESPEED)
            if not p1_pad_b.collide_in_x(p1_area):
                p1_pad_b.get_rect().left = p1_area.left
            p1_pad_c.get_rect().left = p1_pad_b.get_rect().left
        if p1_R:
            p1_pad_b.move_x(PADDLE_MOVESPEED)
            if not p1_pad_b.collide_in_x(p1_area):
                p1_pad_b.get_rect().right = p1_area.right
            p1_pad_c.get_rect().left = p1_pad_b.get_rect().left

        # CPU Movement attempts to always choose direction to match the paddle's and ball's center
        p2_U, p2_D, p2_L, p2_R = False, False, False, False
        if ball.get_rect().centery < p2_pad_a.get_rect().centery:
            p2_D, p2_U = False, True
        if ball.get_rect().centery > p2_pad_a.get_rect().centery:
            p2_U, p2_D = False, True
        if ball.get_rect().centerx > p2_pad_b.get_rect().centerx:
            p2_L, p2_R= False, True
        if ball.get_rect().centerx < p2_pad_b.get_rect().centerx:
            p2_R, p2_L = False, True

        # CPU paddle movement follows same rules as player
        if p2_U:
            p2_pad_a.move_y(-PADDLE_MOVESPEED)
            if not p2_pad_a.collide_in_y(p2_area):
                p2_pad_a.get_rect().top = p2_area.top
        if p2_D:
            p2_pad_a.move_y(PADDLE_MOVESPEED)
            if not p2_pad_a.collide_in_y(p2_area):
                p2_pad_a.get_rect().bottom = p2_area.bottom
        if p2_L:
            p2_pad_b.move_x(-PADDLE_MOVESPEED)
            if not p2_pad_b.collide_in_x(p2_area):
                p2_pad_b.get_rect().left = p2_area.left
            p2_pad_c.get_rect().left = p2_pad_b.get_rect().left
        if p2_R:
            p2_pad_b.move_x(PADDLE_MOVESPEED)
            if not p2_pad_b.collide_in_x(p2_area):
                p2_pad_b.get_rect().right = p2_area.right
            p2_pad_c.get_rect().left = p2_pad_b.get_rect().left

        # passes window surface to ImgRect/TextRect function that blits the image for display
        background.grid(windowSurface)
        ball.grid(windowSurface)
        p1_pad_a.grid(windowSurface)
        p1_pad_b.grid(windowSurface)
        p1_pad_c.grid(windowSurface)
        p2_pad_a.grid(windowSurface)
        p2_pad_b.grid(windowSurface)
        p2_pad_c.grid(windowSurface)
        p1_score_rect.grid(windowSurface)
        p2_score_rect.grid(windowSurface)

    pygame.display.update()
    mainClock.tick(40)