import tkinter
import point
from game_logic import *


class board:
    def __init__(self,GameState):
        self.root_window = tkinter.Tk()
        self.GameState = GameState
        self.state = GameState.board
        self.row = GameState.height
        self.column = GameState.width
        self.turn = GameState.turn
        self.deter = GameState.deter
        self.left_end,self.up_end = 0,0
        self.right_end,self.lower_end = 1,1
        self.init = "B"
        if self.column <= self.row:
            self.left_end = (self.row - self.column)/2/self.row
            self.right_end = (self.row + self.column)/2/self.row
        elif self.column > self.row:         
            self.up_end = (self.column - self.row)/2/self.column
            self.lower_end = (self.column + self.row)/2/self.column
        self.swtchbtn = tkinter.Button(master = self.root_window,text = "Switch to White",command=self.sbutton)
        self.swtchbtn.grid(
            row = 2,column = 0,sticky = tkinter.W)

        self.quitbtn = tkinter.Button(master = self.root_window,text = "Quit",command = lambda:self.root_window.destroy())

        self.quitbtn.grid(
            row = 2,column = 0,sticky = tkinter.E)

        self.canvas = tkinter.Canvas(
            master = self.root_window, width = 500, height = 500,
            background = "#93e2ff")
        self.canvas.grid(
            row = 0,column = 0,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)
        self.canvas2 =tkinter.Canvas(
            master = self.root_window, width = 500,height =200,
            background = "#66ccff")
        self.canvas_height = 500 
        self.canvas_width = 500
        self.canvas2_height = 200
        self.canvas2_width = 500
        self.canvas2.grid(
            row = 1,column = 0,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)
        self.show_status()

        self.canvas.bind("<Configure>", self.resize)
##        self.canvas.bind("<Motion>",self.track_mouse)
        self.canvas.bind("<Button-1>",self.move)
        self.canvas2.bind("<Configure>", self.resize_canvas2)

        self.root_window.rowconfigure(0,weight = 2)
        self.root_window.rowconfigure(1,weight = 1)
        self.root_window.rowconfigure(2,weight = 1)
        self.root_window.columnconfigure(0,weight = 2)

    def sbutton(self):
        if self.init == "B":
            self.init = "W"
            self.swtchbtn["text"] = "Start Game"
        elif self.init == "W":
            GameState.game_end(self.GameState)
            self.init = "SBSBSBSBSB"
            self.swtchbtn["text"] = "Game Started"
            self.show_status()
        pass

##    def track_mouse(self,event):
##        print(event)

    def resize_canvas2(self,event):
        self.canvas2_height = event.height
        self.canvas2_width = event.width
        self.show_status()
        
    def resize(self,event):
        self.canvas_height = event.height
        self.canvas_width = event.width
        self.draw_grid(self.row,self.column)
        self.draw_pieces(self.state)
        
    def move(self,event):
        try:
            
            if self.init == "B":

                change_row,change_column = self._on_grid(event)
                self.GameState.board[change_row-1][change_column-1] = "B"
                self.draw_pieces(self.state)
                self.show_status()
                pass
            elif self.init == "W":
                change_row,change_column = self._on_grid(event)
                self.GameState.board[change_row-1][change_column-1] = "W"
                self.draw_pieces(self.state)
                self.show_status()
                pass
            else:
                if board._in_x_range(self,event) and board._in_y_range(self,event):
                    ## position_order_as_gamelogic = [(n-th_of_the_column,n-th_of_row)]第几行的第几个先向下再向右
                    
                    if board._on_grid(self,event) in GameState._valid_positions(self.GameState,self.GameState.turn):
                        GameState.move(self.GameState,board._on_grid(self,event),self.GameState.turn)
                        self.draw_pieces(self.state)

                    self.show_status()
        except IndexError:
            pass
        

    def _on_grid(self,event):
        if self.column<=self.row:
            grid_position = (int(((event.y/self.canvas_height)-self.up_end)*self.row)+1,
                             int(((event.x/self.canvas_width)-self.left_end)*self.row)+1)
        elif self.column>self.row:
            grid_position = (int(((event.y/self.canvas_height)-self.up_end)*self.column)+1,
                             int(((event.x/self.canvas_width)-self.left_end)*self.column)+1)
        print(grid_position)
        ##grid_position=(down_how_many_row,right_how_many_column)
        return grid_position

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

    def show_status(self):
        self.canvas2.delete(tkinter.ALL)
        wpix,hpix = self.canvas2_width,self.canvas2_height
        status_middle = point.Point(1/2,1/2).pixel(wpix,hpix)
        self.canvas2.create_text(status_middle,
                                 text = "FULL VERSION\nBLACK: {}\nWHITE: {}\nTURN:{}\nWINNER:{}".format(self.GameState.count_pieces("B"),
                                                                                          self.GameState.count_pieces("W"),
                                                                                          self.GameState.turn,
                                                                                          self.GameState.winner),
                                 font=("calibri",20),
                                 fill = "white")
        

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
