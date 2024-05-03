import time 
import pygame 
import math 

WIDTH, HEIGHT = 1000, 650
SCREEN_WIDTH, SCREEN_HEIGHT = 4000, 2000

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.font.init()
SCALE_PIXEL = 5

font = pygame.font.SysFont("comicsans", 50)
STRENG_BAR = pygame.transform.scale(
    pygame.image.load("C:\\Users\\PC\\Documents\\strength.png"), (300, 500))

background = pygame.transform.scale(
    pygame.image.load("C:\\Users\\PC\\Documents\\earth.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))

class Ball:
    GRAVITY = 9.807
    def __init__(self, start_x, start_y, color):
        self.start_x = start_x
        self.start_y = start_y
        
        self.x = start_x
        self.y = start_y 

        self.color = color
        self.radius = 10
        self.angle = None 
        self.start_speed = 0 
        self.state = "on_ground"
        self.time = 0 

    def draw_ball(self, screen):
        pygame.draw.circle(screen, self.color, (self.x,  SCREEN_HEIGHT - (HEIGHT - self.y)), self.radius) 


    def move_ball(self, start_time):
        self.time = (time.time() - start_time) * 2
        self.x = self.start_x + ((self.start_speed*math.cos(self.angle))*self.time) 
        self.y = self.start_y - (((self.start_speed*math.sin(self.angle))*self.time - (self.GRAVITY*self.time**2)/2))

        if self.y >= self.start_y:
            self.state = "on_ground"
            time.sleep(1)
            self.y = self.start_y
            self.x = self.start_x
            self.angle = None 
            self.time = 0
            self.start_speed = 0 

def calculate_angle(ball, mouse):
    dis_x = mouse[0] - ball.x
    dis_y = ball.y - mouse[1]

    if dis_x > 0:
        angle = math.atan(dis_y/dis_x)
    else:
        angle = math.radians(90) 

    return angle

def draw_speed_bar(win, ball):
    if ball.angle:

        win.blit(STRENG_BAR, (-100, 50))
        pygame.draw.rect(win, "white", (10, 110, 30, 397), 5)

        if ball.start_speed:
            win.blit(STRENG_BAR, (-100, 50))
            length = (ball.start_speed - 50)// (130 / 386)
            pygame.draw.rect(win, "black", (15, 115, 20, 386 - length))


    font = pygame.font.SysFont("comicsans", 25)
    text = font.render("180m/s", False, "white")
    win.blit(text, (0, 115 - text.get_height() - 10))
    # win.blit(text, (0, 0))
    text = font.render("50m/s", False, "white")
    win.blit(text, (0, 510))


def draw_how_far_ball_go(screen, ball):
    font = pygame.font.SysFont("comicsans", 40)
    if (ball.x - ball.start_x) % 200 <= 100 and ball.state == "flying" and (ball.x - ball.start_x) // 200 >0:
        x = ((ball.x - ball.start_x) // 200) * 200
        text = font.render(f"{x}m->", False, "white")

        screen.blit(text, (x + 100, SCREEN_HEIGHT - (HEIGHT - ball.y)))


    if ball.state == "flying" and ball.time <= (ball.start_speed*ball.angle) / 9.807:
        if (ball.start_y - ball.y) % 100 <= 50 and (ball.start_y - ball.y) //100 >0:
            y = ((ball.start_y - ball.y) // 100) * 100
            text = font.render(f"{y}m up", False, "white")

            screen.blit(text, (ball.x - text.get_width() / 2,
               SCREEN_HEIGHT - (HEIGHT - ball.y + 100) ))



def draw_window(win, ball, screen):
    win.fill((0, 0, 0)) 
    draw_on_screen(ball, screen)
    if ball.x <= WIDTH // 2:
        if ball.y >= HEIGHT // 4:
            win.blit(screen, (0, - SCREEN_HEIGHT + HEIGHT))
        else:
            win.blit(screen, (0, - SCREEN_HEIGHT + HEIGHT + (HEIGHT//4 - ball.y)))
    

    else:
        if ball.y >= HEIGHT // 4:
            win.blit(screen, (WIDTH / 2 - ball.x - ball.radius, - SCREEN_HEIGHT + HEIGHT))
        else:
            win.blit(screen, (WIDTH / 2 - ball.x - ball.radius, - SCREEN_HEIGHT + HEIGHT + (HEIGHT//4 - ball.y)))


    draw_speed_bar(win, ball)
    pygame.draw.rect(win, 'white', (100, 100, 00, 100))

    pygame.draw.rect(win, "white", (10, 110, 30, 397), 5)
    font = pygame.font.SysFont("comicsans", 30)

    text_x = font.render(f"Distance: {round(ball.x - ball.start_x, 2)}m", True, "white")
    text_y = font.render(f"Height: {round(ball.start_y - ball.y, 2)}m", True, "white")

    win.blit(text_x, (WIDTH - text_x.get_width() - 10, 50))
    win.blit(text_y, (WIDTH - text_y.get_width() - 10, 100))


def draw_on_screen(ball, screen):
    screen.fill("black")
    screen.blit(background, (0, 0))
    pygame.draw.line(screen, "yellow", 
        (0, SCREEN_HEIGHT - (HEIGHT - ball.start_y - ball.radius)), 
        (SCREEN_WIDTH, SCREEN_HEIGHT - (HEIGHT - ball.start_y - ball.radius)), 5)

    ball.draw_ball(screen)
    draw_how_far_ball_go(screen, ball)
    

 
def main(win):
    screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    run = True 
    ball = Ball(100, 600, "white")

    mouse_type = None 


    while run:

        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if ball.state == "on_ground":
                    if x > 100 and y < 600:
                        mouse_type = "set_ball"

                    elif 14 < x < 38 and 115 <= y <= 501:
                        if ball.angle:
                            mouse_type = "set_speed"

            if event.type == pygame.MOUSEBUTTONUP: 

                if mouse_type == "set_speed":
                    if y >= 510:
                        ball.start_speed = 50
                    elif y <= 115:
                        ball.start_speed = 180 
                    else:
                        ball.start_speed = (501 - y) * (130 / 386) + 50
                    ball.state = "flying"
                    start_time = time.time()

                mouse_type = None


            if pygame.mouse.get_pressed()[0]:
                if mouse_type == "set_ball":
                    ball.angle = calculate_angle(ball, (x, y))


        draw_window(win, ball, screen)

        if ball.angle:

            if ball.state == "on_ground":
                radius = 200
                dis_y = radius * math.sin(ball.angle)
                dis_x = radius * math.cos(ball.angle)

                pygame.draw.line(win, "yellow", (ball.x, ball.y), (ball.x + dis_x, ball.y - dis_y), 5)

            if mouse_type == "set_speed":
                if y < 115:
                    pass
                elif y > 501:
                    pygame.draw.rect(win, "black", ((15, 115, 20, 386)))
                else:
                    pygame.draw.rect(win, "black", ((15, 115, 20, y - 115)))

        if ball.state == "flying":
            ball.move_ball(start_time)

        pygame.display.update()

    pygame.quit()


main(win)