# Ping: our simple implementation of the pong game

import color
import pygame
import sys
import random

# initializing pygame and defining some global variables.
########################################################
pygame.init()

# dispalying windows:-
################
width = height = 600
win = pygame.display.set_mode((width, height))
# set a title to the windows
pygame.display.set_caption(" Ping")
# set an icon to the windows
icon_img = pygame.image.load("ball.png")
pygame.display.set_icon(icon_img)
################

# create clock object
clock = pygame.time.Clock()


# barrier :-
################
barrier_width = barrier_height = 150
barrier_x = width//2-barrier_width//2
barrier_y = height//2-barrier_height//2
barrier_collision_rect = pygame.Rect(barrier_x, barrier_y, barrier_width, barrier_height)
################

# ball:-
################
# load an image file for the ball with pygame
ball = pygame.image.load("ball.png").convert_alpha()
# because ball is a pygame surface we can use the get_
ball_width = ball.get_width()
ball_height = ball.get_height()
# Randomly choose a valid starting location for the ball
ball_x = random.randint(barrier_x+barrier_width+ball_width+10, width-ball_width-10)
ball_y = random.randint(10+ball_height, height-ball_height-10)
# Randomly choose a starting velocity for the ball
ball_dx = random.randint(width  // 3, width-150)  # ball_dx = delta x of the ball. It represents the velocity of the ball in the x-coordinate 
ball_dy = random.randint(height // 3, height-100) # ball_dy = delta y of the ball. It represents the velocity of the ball in the y-coordinate 
# define the collision rectangular for the ball
ball_collision_rect = pygame.Rect(ball_x, ball_y, ball_width, ball_height)
################

# Paddle:-
################
# load an image file for our paddle
paddle = pygame.image.load("paddle.png").convert_alpha()
paddle_width = paddle.get_width()
paddle_height = paddle.get_height()
# place our paddle 10 px from the left side and centered vertically
paddle_x = 10
paddle_y = height // 2 - paddle_height // 2
# set our initial velocity of the Paddle
paddle_dy = 0
paddle_collision_rect = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height) 
################

#Keep track of the user’s/player's score:
score = 0
best_score = 0
########################################################


def move_ball(x, y, dx, dy, dt):
    """
    Move a particle based off of a current location and velocity
    :param x: x-coordinate of the first point of the ball
    :param y: y-coordinate of the first point of the ball
    :param dx: delta-x of the velocity of the ball in the x-coordinate
    :param dy: delta-y of the velocity of the ball in the y-coordinate
    :param dt: (delta-time) the amount of time that has elapsed since the last call to move (seconds)
    :return: (x, y, dx, dy) tuple of the updated location and velocities
    """
    global ball_collision_rect, score

    # did we hit the side wall?
    if x <= 0:
        # hit the left hand side
        x = 0
        dx = -dx
    elif x + ball_width >= width:
        # hit the right hand side
        x = width - ball_width
        dx = -dx

    # check for top/bottom
    if y <= 0:
        # hit the top
        y = 0
        dy = -dy
    elif y + ball_height >= height:
        # hit the bottom
        y = height - ball_height
        dy = -dy
    
    # check for collision with the Paddle
    # resources: https://www.pygame.org/docs/ref/rect.html
    if paddle_collision_rect.colliderect(ball_collision_rect):
        if x > paddle_x + paddle_width//2:
            x = paddle_x + paddle_width
            dx *= -1
            score += 1
        else:
            restart()
    
    # check if player loses
    if x <= 0:
        restart()

    # check for collision with the barrier:
    if barrier_collision_rect.colliderect(ball_collision_rect):
        # Top side                      
        if y + ball_height >= barrier_y and y + ball_height <= barrier_y+ball_height//2:
            dy *= -1
            y = barrier_y-ball_height-3
        # Bottom side
        elif y <= barrier_y+barrier_height and y >= barrier_y+barrier_height - ball_height//2:
            dy *= -1
            y = barrier_y+barrier_height+3
        # Right side
        elif x <= barrier_x+barrier_width and x >= barrier_x+barrier_width - ball_width//2:
            dx *= -1
            x = barrier_x+barrier_width+3
        # Left side
        elif x + ball_width >= barrier_x and x + ball_width <= barrier_x+ball_width//2:
            dx *= -1
            x = barrier_x-ball_width-3

    # update our location based on the current coordinate and the distance moved
    x += dx * dt
    y += dy * dt

    # update the ball_collision_rect
    ball_collision_rect = pygame.Rect(x, y, ball_width, ball_height)    

    #return our updated location and velocity
    return (x, y, dx, dy)


def move_paddle(paddle_y, paddle_dy):
    global paddle_collision_rect
    #             moving the paddle up             #                 moving the paddle down
    if (paddle_dy < 0 and paddle_y+paddle_dy >= 0) or (paddle_dy > 0 and paddle_y+paddle_dy+paddle_height <= height):
        paddle_y += paddle_dy
    # update the paddle_collision_rect
    paddle_collision_rect  = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)
    return paddle_y


def start_game():
    # to access the some global variables
    global  ball_x, ball_y, ball_dx, ball_dy
    global  paddle_y, paddle_dy
    global score, best_score

    score = 0
    print("Random Starting Location = (" + str(ball_x) + ", " + str(ball_y) + ")")
    print("Random Starting Velocity: dx = " + str(ball_dx) + ", dy = " + str(ball_dy))

    # Animation loop forever. Unless the player/user loses or clicks on the close icon of the windows.    
    while True:
        # we specify the frame rate so that
        # pygame can pause our program if our animation is moving too quickly (i.e..
        # we're drawing too many frames per second)

        # set the background. (clear the screen)
        win.fill(color.white)
        
        # add barrier to the middle of the game board
        pygame.draw.rect(win, color.blue, barrier_collision_rect)

        # dt (delta-time) get the time that has elapsed since the last call to tick
        # (0r the creation of the clock).
        dt = clock.tick(60) / 1000 # this gives an answer in ms -> divide by 1000 to get seconds


        # move the ball and update our variables
        ball_x, ball_y, ball_dx, ball_dy = move_ball(ball_x, ball_y, ball_dx, ball_dy, dt)
        # check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    paddle_dy = 6
                elif event.key == pygame.K_UP:
                    paddle_dy = -6
                elif event.key == pygame.K_SPACE:
                    paddle_dy = 0
                elif event.key == pygame.K_q:
                    exit_game()
                elif event.key == pygame.K_r:
                    restart()  

            # moving the paddle with the mouse
            elif event.type == pygame.MOUSEMOTION:
                m_x, m_y = event.pos
                paddle_dy = 0

                paddle_y = m_y - paddle_height//2
                if paddle_y+paddle_height > height:
                    paddle_y = height - paddle_height
                elif paddle_y < 0:
                    paddle_y = 0

                

        # blit the ball on the screen (draw it)
        win.blit(ball,(ball_x, ball_y))
        # pygame.draw.rect(win, color.blue, (ball_x, ball_y, ball_width, ball_height))

        # move and blit the paddle (draw it) and update our variables.
        paddle_y = move_paddle(paddle_y, paddle_dy)
        win.blit(paddle, (paddle_x, paddle_y))
        # pygame.draw.rect(win, color.blue, (paddle_x, paddle_y, paddle_width, paddle_height))

        # draw some text inside the barrier
        # resources: https://www.pygame.org/docs/ref/font.html
        font = pygame.font.Font("freesansbold.ttf", 14)
        score_text = font.render("Score = " + str(score), True, color.white) 
        restart_text = font.render("press R: to restart", True, color.white) 
        exit_text = font.render("press Q: to exit", True, color.white) 
        stop_text1 = font.render("press space:", True, color.white) 
        stop_text2 = font.render("to stop paddle", True, color.white) 
        win.blit(score_text, (barrier_x+10, barrier_y+18))
        win.blit(restart_text, (barrier_x+10, barrier_y+18*3))
        win.blit(exit_text, (barrier_x+10, barrier_y+18*4))
        win.blit(stop_text1, (barrier_x+10, barrier_y+18*5))
        win.blit(stop_text2, (barrier_x+10, barrier_y+18*6))

        #if current score is higher than the best score, then update best score
        if score > best_score:
            best_score = score

        # update the screen
        pygame.display.update()


def restart():
    global ball_x, ball_y, ball_dx, ball_dy
    global paddle_y, paddle_dy
    global score

    # restart the place of the paddle
    paddle_y = height // 2 - paddle_height // 2
    paddle_dy = 0

    # restart the velocity and the place of the ball (random velocity and random velocity)
    ball_dx = random.randint(width  // 3, width-150)  # ball_dx = delta x of the ball. It represents the velocity of the ball in the x-coordinate 
    ball_dy = random.randint(height // 3, height-100) # ball_dy = delta y of the ball. It represents the velocity of the ball in the y-coordinate 
    # Randomly choose a valid starting location for the ball
    ball_x = random.randint(barrier_x+barrier_width+ball_width+10, width-ball_width-10)
    ball_y = random.randint(10+ball_height, height-ball_height-10)

    introduction_screen(score)


def introduction_screen(score = None):

    # to print the score on the console
    if score != None:
        print("Best Score = " + str(best_score))
        print("Current Score = " + str(score))

    while True:
        win.fill(color.white)
        if score is not None:
            # to draw/blit the text on the pygame windows
            font = pygame.font.Font("freesansbold.ttf", 24)
            current_score_text = font.render("Current Score = " + str(score), True, color.orange) 
            best_text = font.render("Best Score = " + str(best_score), True, color.orange) 
            win.blit(current_score_text, (width/2-current_score_text.get_width()/2, 150))
            win.blit(best_text, (width/2-best_text.get_width()/2, 180))


        font = pygame.font.Font("freesansbold.ttf", 24)
        introduction_text = font.render("Press any key to start the game or Q to exit.", True, color.orange)
        win.blit(introduction_text, (width/2-introduction_text.get_width()/2, height/2-introduction_text.get_height()/2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.KEYDOWN: 
                if event.key != pygame.K_q:
                    start_game()
                else:
                    exit_game()    

        pygame.display.update()

def exit_game():
    pygame.quit()
    sys.exit()

introduction_screen()
