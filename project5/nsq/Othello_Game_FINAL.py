#Shengquan Ni 46564157 
import copy
import time
import random


#the max value of AI estimate
MAX_VALUE=100000000
#the dict to map opposite
Opposite={'W':'B','B':'W'}

isHeld=lambda turn,pos:1 if pos==turn else 0
#the dict to map str dices to number 
Transform={'.':0,'W':1,'B':2}

'''
the struct for store information in a hash table
key for hashkey
depth for the depth of the situation of the game
lower for min value of this situation
upper for max value of this situation
move for the position to drop
'''
class hash_unit:
    def __init__(self):
        self.key=0
        self.depth=-1
        self.lower=0
        self.upper=0
        self.move=None





class Othello_Game:
        
    def __init__(self,data):
        '''init of one game'''
        self.initdata=data
        self.__init_AI(data)
        self.__init_board(data)
        self.__init_hash_table(data)
        self.__init_value_matrix(data)
        self.__init_withdraw_system()
        self.__generate_hash_key()
        self.__vaild_check()

    def restart(self):
        '''restart a game'''
        self.__init_board(self.initdata)
        self.__init_withdraw_system()
        self.__generate_hash_key()
        self.__vaild_check()

    def __init_board(self,data):
        '''
        init a nested list with the data of row and col
        and put 4 dices on the board
        '''
        NUM_OF_ROWS,NUM_OF_COLS,FIRST_MOVE,TOP_LEFT,WIN_DETERMINE=data
        CHESS=[['.' for i in range(NUM_OF_ROWS)]for j in range(NUM_OF_COLS)]
        BOTTOM_RIGHT_Y=int(NUM_OF_COLS/2)
        BOTTOM_RIGHT_X=int(NUM_OF_ROWS/2)
        CHESS[BOTTOM_RIGHT_Y-1][BOTTOM_RIGHT_X-1]=TOP_LEFT
        CHESS[BOTTOM_RIGHT_Y][BOTTOM_RIGHT_X]=TOP_LEFT
        CHESS[BOTTOM_RIGHT_Y][BOTTOM_RIGHT_X-1]=Opposite[TOP_LEFT]
        CHESS[BOTTOM_RIGHT_Y-1][BOTTOM_RIGHT_X]=Opposite[TOP_LEFT]
        self.board=CHESS
        self.turn=FIRST_MOVE
        self.vaildpos=[]
        self.isover=False
        self.stats={'W':2,'B':2,'.':NUM_OF_COLS*NUM_OF_ROWS-4}
        self.width=NUM_OF_ROWS
        self.height=NUM_OF_COLS
        self.win_determine=WIN_DETERMINE
        self.probpoints=set([(BOTTOM_RIGHT_Y-2,BOTTOM_RIGHT_X-2),(BOTTOM_RIGHT_Y-2,BOTTOM_RIGHT_X-1),(BOTTOM_RIGHT_Y-1,BOTTOM_RIGHT_X-2),\
                         (BOTTOM_RIGHT_Y-2,BOTTOM_RIGHT_X),(BOTTOM_RIGHT_Y-2,BOTTOM_RIGHT_X+1),(BOTTOM_RIGHT_Y-1,BOTTOM_RIGHT_X+1),\
                         (BOTTOM_RIGHT_Y,BOTTOM_RIGHT_X+1),(BOTTOM_RIGHT_Y+1,BOTTOM_RIGHT_X+1),(BOTTOM_RIGHT_Y+1,BOTTOM_RIGHT_X),\
                         (BOTTOM_RIGHT_Y+1,BOTTOM_RIGHT_X-1),(BOTTOM_RIGHT_Y+1,BOTTOM_RIGHT_X-2),(BOTTOM_RIGHT_Y,BOTTOM_RIGHT_X-2),\
                         ])
    def __init_hash_table(self,data):
        '''init hash table for AI'''
        NUM_OF_ROWS,NUM_OF_COLS,FIRST_MOVE,TOP_LEFT,WIN_DETERMINE=data
        self.zobrist=None
        self.hash_table=None
        self.table_size=0
        self.__generate_zobrist(NUM_OF_ROWS,NUM_OF_COLS)

    def __init_withdraw_system(self):
        '''init some queue for user's withdraw'''
        self.pre_board=[]
        self.pre_probpoints=[]
        self.pre_turn=[]
        self.pre_hashkey=[]
        self.pre_vaildpos=[]
        self.pre_stats=[]
        self.pre_drop=[]
        self.pre_count=0

    def __init_value_matrix(self,data):
        '''init the estimated value for AI to evaluate the score of a situation'''
        NUM_OF_ROWS,NUM_OF_COLS,FIRST_MOVE,TOP_LEFT,WIN_DETERMINE=data
        self.values=[[(i-NUM_OF_ROWS/2)**2+(j-NUM_OF_COLS/2)**2 for i in range(NUM_OF_ROWS)]for j in range(NUM_OF_COLS)]
        for i in range(-2,2,3):
            for j in range(-2,2,3):
                self.values[i][j]*=-1
        for i in range(-1,1):
            for j in range(-1,1):
                self.values[i][j]*=4
        self.values[0][1]*=-1
        self.values[1][0]*=-1
        self.values[0][-2]*=-1
        self.values[1][-1]*=-1
        self.values[-1][-2]*=-1
        self.values[-2][-1]*=-1
        self.values[-1][1]*=-1
        self.values[-2][0]*=-1
        
    def __init_AI(self,data):
        '''init some attributes for AI'''
        NUM_OF_ROWS,NUM_OF_COLS,FIRST_MOVE,TOP_LEFT,WIN_DETERMINE=data
        self.AI_timer=0
        self.AI_max_time=2+(NUM_OF_ROWS-4)*0.06+(NUM_OF_COLS-4)*0.06
        self.AI_base_depth=1 if WIN_DETERMINE=='>' else 2
        self.AI_simple_eval=True if NUM_OF_ROWS*NUM_OF_COLS==16 else False
        self.AI_timer_start=0
    
    def __generate_zobrist(self,NUM_OF_ROWS,NUM_OF_COLS):
        '''generate a huge hash table and fill it with empty hash_unit'''
        self.zobrist=[[[random.getrandbits(15)^(random.getrandbits(15)<<15)^(random.getrandbits(15)<<30)^(random.getrandbits(15)<<45)^(random.getrandbits(15)<<60) for i in range(NUM_OF_ROWS)]for j in range(NUM_OF_COLS)]for k in range(3)]
        self.table_size=2**17
        self.hash_table=[hash_unit() for i in range(self.table_size)]

    def on_board(self,pos):
        '''determine if a position is on the game board'''
        y,x=pos
        return x>=0 and x<self.width and y<self.height and y>=0

    def cancel_drop(self):
        '''pop the queues to recover the board'''
        self.pre_count-=1
        self.board=self.pre_board.pop()
        self.probpoints=self.pre_probpoints.pop()
        self.turn=self.pre_turn.pop()
        self.hashkey=self.pre_hashkey.pop()
        self.vaildpos=self.pre_vaildpos.pop()
        self.stats=self.pre_stats.pop()
        self.isover=False
        pos=self.pre_drop.pop()
        return pos[0],pos[1],self.turn
        
    def __vaild_check(self):
        '''refresh the valid drop positions for current player(white or black)'''
        list=[]
        for i,j in self.probpoints:
            if self.board[i][j]=='.' and self.__vaild_drop((i,j)):
                list.append((i,j))
        self.vaildpos=list

    def __vaild_drop(self,pos):
        '''check if the position is vaild for current player'''
        for i in range(-1,2):
            for j in range(-1,2):
                if i!=0 or j!=0:
                    x=pos[1]+j
                    y=pos[0]+i
                    flag=False
                    while self.on_board((y,x)):
                        TEMP=self.board[y][x]
                        if TEMP=='.':
                            break
                        elif TEMP==Opposite[self.turn]:
                            flag=True
                        else:
                            if flag:
                                return True
                            else:
                                break
                        x+=j
                        y+=i
        return False

    def __Save_Game(self,pos=None):
        '''save current board and stats of the game'''
        self.pre_count+=1
        self.pre_board.append(copy.deepcopy(self.board))
        self.pre_probpoints.append(copy.deepcopy(self.probpoints))
        self.pre_turn.append(self.turn)
        self.pre_hashkey.append(self.hashkey)
        self.pre_vaildpos.append(copy.deepcopy(self.vaildpos))
        self.pre_stats.append(copy.deepcopy(self.stats))
        self.pre_drop.append(pos)
    

    def __turn_the_dices(self,pos,i,j):
        '''turn the dices from one drop position to a single direction'''
        x=pos[1]+j
        y=pos[0]+i
        while self.on_board((y,x)):
            TEMP=self.board[y][x]
            if TEMP=='.':
                self.probpoints.add((y,x))
                break
            elif TEMP==self.turn:
                while x!=pos[1] or y!=pos[0]:
                    if self.board[y][x]!=self.turn:
                        self.board[y][x]=self.turn
                        self.stats[self.turn]+=1
                        self.stats[Opposite[self.turn]]-=1
                    x-=j
                    y-=i
                break
            x+=j
            y+=i

    
    def drop(self,pos):
        '''drop one dice on the game board and turn the dices(8 directions)'''
        self.__Save_Game(pos)
        self.probpoints.remove(pos)
        self.board[pos[0]][pos[1]]=self.turn
        self.stats[self.turn]+=1
        self.stats['.']-=1
        for i in range(-1,2):
            for j in range(-1,2):
                if i!=0 or j!=0:
                    self.__turn_the_dices(pos,i,j)
        self.__generate_hash_key()
        self.turn=Opposite[self.turn]
        self.__vaild_check()
        if self.vaildpos==[]:
            self.turn=Opposite[self.turn]
            self.__vaild_check()
            if self.vaildpos==[]:
                self.isover=True

    def __generate_hash_key(self):
        '''according to current situation to create a hashkey'''
        self.hashkey=0
        for i in range(self.height):
            for j in range(self.width):
                self.hashkey^=self.zobrist[Transform[self.board[i][j]]][i][j]
            

    def get_stats(self):
        '''simply return self.stats'''
        return self.stats

    def get_winner(self):
        '''determine who is the winner and return a str to represent it'''
        d=self.get_stats()
        if self.win_determine=='>':
            return 'W' if d['W']>d['B'] else 'B' if d['B']>d['W'] else 'NONE'
        else:
            return 'W' if d['W']<d['B'] else 'B' if d['B']<d['W'] else 'NONE'

    def AI_move_input(self):
        '''
        let the AI think deeper and deeper until time is up
        and return the best move at that time
        '''
        depth=self.AI_base_depth
        result=0
        pre=None
        while True:
            try:
                result=self.__calc_value(-MAX_VALUE,MAX_VALUE,0,depth)[1]
                if result!=None:
                    pre=result
                depth+=2
                if depth>self.stats['.']-1:
                    break
            except:
                break
        self.AI_timer=0
        self.AI_timer_start=0
        return pre 

   
    def __evaluate(self,flag):
        '''
        AI evaluate the score of current situation
        based on:
        the difference of its dices and opponent's dices
        estimated score on value martix
        how many corners are occupied by itself
        the probability of occupying a corner in the next drop
        how many vaild position it and the opponent have
        how many dices are on the four sides
        '''
        if self.isover:
            winner=self.get_winner()
            if winner=='W':
                return -MAX_VALUE
            elif winner=='B':
                return MAX_VALUE
            else:
                return 0
        if self.AI_simple_eval:
            result=self.__martix_score(flag)
        else:
            result=10*self.__dices_difference(flag)\
                    +800*self.__corner_occupied(flag)\
                    +400*self.__corner_adjacent(flag)\
                    +80*self.__mobility(flag)\
                    +75*self.__dices_side(flag)\
                    +10*self.__martix_score(flag)
        return result if self.win_determine=='>' else -result

    
    def __dices_difference(self,flag):
        '''
        calculate the difference of AI's dices and opponent's dices
        and return as percentage
        '''
        opp=Opposite[flag]
        num_flag=0
        num_opp=0
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j]==flag:
                    num_flag+=1
                elif self.board[i][j]==opp:
                    num_opp+=1
        if num_opp>num_flag:
            return 100*num_flag/(num_opp+num_flag)
        elif num_opp<num_flag:
            return -100*num_opp/(num_opp+num_flag)
        else:
            return 0

    def __mobility(self,flag):
        '''
        calculate the difference of AI's number of vaild position and opponent's number of vaild position
        and return as percentage
        '''
        temp_vaildpos=self.vaildpos[:]
        num_flag=len(self.vaildpos)
        self.turn=Opposite[flag]
        self.__vaild_check()
        num_opp=len(self.vaildpos)
        self.vaildpos=temp_vaildpos[:]
        if num_opp>num_flag:
            return 100*num_flag/(num_opp+num_flag)
        elif num_opp<num_flag:
            return -100*num_opp/(num_opp+num_flag)
        else:
            return 0

    def __corner_occupied(self,flag):
        '''
        calculate how many corners are occupied by AI and the opponent
        and return a weighted score
        '''
        num=0
        opp=Opposite[flag]
        ps=(self.board[0][0],self.board[0][-1],self.board[-1][0],self.board[-1][-1])
        for p in ps:
            if p==flag:
                num+=1
            elif p==opp:
                num-=1
        return 25*num
        
    def __corner_adjacent(self,flag):
        '''
        calculate the probability of occupying a corner in the next drop
        and return a weighted score
        '''
        return 12.5*(self.__helper_corner_adjacent(Opposite[flag])-self.__helper_corner_adjacent(flag))
                             
    def __helper_corner_adjacent(self,flag):
        '''
        calculate how many positions adjacent to the corner are occupied by a player
        and return the number
        '''
        num=0
        if self.board[0][0]=='.':
            num+=1 if self.board[1][0]==flag else 0
            num+=1 if self.board[0][1]==flag else 0
            num+=1 if self.board[1][1]==flag else 0
        if self.board[0][-1]=='.':
            num+=1 if self.board[0][-2]==flag else 0
            num+=1 if self.board[1][-1]==flag else 0
            num+=1 if self.board[1][-2]==flag else 0
        if self.board[-1][-1]=='.':
            num+=1 if self.board[-1][-2]==flag else 0
            num+=1 if self.board[-2][-1]==flag else 0
            num+=1 if self.board[-2][-2]==flag else 0
        if self.board[-1][0]=='.':
            num+=1 if self.board[-1][1]==flag else 0
            num+=1 if self.board[-2][0]==flag else 0
            num+=1 if self.board[-2][1]==flag else 0
        return num

    def __dices_side(self,flag):
        '''
        calculate how many AI's dices on the four sides 
        and return the number
        '''
        num=0
        for i in range(self.height):
            for j in range(self.width):
                if not self.__isCorner(i,j):
                    break;
                if self.board[i][j]==flag:
                    if i==0 or i==col:
                        if self.board[i][j-1]=='.' and self.board[i][j+1]=='.':
                            num+=1
                    elif j==0 or j==row:
                        if self.board[i-1][j]=='.' and self.board[i+1][j]=='.':
                            num+=1
                    else:
                        if self.board[i-1][j]=='.' and self.board[i-1][j-1]=='.'\
                           and self.board[i][j-1]=='.' and self.board[i+1][j-1]=='.'\
                           and self.board[i+1][j]=='.' and self.board[i+1][j+1]=='.'\
                           and self.board[i][j+1]=='.' and self.board[i-1][j+1]=='.':
                            num+=1
        return num
                
    def __martix_score(self,flag):
        '''
        according to the estimated score matrix
        simply summing up all AI dices
        minus the sum of all opponent dices
        '''
        opp=Opposite[flag]
        num=0
        for i in range(self.height):
            for j in range(self.width):
                temp=self.board[i][j]
                if temp==flag:
                    num+=self.values[i][j]
                elif temp==opp:
                    num-=self.values[i][j]
        return num



    def __isCorner(self,i,j):
        '''
        determine if the i j in the game board is a corner
        '''
        if i==0:
            if j==0 or j==len(self.board[0]):
                return True
        elif i==len(self.board):
            if j==0 or j==len(self.board[0]):
                return True
        return False



    def __calc_value(self,a,b,depth,max_depth):
        '''
        the most important part of AI
        based on Principal Variation Search(PVS) and Alpha-beta Pruning
        blending with zobrist hash table
        '''
        #if the time is up
        #break out
        if self.AI_timer>self.AI_max_time:
            for i in range(depth):
                self.cancel_drop()
            raise 
        #init max_value
        max_value=-MAX_VALUE
        #see if the situation is in the hash table
        #if true, pruning 
        if depth!=0:
            hashunit=self.__CheckHash(depth)
            if hashunit!=None:
                if hashunit.lower>a:
                    a=hashunit.lower
                    if a>=b:
                        self.__Update_Timer()
                        return a,None
                if hashunit.upper<b:
                    b=hashunit.upper
                    if b<=a:
                        self.__Update_Timer()
                        return b,None
        #see if the game is over or the depth reaches the limit
        #if true, directly return the score of current situation
        if self.isover or depth==max_depth:
            val=self.__evaluate(self.turn)
            self.__Update_Timer()
            return val,None
        #init the best move
        move=(self.vaildpos[0][0],self.vaildpos[0][1])
        #try to drop every vaild move
        for i in self.vaildpos:
            self.drop(i)
            #if no vaild drop is found, continue searching
            if max_value==-MAX_VALUE:
                value=-self.__calc_value(-b,-max(a,max_value),depth+1,max_depth)[0]
            else:
                #try Minimal Window Search
                value=-self.__calc_value(-a-1,-a,depth+1,max_depth)[0]
                if value>a:
                    a=value
                    #if there is no pruning 
                    if a<b:
                        #continue searching
                        value=-self.__calc_value(-b,-max(a,max_value),depth+1,max_depth)[0]
            self.cancel_drop()
            self.__SaveHash(depth,value,i,a,b)
            #update max_value and the best move
            if value>max_value:
                max_value=value
                move=i
            #if this drop is the best
            if max_value>a:
                #update the floor of score
                a=max_value
            #if this drop is not good 
            if max_value>=b:
                #pruning
                self.__Update_Timer()
                return max_value,move
        self.__Update_Timer()
        return max_value,move         

    def __SaveHash(self,depth,value,i,a,b):
        '''
        function to save current data to hash table
        '''
        if value>=b:
            self.__RecordHash(depth,value,MAX_VALUE,i)
        elif value<=a:
            self.__RecordHash(depth,-MAX_VALUE,value,i)
        else:
            self.__RecordHash(depth,value,value,i)
                
    def __Update_Timer(self):
        '''
        update the AI's timer to ensure its time of thinking is constant
        '''
        if self.AI_timer_start==0:
            self.AI_timer_start=time.time()
        else:
            self.AI_timer+=time.time()-self.AI_timer_start
            self.AI_timer_start=time.time()


    def __CheckHash(self,depth):
        '''
        see if there is a same situation in the hash table
        it must deeper than current depth
        '''
        index=self.hashkey%self.table_size
        unit=self.hash_table[index]
        if unit.depth==-1 or unit.key!=self.hashkey or unit.depth<=depth:
            return None
        return unit

    def __RecordHash(self,depth,lower,upper,extra):
        '''record deeper situation to the hash table'''
        index=self.hashkey%self.table_size
        if self.hash_table[index].depth>=depth:
           return
        self.hash_table[index].key=self.hashkey
        self.hash_table[index].depth=depth
        self.hash_table[index].upper=upper
        self.hash_table[index].lower=lower
        self.hash_table[index].move=extra

    
