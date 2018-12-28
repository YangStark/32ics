#Shengquan Ni 46564157 
from tkinter import *
from Othello_Game_FINAL import *


#constant var of fonts
TITLE_FONT=('Arial', 15)
DEFAULT_FONT=('Arial', 12)





class Othello_TK:
    def __init__(self):
        '''
        initiate all variables for the GUI
        and setup the window
        
        '''
        self.data_dict={}
        self.widget_dict={}
        self.widget_dict2={}
        self.grid_pool=[]
        self.item_pool=[]
        self.pre_board=None
        self.Game=None
        self.window = Tk()
        self.lock=False
        self.xoffset=1
        self.yoffset=1
        self.pre_xoffset=1
        self.pre_yoffset=1
        self.window.title('Othello')
        self.window.geometry('513x600')
        self.window.bind('<Configure>',self.__on_resize)
        self.window.protocol('WM_DELETE_WINDOW',self.__Quit)
        self.__init_GUI()
        mainloop()

    def __on_resize(self,e):
        '''
        adjust the xoffset and yoffset and redraw the canvas
        
        '''
        canvas=self.widget_dict2['game_canvas']
        cw=canvas.winfo_width()
        ch=canvas.winfo_height()
        ww=self.window.winfo_width()
        wh=self.window.winfo_height()
        if ch>1 and cw>1 and ch<wh and cw<ww:
            self.xoffset=cw/513
            self.yoffset=ch/515
        else:
            self.xoffset=ww/513
            self.yoffset=wh/600
        if self.Game:
            self.__redraw()
            self.pre_xoffset=self.xoffset
            self.pre_yoffset=self.yoffset

    def __redraw(self):
        '''
        redraw the grid(lines), dices on the board and the vaild positions
        
        '''
        self.__create_grid()
        self.__redraw_dices()
        self.__draw_vaildpos()

    def __redraw_dices(self):
        '''
        according to xoffset and yoffset, redraw all the dices on the board
        
        '''
        canvas=self.widget_dict2['game_canvas']
        for i in range(self.Game.height):
            for j in range(self.Game.width):
                if self.board[i][j]!=None:
                    x1,y1,x2,y2=canvas.coords(self.board[i][j])
                    canvas.coords(self.board[i][j],x1/self.pre_xoffset*self.xoffset,y1/self.pre_yoffset*self.yoffset,x2/self.pre_xoffset*self.xoffset,y2/self.pre_yoffset*self.yoffset)
            

    def __init_GUI(self):
        '''
        initiate all widgets and data, then put them in different big dicts
        
        '''
        self.widget_dict['title_label']=Label(self.window, text='FULL Othello', font=TITLE_FONT)
    
        NUM_OF_ROWS=IntVar()
        NUM_OF_ROWS.set(4)
        self.widget_dict['rows_label']=Label(self.window, text='number of rows of the board', font=DEFAULT_FONT)
        self.widget_dict['rows_scale']=Scale(self.window,from_ = 4,to = 16,resolution = 2,orient = HORIZONTAL,variable=NUM_OF_ROWS)
        
        NUM_OF_COLS=IntVar()
        NUM_OF_COLS.set(4)
        self.widget_dict['cols_label']=Label(self.window, text='number of columns of the board', font=DEFAULT_FONT)
        self.widget_dict['cols_scale']=Scale(self.window,from_ = 4,to = 16,resolution = 2,orient = HORIZONTAL,variable=NUM_OF_COLS)
        
        FIRST_MOVE=StringVar()
        FIRST_MOVE.set('B')
        self.widget_dict['move_first_label']=Label(self.window, text='choose a player who move first', font=DEFAULT_FONT)
        self.widget_dict['move_first_b']=Radiobutton(self.window, text="Black", variable=FIRST_MOVE, value='B')
        self.widget_dict['move_first_w']=Radiobutton(self.window, text="White", variable=FIRST_MOVE, value='W')

        TOP_LEFT=StringVar()
        TOP_LEFT.set('B')
        self.widget_dict['top_left_label']=Label(self.window, text='choose a color which is in top-left at the beginning', font=DEFAULT_FONT)
        self.widget_dict['top_left_b']=Radiobutton(self.window,text="Black", variable=TOP_LEFT, value='B')
        self.widget_dict['top_left_w']=Radiobutton(self.window, text="White", variable=TOP_LEFT, value='W')

        WIN_DETERMINE=StringVar()
        WIN_DETERMINE.set('>')
        self.widget_dict['win_determine_label']=Label(self.window, text='choose the player with the most or the fewer discs on the board\n at the end of the game wins', font=DEFAULT_FONT)
        self.widget_dict['win_determine_>']=Radiobutton(self.window,text=">", variable=WIN_DETERMINE, value='>')
        self.widget_dict['win_determine_<']=Radiobutton(self.window, text="<", variable=WIN_DETERMINE, value='<')

        
        self.widget_dict['start_botton']=Button(self.window,text = 'Start Game',command = self.__GameStart)
        
        self.data_dict={'rows':NUM_OF_ROWS,'cols':NUM_OF_COLS,'fm':FIRST_MOVE,'tf':TOP_LEFT,'wd':WIN_DETERMINE}

        self.data_dict['stats']=StringVar()
        self.data_dict['stats'].set('BLACK:2 WHITE:2 TURN:{}'.format(self.data_dict['fm'].get()))
        self.widget_dict2['game_stats']=Label(self.window, textvariable=self.data_dict['stats'], font=DEFAULT_FONT)

        self.data_dict['winner']=StringVar()
        self.data_dict['winner'].set('')
        self.widget_dict2['game_winner']=Label(self.window, textvariable=self.data_dict['winner'], font=TITLE_FONT)

        self.widget_dict2['game_canvas']=Canvas(self.window,bg='#{:02x}{:02x}{:02x}'.format(38,188,213),height=510,width=510)
        self.widget_dict2['game_canvas'].bind('<ButtonRelease-1>',self.__click_callback)
        
        self.widget_dict2['restart']=Button(self.window,text = 'Restart',command = self.__GameReStart)
        self.widget_dict2['quit']=Button(self.window,text = 'Quit',command=self.__Quit)
        self.widget_dict2['return']=Button(self.window,text = 'Return to Menu',command = self.__ReturnMenu)
        self.widget_dict2['withdraw']=Button(self.window,text = 'Withdraw',command = self.__Withdraw)

        self.data_dict['AI']=IntVar()
        self.widget_dict['AI']=Checkbutton(self.window,text='Need AI?\n AI -> White\n Withdraw -> until turn=black',variable=self.data_dict['AI'],onvalue=1,offvalue=0,height=5,width=50)

        self.__widget_place_1()

    def __widget_place_1(self):
        '''
        put the widgets to the main menu. 

        '''
        self.widget_dict['title_label'].grid(padx=200,pady=15,row=0,column=0,columnspan=8)
        self.widget_dict['rows_label'].grid(row=1,column=0,columnspan=8,pady=5)
        self.widget_dict['rows_scale'].grid(row=2,column=0,columnspan=8)
        self.widget_dict['cols_label'].grid(row=3,column=0,columnspan=8,pady=5)
        self.widget_dict['cols_scale'].grid(row=4,column=0,columnspan=8)
        self.widget_dict['move_first_label'].grid(row=5,column=0,columnspan=8,pady=5)
        self.widget_dict['move_first_b'].grid(row=6,column=3)
        self.widget_dict['move_first_w'].grid(row=6,column=4)
        self.widget_dict['top_left_label'].grid(row=7,column=0,columnspan=8,pady=5)
        self.widget_dict['top_left_b'].grid(row=8,column=3)
        self.widget_dict['top_left_w'].grid(row=8,column=4)
        self.widget_dict['win_determine_label'].grid(row=9,column=0,columnspan=8,pady=5)
        self.widget_dict['win_determine_>'].grid(row=10,column=3)
        self.widget_dict['win_determine_<'].grid(row=10,column=4)
        self.widget_dict['start_botton'].grid(row=11,column=0,columnspan=8,pady=10)
        self.widget_dict['AI'].grid(row=12,column=0,columnspan=8,pady=10)
        for i in range(8):
            self.window.columnconfigure(i, weight = 1,minsize=37)
        for i in range(12):
            self.window.rowconfigure(i, weight = 1)
            
            

    def __widget_place_2(self):
        '''
        put the widgets to the game display.
        
        '''
        self.widget_dict2['game_winner'].grid(columnspan=4,sticky=W+S+N+E)
        self.widget_dict2['game_canvas'].grid(row=1,columnspan=4,sticky=W+S+N+E)
        self.widget_dict2['game_stats'].grid(row=2,columnspan=4,sticky=W+S+N+E)
        self.widget_dict2['restart'].grid(row=3,column=0)
        self.widget_dict2['quit'].grid(row=3,column=3)
        self.widget_dict2['return'].grid(row=3,column=2)
        self.widget_dict2['withdraw'].grid(row=3,column=1)
        for i in range(4):
            self.window.rowconfigure(i, weight = 1)
            self.window.columnconfigure(i, weight = 1,minsize=127)
    
    def __Withdraw(self):
        '''
        callback func when user decide to withdraw

        withdraw 1 turn when PVP
        withdraw until the black's turn when Player VS AI
        
        '''
        if self.lock:
            return
        self.data_dict['winner'].set('')
        self.lock=True
        if self.data_dict['AI'].get()==1:
            if self.Game.pre_count>=2:
                flag=True
                while flag:
                    self.pre_board=copy.deepcopy(self.Game.board)
                    dice=self.Game.cancel_drop()
                    self.__update_stats(dice,True)
                    if dice[2]=='B':
                        flag=False
        else:
            if self.Game.pre_count>=1:
                self.pre_board=copy.deepcopy(self.Game.board)
                self.__update_stats(self.Game.cancel_drop(),True)
        self.lock=False


    def __click_callback(self,event):
        '''
        callback func when user click the window

        map the mouse position to the board index
        and check if it is a vaild drop
        then drop it, update stats, refresh the whole display.
        
        '''
        if self.lock:
            return
        x=int((event.x-self.data_dict['startx'])/(32*self.xoffset))
        y=int((event.y-self.data_dict['starty'])/(32*self.yoffset))
        #Player Moves
        if x>=0 and x<self.data_dict['rows'].get() and y>=0 and y<self.data_dict['cols'].get():
            if (y,x) in self.Game.vaildpos:
                self.lock=True
                self.data_dict['winner'].set('VAILD ({},{})'.format(y+1,x+1))
                turn=self.Game.turn
                self.pre_board=copy.deepcopy(self.Game.board)
                self.Game.drop((y,x))
                self.__update_stats((y,x,turn))
                self.lock=False
            elif self.Game.isover == False:
                self.data_dict['winner'].set('INVAILD')
        elif self.Game.isover == False:
            self.data_dict['winner'].set('INVAILD')
        if self.data_dict['AI'].get():
            while self.Game.turn=='W' and not self.Game.isover:
                self.__AI_moves()

    def __AI_moves(self):
        '''
        one move of AI on board
        
        '''
        self.lock=True
        self.pre_board=copy.deepcopy(self.Game.board)
        self.data_dict['winner'].set('Waiting for AI..')
        self.widget_dict2['game_canvas'].update()
        pos=self.Game.AI_move_input()
        self.Game.drop(pos)
        self.data_dict['winner'].set('VAILD ({},{})'.format(pos[0]+1,pos[1]+1))
        self.__update_stats((pos[0],pos[1],'W'))
        self.lock=False

    
    def __update_stats(self,pos,reverse=False):
        '''
        update the stats of the game and show it

        '''
        stats=self.Game.get_stats()
        self.data_dict['stats'].set('BLACK:{} WHITE:{} TURN:{}'.format(stats['B'],stats['W'],self.Game.turn))
        self.__display_tk(pos,reverse)
        if self.Game.isover:
            self.data_dict['winner'].set('WINNER:{}'.format(self.Game.get_winner()))
            self.data_dict['stats'].set('BLACK:{} WHITE:{}'.format(stats['B'],stats['W']))



    def __create_update_pos(self,rect):
        '''
        create a list of points on the game board which represent a square
        then choose the dices which has filped because of the last drop
        
        '''
        result=[]
        for i in range(4):
            end=max(rect[i][i%2],rect[i-3][i%2])
            start=min(rect[i][i%2],rect[i-3][i%2])
            for j in range(start,end+1):
                pos=(rect[i][0],j) if i%2==1 else (j,rect[i][1])
                if self.Game.on_board(pos):
                    y,x=pos
                    color=self.Game.board[y][x]
                    if color!='.' and self.pre_board[pos[0]][pos[1]]!=color:
                        result.append((y,x,color))
        return result
        
            
            
    def __update_canvas(self,rect=None,pos=None,reverse=False):
        '''
        according to the argument to choose a way to update dice

        rect:
            filp the dices with a growing square
        pos:
            expand or shrink one specific point, it depends on the argument called 'reverse'
            
        '''
        if rect:
            pos=self.__create_update_pos(rect)
            self.__flip(pos)
        elif pos:
            if not reverse:
                self.__scale([pos],False)
            else:
                self.__scale([pos],True)

    def __scale(self,pos,flag):
        '''
        the animation of scaling
        
        '''
        canvas=self.widget_dict2['game_canvas']
        for i in range(1,11):
            starty=self.data_dict['starty']
            startx=self.data_dict['startx']
            delta=(1.5*i) if flag else (15-1.5*i)
            for p in pos:
                canvas.delete(self.board[p[0]][p[1]])
                self.board[p[0]][p[1]]=canvas.create_oval(startx+(p[1]*32+2+delta)*self.xoffset,starty+(p[0]*32+2+delta)*self.yoffset,startx+((p[1]+1)*32-2-delta)*self.xoffset,starty+(p[0]*32+30-delta)*self.yoffset,fill='white'if p[2]=='W' else 'black',width=0)
            canvas.update()
            time.sleep(0.01)
        if flag:
            for p in pos:
                canvas.delete(self.board[p[0]][p[1]])
                self.board[p[0]][p[1]]=None
    
    def __flip(self,pos):
        '''
        the animation of fliping
        
        '''
        canvas=self.widget_dict2['game_canvas']
        if pos!=[]:
            for j in range(1,21):
                starty=self.data_dict['starty']
                startx=self.data_dict['startx']
                if j>10:
                    delta=15-1.5*(j-10)
                else:
                    delta=1.5*j
                for i in pos:
                    if j>10:
                        fillcolor='white'if i[2]=='W' else 'black'
                    else:
                        fillcolor='white'if i[2]=='B' else 'black' 
                    canvas.delete(self.board[i[0]][i[1]])
                    self.board[i[0]][i[1]]=canvas.create_oval(startx+(i[1]*32+2+delta)*self.xoffset,starty+(i[0]*32+2)*self.yoffset,startx+((i[1]+1)*32-2-delta)*self.xoffset,starty+(i[0]*32+30)*self.yoffset,fill=fillcolor,width=0)
                canvas.update()
                time.sleep(0.01)
            
    def __collect_dices(self):
        '''
        return a list of the position of dices on the game board
        
        '''
        result=[]
        for i in range(self.Game.height):
            for j in range(self.Game.width):
                if self.Game.board[i][j]!='.':
                    result.append((i,j,self.Game.board[i][j]))
        return result

    def __draw_vaildpos(self):
        '''
        draw the vaild positions of the current player
        
        '''
        self.__clean_up(self.item_pool)
        canvas=self.widget_dict2['game_canvas']
        starty=self.data_dict['starty']
        startx=self.data_dict['startx']
        for i in self.Game.vaildpos:
            self.item_pool.append(canvas.create_oval(startx+(i[1]*32+13)*self.xoffset,starty+(32*i[0]+13)*self.yoffset,startx+((i[1]+1)*32-13)*self.xoffset,starty+(32*i[0]+19)*self.yoffset,fill='white' if self.Game.turn=='W' else 'black',width=0))
        
    def __init_display(self):
        '''
        the display of initiating a new game
        
        '''
        self.__scale(self.__collect_dices(),False)
        self.__draw_vaildpos()

            
    def __display_tk(self,pos,reverse=False):
        '''
        the full display process
        
        '''
        self.__clean_up(self.item_pool)
        maxtimes=max(pos[0],pos[1],self.Game.height-pos[0],self.Game.width-pos[1])
        if reverse:
            rect=[[pos[0]-maxtimes,pos[1]-maxtimes],[pos[0]+maxtimes,pos[1]-maxtimes],[pos[0]+maxtimes,pos[1]+maxtimes],[pos[0]-maxtimes,pos[1]+maxtimes]]
            delta=-1
            for i in range(maxtimes):
                self.__update_canvas(rect=rect)
                self.__expand_rect(rect,delta)
            self.__update_canvas(pos=pos,reverse=True)
        else:
            self.__update_canvas(pos=pos)
            rect=[[pos[0]-1,pos[1]-1],[pos[0]+1,pos[1]-1],[pos[0]+1,pos[1]+1],[pos[0]-1,pos[1]+1]]
            delta=1
            for i in range(maxtimes):
                self.__update_canvas(rect=rect)
                self.__expand_rect(rect,delta)
        self.__draw_vaildpos()
        self.widget_dict2['game_canvas'].update()
            
    def __expand_rect(self,rect,delta):
        '''
        expend square corners by delta
        
        '''
        rect[0][0]-=delta
        rect[0][1]-=delta
        rect[1][0]+=delta
        rect[1][1]-=delta
        rect[2][0]+=delta
        rect[2][1]+=delta
        rect[3][0]-=delta
        rect[3][1]+=delta
        

    def __clean_up(self,pool):
        '''
        clean up a pool and delete the instances in game canvas at the same time
        
        '''
        for i in range(len(pool)-1,-1,-1):
            self.widget_dict2['game_canvas'].delete(pool[i])
            del pool[i]

    def __hide_widget(self,dict_of_widget):
        '''
        hide a set of widget and reset rows and columns of the root window
        
        '''
        for i in dict_of_widget.values():
            i.grid_forget()
        for i in range(8):
            self.window.columnconfigure(i, weight =0,minsize=0)
        for i in range(12):
            self.window.rowconfigure(i, weight =0,minsize=0)

    def __create_grid(self):
        '''
        create the lines which form a game board
        
        '''
        self.__clean_up(self.grid_pool)
        l=32
        canvas=self.widget_dict2['game_canvas']
        rows=self.data_dict['rows'].get()
        self.data_dict['startx']=((512-l*rows)/2)*self.xoffset
        cols=self.data_dict['cols'].get()
        self.data_dict['starty']=((512-l*cols)/2)*self.yoffset
        for i in range(rows+1):
            self.grid_pool.append(canvas.create_line(self.data_dict['startx']+(i*l)*self.xoffset,(256-cols*16)*self.yoffset,self.data_dict['startx']+(i*l)*self.xoffset,(256+cols*16)*self.yoffset))
        for i in range(cols+1):
            self.grid_pool.append(canvas.create_line((256-rows*16)*self.xoffset,self.data_dict['starty']+(i*l)*self.yoffset,(256+rows*16)*self.xoffset,self.data_dict['starty']+(i*l)*self.yoffset))


        
    def __GameStart(self):
        '''
        callback func when user press 'start game' botton

        init a new Game and save it to self.game
        display the current game
        if its an AI game and first turn is white's
        AI moves
        
        '''
        self.__hide_widget(self.widget_dict)
        self.__widget_place_2()
        if self.Game:
            del self.Game
        self.Game=Othello_Game(tuple(map(lambda x:self.data_dict[x].get(),['rows','cols','fm','tf','wd'])))
        self.data_dict['winner'].set('')
        self.data_dict['stats'].set('BLACK:2 WHITE:2 TURN:{}'.format(self.data_dict['fm'].get()))
        self.board=[[None for i in range(self.Game.width)] for j in range(self.Game.height)]
        self.__create_grid()
        self.__init_display()
        self.widget_dict2['game_canvas'].update()
        if self.Game.turn=='W'and self.data_dict['AI'].get():
            self.__AI_moves()
         

    def __GameReStart(self):
        '''
        callback func when user press 'restart' button

        reset all game stats
        restart the game
        display the current game
        if its an AI game and first turn is white's
        AI moves
        
        '''
        if self.lock:
            return
        self.data_dict['winner'].set('')
        self.data_dict['stats'].set('BLACK:2 WHITE:2 TURN:{}'.format(self.data_dict['fm'].get()))
        self.__clean_up(self.item_pool)
        self.__scale(self.__collect_dices(),True)
        self.Game.restart()
        self.__create_grid()
        self.__init_display()
        self.widget_dict2['game_canvas'].update()
        if self.Game.turn=='W'and self.data_dict['AI'].get():
            self.__AI_moves()


    def __Quit(self):
        '''
        callback func when user press 'quit' button

        destroy the window
        
        '''
        if self.lock:
            return
        self.window.destroy()


    def __ReturnMenu(self):
        '''
        callback func when user press 'return main menu' button

        delete the game
        hide all widgets of game display
        place all widgets of main menu
        
        '''
        if self.lock:
            return
        self.board=None
        if self.Game:
            del self.Game
        self.Game=None
        self.widget_dict2['game_canvas'].delete('all')
        self.__hide_widget(self.widget_dict2)
        self.__widget_place_1()




if __name__=='__main__':
    Othello_TK()





        
