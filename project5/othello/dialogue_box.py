import tkinter
from game_logic import *
from tk_board import *
class dialoguebox:
    def __init__(self):
        
        self.root_window = tkinter.Tk()
        strvar1 = tkinter.StringVar(self.root_window)
        strvar1.set("None")
        strvar2 = tkinter.StringVar(self.root_window)
        strvar2.set("None")
        strvar3 = tkinter.StringVar(self.root_window)
        strvar3.set("None")
        strvar4 = tkinter.StringVar(self.root_window)
        strvar4.set("None")
        w = tkinter.Label(self.root_window,text = "Row:")
        w.pack()
        options = tkinter.OptionMenu(self.root_window, strvar1, "4","6","8","10","12","14","16")
        options.pack()
        w = tkinter.Label(self.root_window,text = "Column:")
        w.pack()
        options2 = tkinter.OptionMenu(self.root_window, strvar2, "4","6","8","10","12","14","16")
        options2.pack()
        w = tkinter.Label(self.root_window,text = "First move:")
        w.pack()
        option_move = tkinter.OptionMenu(self.root_window,strvar3, "Black","White")
        option_move.pack()
        w = tkinter.Label(self.root_window,text = "Winner determinant:")
        w.pack()
        option_win = tkinter.OptionMenu(self.root_window,strvar4, ">","<")
        option_win.pack()

        
        btn = tkinter.Button(self.root_window,text = "    ok    ",command=lambda :self.call_GUI(int(strvar1.get()),
                                                                                                int(strvar2.get()),
                                                                                                strvar3.get(),
                                                                                                strvar4.get()))
        btn.pack()
        
        self.root_window.mainloop()

    def call_GUI(self,row,column,first_move,deter):
        empty_board = []
        for i in range(row):
            row_list = []
            for j in range(column):
                row_list.append(".")
            empty_board.append(row_list)
        new_game=GameState(row,column,"B" if first_move == "Black" else "W",deter,empty_board)
        init_board=board(new_game)
        self.root_window.destroy()
        
if __name__ == "__main__":
    k = dialoguebox()
