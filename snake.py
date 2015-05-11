import os
import pickle
import random
import tkinter as tk

class Snake:
    def __init__(self):
        ## settings
        self.WIDTH = 1000
        self.HEIGHT = 500
        self.BOREDER = 20
        self.background_color = 'lightblue'
        self.board_color = 'coral'
        self.snake_color = '#3333ff'
        self.prey_color = '#ffff33'

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

        self.banner = self.draw_banner()
        self.instructions = self.draw_instructions()
        self.current_score = self.draw_current_score()
        self.top_scores = self.draw_top_scores()


    
    def draw_board(self):
        '''Creates the board, this will be the inbounds part of the the game.'''
        self.canvas.create_rectangle(self.BOREDER,self.BOREDER,
                                     self.WIDTH-self.BOREDER,self.HEIGHT-self.BOREDER,
                                     fill=self.board_color,
                                     outline='')

    def draw_banner(self):
        '''Creates the banner, this this object will be used to display the title of the game,
            a countdown to the start of the game and when the game is over.
        param: None
        return: int: the id number of the banner text
        '''
        id_num = self.canvas.create_text(self.WIDTH//2,
                                self.HEIGHT//3,
                                text='Snake',
                                font=("Helvetica", 72, "bold"))
        return id_num

    def draw_instructions(self):
        '''Creates the instructions on the page
        param: None
        return: int: the id number of the instructions text
        '''
        id_num = self.canvas.create_text(self.WIDTH*4//5,
                                         self.HEIGHT//3,
                                         text='Press Return to start\n\nW == Up\nA == Left\nS == Down\nD == Right',
                                         font=("Helvetica", 24))
        return id_num

    def draw_current_score(self):
        ''' Displays the current score the game
        param: None
        return: int: the id number of the current score
        '''
        id_num = self.canvas.create_text(self.WIDTH*4//5,
                                         self.HEIGHT-10,
                                         text='0',
                                         font=("Helvetica", 22))
        return id_num

    def draw_top_scores(self):
        ''' Displays the top scores
        param: None
        return: int: the id number of the current score
        '''
        scores = self.get_top_scores()
        scoreboard = 'Top scores\n\n{}\n{}\n{}\n{}\n{}'.format(*scores)
        id_num = self.canvas.create_text(self.WIDTH//5,
                                         self.HEIGHT//3,
                                         text=scoreboard,
                                         font=("Helvetica", 22))

        return id_num

    def get_top_scores(self):
        '''Gets the top scores saved by pickling 
        param: None
        return: list: a list of the the top scores ordered from highest to lowest
        '''
        self.setup_top_scores_file()
        with open('top.dat','rb') as f:
            return pickle.load(f)

    def setup_top_scores_file(self):
        '''Creates a top.dat file if there is none in this path
            then sets the top scores to default of zero
        param: None
        return: list: the top five scores
        '''
        if not os.path.exists('top.dat'):
            with open('top.dat','wb') as f:
                high_score = [0,0,0,0,0]
                pickle.dump(high_score,f)


if __name__ == '__main__':
    Snake()
    tk.mainloop()