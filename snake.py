# Name: Casey Meisenzahl
# Date: 5/11/15
# Program name: snake.py
# Description: The Game snake, as you move around and eat blocks you grow larger. 
#                  Try not to bite yourself or go out of bounds.

import os
import pickle
from random import randint, randrange
import tkinter as tk

class Snake:
    def __init__(self):
        ## settings
        self.WIDTH = 1000
        self.HEIGHT = 500
        self.BOREDER = 20
        self.background_color = 'lightblue'
        self.board_color = 'coral'
        self.prey_color = '#ffff33'
        self.font = 'Helvetica'
        # Milliseconds till refresh lower is harder
        self.speed = 80

        ## tk
        self.root = tk.Tk()
        self.frame = tk.Frame()
        self.frame.pack()
        self.canvas = tk.Canvas(self.frame,
                                width =self.WIDTH,
                                height=self.HEIGHT,
                                bg    =self.background_color)
        self.canvas.pack()

        self.draw_board()
        # the grid is a representation of all the 20 by 20 squares on the board
        self.grid = self.create_grid()

        # the snake is made of blocks
        # the first block in the list is the head and the last is the tail
        self.snake = []
        # the food is a single block
        self.food = None

        self.banner = None
        self.display_banner('SNAKE')
        self.instructions = None
        self.display_instructions()
        self.current_score = None
        self.display_current_score()
        self.top_scores = None
        self.display_top_scores()

        self.heading = 'Left'
        self.active_game = False
        self.queue = 0


        self.root.bind('<Key>',self.handel_keys)
        self.root.bind('<Return>',self.handel_return)
    

    ## set up
    def draw_board(self):
        '''Creates the board, this will be the inbounds part of the the game.'''
        self.canvas.create_rectangle(self.BOREDER,self.BOREDER,
                                     self.WIDTH-self.BOREDER,self.HEIGHT-self.BOREDER,
                                     fill=self.board_color,
                                     outline='')
    def create_grid(self):
        ''' a set of all the 20 by 20 squares on the board
        return: set:
        '''
        grid = set()
        for x in range(self.BOREDER,self.WIDTH-self.BOREDER,20):
            for y in range(self.BOREDER,self.HEIGHT-self.BOREDER,20):
                grid.add((x,y,x+20,y+20))
        return grid

    ## scoring file
    def get_top_scores(self):
        '''Gets the top scores saved by pickling 
        return: list: a list of the the top scores ordered from highest to lowest
        '''
        self.setup_top_scores_file()
        with open('top.dat','rb') as f:
            return pickle.load(f)

    def update_top_scores(self):
        scores = self.get_top_scores()
        current_score = (len(self.snake)-1)*10
        scores.append(current_score)
        scores.sort(reverse=True)
        with open('top.dat','wb') as f:
            pickle.dump(scores[:-1],f)

    def setup_top_scores_file(self):
        '''Creates a top.dat file if there is none in this path
            then sets the top scores to default of zero
        return: list: the top five scores
        '''
        if not os.path.exists('top.dat'):
            with open('top.dat','wb') as f:
                high_score = [0,0,0,0,0]
                pickle.dump(high_score,f)

    ## snake and food blocks
    def add_snake_block(self,x,y):
        c = '0123456789abcdef'
        color = '#{}ff'.format(c[randint(0,15)],)

        block_id = self.canvas.create_rectangle(x,y,x+20,y+20, fill=color,outline='')
        self.snake.append(block_id)

    def draw_food(self,x,y):
        return self.canvas.create_rectangle(x,y,x+20,y+20, fill=self.prey_color,outline='')

    def reset_snake(self):
        for i in self.snake:
            self.canvas.delete(i)
        self.snake = []
        self.add_snake_block(700,300)

    def reset_food(self):
        self.canvas.delete(self.food)
        self.food = self.draw_food(200,300)

    def move_food(self):
        free_squares = list(self.free_blocks())
        location = free_squares[randint(0,len(free_squares))]


        x = location[0]
        y = location[1]
        delta_x = x - self.canvas.coords(self.food)[0]
        delta_y = y - self.canvas.coords(self.food)[1]

        self.canvas.move(self.food, delta_x,delta_y)

    ## placement
    def free_blocks(self):
        ''' returns the locations of all the available squares on the board
        return: set: 
        '''
        snake_xy = set()
        for block in self.snake:
            snake_xy.add(tuple(self.canvas.coords(block)))
        # subtracting the subset snake_xy from the superset grid
        return self.grid - snake_xy

    ## handle input
    def handel_keys(self,event):
        '''Changes the direction of the snake except for going back on its self
        '''
        key = event.keysym
        if (key == 'w' or key == 'Up') and self.heading != 'Down':
            self.heading = 'Up'
        elif (key == 'a' or key == 'Left') and self.heading != 'Right':
            self.heading = 'Left'
        elif (key == 's' or key == 'Down') and self.heading != 'Up':
            self.heading = 'Down'
        elif (key == 'd' or key == 'Right') and self.heading != 'Left':
            self.heading = 'Right'
 
    def handel_return(self,event=None):
        ''' Starts the game if not started already'''
        if not self.active_game:
            self.active_game = True
            self.display_instructions()
            self.reset_snake()
            self.reset_food()
            self.heading = 'Left'

            self.start_count_down()
            # clearing the banner, instructions, and top scores
            self.claer_menu()
            self.start()

    def start_count_down(self):
        for i in range(3,0,-1):
            self.display_banner(str(i))
            self.canvas.update()
            self.canvas.after(1000)

    def claer_menu(self):
        self.canvas.itemconfig(self.banner,text='')
        self.canvas.itemconfig(self.instructions,text='')
        self.canvas.itemconfig(self.top_scores,text='')

    def move_body(self):
        # moves each block in the list to the location of the index in front of it except for the head
        if self.queue > 0:
            self.add_snake_block(self.canvas.coords(self.snake[-1])[0],self.canvas.coords(self.snake[-1])[1])
            self.queue -= 1

        new_snake = []
        for i in range(1,len(self.snake)):
            x = self.canvas.coords(self.snake[i-1])[0]
            y = self.canvas.coords(self.snake[i-1])[1]
            delta_x = x - self.canvas.coords(self.snake[i])[0]
            delta_y = y - self.canvas.coords(self.snake[i])[1]
            new_snake.append([delta_x,delta_y])

        for i in range(1,len(self.snake)): 
            self.canvas.move(self.snake[i],*new_snake[i-1])

    def move_head(self):
        move = {'Left':[-20,0],'Right':[20,0],'Up':[0,-20],'Down':[0,20]}
        self.canvas.move(self.snake[0],*move[self.heading])

    def display_current_score(self):
        score = (len(self.snake)-1)*10
        if self.current_score == None:
            self.current_score = self.canvas.create_text(self.WIDTH*4//5,
                                                self.HEIGHT-10,
                                                text='0',
                                                font=(self.font, 22))
        else:
            self.canvas.itemconfig(self.current_score,text=score)

    def display_banner(self,message):
        if self.banner == None:
            self.banner = self.canvas.create_text(self.WIDTH//2,
                                                self.HEIGHT//3,
                                                text=message,
                                                font=(self.font, 72, "bold"))
        else:
            self.canvas.itemconfig(self.banner,text=message)
        self.canvas.tag_raise(self.banner)

    def display_instructions(self):
        instructions ='Press Return to start\n\nW == Up\nA == Left\nS == Down\nD == Right'
        if self.instructions == None:
            self.instructions =self.canvas.create_text(self.WIDTH*4//5,
                                                self.HEIGHT//3,
                                                text=instructions,
                                                font=(self.font, 24))
        else:
            self.canvas.itemconfig(self.instructions,text=instructions)
        self.canvas.tag_raise(self.instructions)

    def display_top_scores(self):
        scores = self.get_top_scores()
        scoreboard = 'Top scores\n\n{}\n{}\n{}\n{}\n{}'.format(*scores)
        if self.top_scores == None:
            self.top_scores = self.canvas.create_text(self.WIDTH//5,
                                                self.HEIGHT//3,
                                                text=scoreboard,
                                                font=(self.font, 22))
        else:
            self.canvas.itemconfig(self.top_scores,text=scoreboard)
        self.canvas.tag_raise(self.top_scores)

    def inbounds(self):
        head_coords = tuple(self.canvas.coords(self.snake[0]))
        if head_coords in self.grid:
            return True
        return False

    def snake_bite(self):
        head_coords = self.canvas.coords(self.snake[0])
        for i in range(1,len(self.snake)):
            block = self.snake[i]
            block_coords = self.canvas.coords(block)
            if block_coords == head_coords:
                return True
        return False

    def caught_food(self):
        head_coords = self.canvas.coords(self.snake[0])
        food_coords = self.canvas.coords(self.food)
        if head_coords == food_coords:
            return True
        return False

    def start(self):
        while self.inbounds() and not self.snake_bite():
            speed = self.speed
            if self.caught_food():
                self.queue += 5
                self.move_food()
                speed -=3

            self.move_body()
            self.move_head()
            self.display_current_score()

            self.canvas.update()
            self.canvas.after(speed)


        self.display_banner('GAME\nOVER')
        self.display_instructions()
        self.update_top_scores()
        self.display_top_scores()

        self.active_game = False


if __name__ == '__main__':
    Snake()
    tk.mainloop()











