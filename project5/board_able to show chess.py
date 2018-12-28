import tkinter
import point
from game_logic import *


class board:
    def __init__(self,state,row,column,first_move,winstate):
        self.state = state
        self.row = row
        self.column = column
        self.first_move = first_move
        self.winstate = winstate
        self.left_end,self.up_end = 0,0
        self.right_end,self.lower_end = 1,1
        if self.column <= self.row:
            self.left_end = (self.row - self.column)/2/self.row
            self.right_end = (self.row + self.column)/2/self.row
        elif self.column > self.row:         
            self.up_end = (self.column - self.row)/2/self.column
            self.lower_end = (self.column + self.row)/2/self.column


        self.root_window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            master = self.root_window, width = 500, height = 500,
            background = "#93e2ff")
        self.canvas.grid(
            row = 0,column = 0,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)
        self.canvas2 =tkinter.Canvas(
            master = self.root_window, width = 150,height =500,
            background = "#66ccff")
        self.canvas2.grid(
            row = 0,column = 1,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)
        self.canvas_height = 500 
        self.canvas_width = 500

        self.canvas.bind("<Configure>", self.resize)
        self.canvas.bind("<Motion>",self.track_mouse)
        self.root_window.rowconfigure(0,weight = 1)
        self.root_window.columnconfigure(0,weight = 1)
        self.root_window.columnconfigure(1,weight = 1)

    def resize(self,event):
        print("resized window size is",self.canvas_height,self.canvas_width)
        self.canvas_height = event.height
        self.canvas_width = event.width
        self.draw_grid(self.row,self.column)
        self.draw_pieces(self.state)
        
    def track_mouse(self,event):
        major = self.row if self.row > self.column else self.column
        if board._in_x_range(self,event) and board._in_y_range(self,event):
            board._on_grid(self,event)
            print("Valid")

    def _on_grid(self,event):
        if self.column<=self.row:
            grid_position = (int(((event.x/self.canvas_width)-self.left_end)*self.row)+1,
                             int(((event.y/self.canvas_height)-self.up_end)*self.row)+1)
        elif self.column>self.row:
            grid_position = (int(((event.x/self.canvas_width)-self.left_end)*self.column)+1,
                             int(((event.y/self.canvas_height)-self.up_end)*self.column)+1)
        print(grid_position)

    def _in_x_range(self,event):
        if self.column<=self.row:
            if self.left_end<event.x/self.canvas_width<self.right_end:
                return True
            else:
                return False
        else:
            return True

    def _in_y_range(self,event):
        if self.column>self.row:         
            if self.up_end<event.y/self.canvas_height<self.lower_end:
                return True
            else:
                return False
        else:
            return True
        
    def draw_grid(self,row,column):
        major = self.row if self.row >= self.column else self.column
        y_parl_begin_frac = [point.Point(((major-column)/2+i)/major,(major-row)/2/major) for i in range(column+1)]
        y_parl_end_frac = [point.Point(((major-column)/2+i)/major,(major+row)/2/major) for i in range(column+1)]
        x_parl_begin_frac = [point.Point((major-column)/2/major,((major-row)/2+i)/major) for i in range(row+1)]
        x_parl_end_frac = [point.Point((major+column)/2/major,((major-row)/2+i)/major) for i in range(row+1)]

        wpix,hpix = self.canvas.winfo_width(),self.canvas.winfo_height()

        k = [y_parl_begin_frac,y_parl_end_frac,x_parl_begin_frac,x_parl_end_frac]
        self.canvas.delete(tkinter.ALL)
        for i in range(len(y_parl_begin_frac)):
            self.canvas.create_line(y_parl_begin_frac[i].pixel(wpix,hpix),
                                    y_parl_end_frac[i].pixel(wpix,hpix),
                                    fill = "white")

        for i in range(len(x_parl_begin_frac)):
            self.canvas.create_line(x_parl_begin_frac[i].pixel(wpix,hpix),
                                    x_parl_end_frac[i].pixel(wpix,hpix),
                                    fill = "white")

        pass

    def draw_pieces(self,state):
        major = self.row if self.row >= self.column else self.column
        grid_unit_height = 1/major*self.canvas_height
        grid_unit_width = 1/major*self.canvas_width
        white_list = []##(row,column) start from 1
        black_list = []##(row,column) start from 1
        if self.row >= self.column:
            n_column_to_right = int((self.row-self.column)/2)
            for i in range(len(state)):
                for j in range(len(state[i])):
                    if state[i][j]=="B":
                        black_list.append((i+1,j+1+n_column_to_right))
                    elif state[i][j]=="W":
                        white_list.append((i+1,j+1+n_column_to_right))
        elif self.row < self.column:
            n_row_lower = int((self.column-self.row)/2)
            for i in range(len(state)):
                for j in range(len(state[i])):
                    if state[i][j]=="B":
                        black_list.append((i+1+n_row_lower,j+1))
                    elif state[i][j]=="W":
                        white_list.append((i+1+n_row_lower,j+1))
                        
        for white_piece in white_list:
            self.canvas.create_oval((white_piece[1]-1)*grid_unit_width,
                                    (white_piece[0]-1)*grid_unit_height,
                                    white_piece[1]*grid_unit_width,
                                    white_piece[0]*grid_unit_height,
                                    fill = "white",
                                    outline = "white")
            
        for black_piece in black_list:
            self.canvas.create_oval((black_piece[1]-1)*grid_unit_width,
                                    (black_piece[0]-1)*grid_unit_height,
                                    black_piece[1]*grid_unit_width,
                                    black_piece[0]*grid_unit_height,
                                    fill = "black",
                                    outline = "black")
        
        
    def run(self)->None:
        self.root_window.mainloop()

k = board([['.', 'B', '.', 'W', 'W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'B'], ['.', 'B', '.', '.', '.', 'B', 'B', 'W', '.', '.', 'B', 'W', 'B', '.', '.', 'B'], ['.', '.', '.', 'B', '.', 'W', 'W', 'B', '.', '.', 'W', '.', 'B', '.', '.', '.'], ['.', '.', '.', 'W', 'B', '.', '.', '.', '.', '.', 'B', 'W', '.', '.', '.', '.'], ['W', 'W', 'W', '.', '.', '.', '.', '.', 'W', '.', '.', '.', '.', '.', '.', 'B'], ['B', '.', '.', '.', '.', '.', 'B', 'W', '.', '.', '.', '.', '.', '.', '.', '.']],6,16,"","")

print(k)
