import pygame
import sys
import random
from  tkinter import *
pygame.init()


NB_COL = 25
NB_ROW = 15
CELL_SIZE = 40
LARG = NB_COL*CELL_SIZE
HAUT = NB_ROW*CELL_SIZE


window = Tk()
window.title("SNAKE GAME")
window.geometry("1000x600+175+54")
window.minsize(1000,600)
window.config(background='#00FFFF')
# creer la boite ou frame
frame = Frame(window,bg='#00FFFF')


def fonction_quitter_boutton():
    pygame.quit()
    sys.exit()

# creer le texte game over
label_game_over = Label(frame, text='Game Over',font=('Arial',40),bg='#00FFFF',fg='black')
label_game_over.pack()
# creer le text score
label_score = Label(frame, text='score:  ',font=('Arial',40),bg='#00FFFF',fg='black')

label_score.pack()
# Ajouter un boutton


quitt_boutton = Button(frame,text='Quitter',font=('Arial',40),bg='#CC99FF',fg='black',command=fonction_quitter_boutton)
quitt_boutton.pack()


frame.pack(expand=YES)



screen = pygame.display.set_mode((NB_COL*CELL_SIZE,NB_ROW*CELL_SIZE))
timer = pygame.time.Clock()

class Block:
    def __init__(self,pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y

class Food:
    def __init__(self):
        x = random.randint(0,NB_COL-1)
        y = random.randint(0,NB_ROW-1)
        self.block = Block(x,y)
    def draw_food(self):
        self.rect = pygame.Rect(self.block.x*CELL_SIZE,self.block.y*CELL_SIZE,CELL_SIZE,CELL_SIZE)
        pygame.draw.rect(screen,pygame.Color("red"),self.rect)

class Snake:
    def __init__(self):
        self.body = [Block(2,6),Block(3,6),Block(4,6)]
        self.direction = "RIGHT"

    def draw_snake(self):
        for block in self.body:
            self.rect = pygame.Rect(block.x*CELL_SIZE,block.y*CELL_SIZE,CELL_SIZE,CELL_SIZE)
            pygame.draw.rect(screen,pygame.Color("blue"),self.rect)
    def move_snake(self):
        snake_body_count = len(self.body)
        old_head = self.body[snake_body_count-1]
        if self.direction == "RIGHT":
            new_head = Block(old_head.x+1,old_head.y)
        elif self.direction == "LEFT":
            new_head = Block(old_head.x-1,old_head.y)
        elif self.direction == "DOWN":
            new_head = Block(old_head.x,old_head.y+1)
        elif self.direction == "TOP":
            new_head = Block(old_head.x,old_head.y-1)
        self.body.append(new_head)
    def reset_snake(self):
        self.body = [Block(2, 6), Block(3, 6), Block(4, 6)]
        self.direction = "RIGHT"


class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.generate_food()
        self.score = 0

    def update(self):
        self.snake.move_snake()
        self.check_snake_on_food()
        self.game_over()
    def draw_game_element(self):
        self.snake.draw_snake()
        self.food.draw_food()
    def check_snake_on_food(self):
        snake_lenght = len(self.snake.body)
        snake_head_block = self.snake.body[snake_lenght-1]
        food_block = self.food.block
        if snake_head_block.x == food_block.x and snake_head_block.y == food_block.y:
            self.generate_food()
        else:
            self.snake.body.pop(0)
    def generate_food(self):
        would_generate_food = True
        while would_generate_food:
            count = 0
            for block in self.snake.body:
                if block.x == self.food.block.x and block.y == self.food.block.y:
                    count+=1
            if count == 0:
                would_generate_food = False
            else:
                self.food = Food()
    def game_over(self):
        self.score = 0
        snake_lenght = len(self.snake.body)
        snake_head_block = self.snake.body[snake_lenght-1]
        if (snake_head_block.x not  in range(0,NB_COL)) or (snake_head_block.y not  in range(0,NB_ROW)) :
            self.score= len(self.snake.body) - 3
            label_score['text'] = label_score['text'] + str(self.score)


            window.mainloop()
            print("SCORE: {} ".format(self.score))

        for block in self.snake.body[0: snake_lenght - 1]:
            if block.x == snake_head_block.x and block.y == snake_head_block.y:
                self.score= len(self.snake.body)-3
                label_score['text'] = label_score['text'] + str(self.score)
                window.mainloop()
                print("SCORE: {}".format(self.score))
                self.snake.reset_snake()



def draw_grid():
    for i in range(0,NB_COL):
        for j in range(0,NB_ROW):
            rect = pygame.Rect(i*CELL_SIZE,j*CELL_SIZE,CELL_SIZE,CELL_SIZE)
            pygame.draw.rect(screen,pygame.Color("black"),rect,width=1)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,200)

food = Food()
snake = Snake()
game = Game()

def main_menu():
    running = True
    pause = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pause = False
                if event.key == pygame.K_RIGHT:
                    if game.snake.direction != "LEFT":
                        game.snake.direction = "RIGHT"
                if event.key == pygame.K_LEFT:
                    if game.snake.direction != "RIGHT":
                        game.snake.direction = "LEFT"
                if event.key == pygame.K_DOWN:
                    if game.snake.direction != "TOP":
                        game.snake.direction = "DOWN"
                if event.key == pygame.K_UP:
                    if game.snake.direction != "DOWN":
                        game.snake.direction = "TOP"

        screen.fill(pygame.Color("#99FFCC"))
        # draw_grid()
        game.draw_game_element()
        pygame.display.update()
        timer.tick(60)
        

main_menu()


