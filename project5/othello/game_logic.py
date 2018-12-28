class GameState:
    def __init__(self,rows,columns,first_turn,deter,board_list):
        self.board = board_list
        self.width = columns
        self.height = rows
        self.deter = deter              
        self.turn = first_turn
        self.winner = "NONE"
        self.steps = 0

    def prop(self): ###check the current status of the game
        print("self.board=\n",
              self.board,
              "\nself.width=",
              self.width,
              "\nself.height=\n",
              self.height,
              "\nself.deter=\n",
              self.deter,
              "\nself.turn=\n",
              self.turn,
              "\nself.winner=\n",
              self.winner,
              "\nself.steps=\n",
              self.steps
              )
        
    def __repr__(self):
        
        print_list = []

        for row in self.board:
            print_row = " ".join(row)
            print_list.append(print_row)

        print_str = "B: {}  W: {}\n".format(GameState.count_pieces(self,"B"),GameState.count_pieces(self,"W"))
        print_str += "\n".join(print_list)
        if GameState.game_end(self):
            print_str += "\nWINNER: {}".format(str(self.winner))
        elif not GameState.game_end(self):
            print_str += "\nTURN: {}".format(self.turn)
            
        return print_str

    def move(self,move_position:(int,int),color): ###othello move
        
        move_row,move_column = move_position[0]-1,move_position[1]-1
        try_dir = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        oppo_color = "B" if color == "W" else "W"

        if GameState._valid_move(self,move_position,color):

            impact_directions = GameState._piece_impact_directions(self,move_position,color)

            for impact_dir in impact_directions:
                d_row,d_column = try_dir[impact_dir]
                i = 0
                while True:
                    i += 1
                    if self.height >move_row + i*d_row >= 0 and self.width> move_column + i*d_column >= 0:
                        if self.board[move_row + i*d_row][move_column + i*d_column] == oppo_color:
                            self.board[move_row + i*d_row][move_column + i*d_column] = color
                        elif self.board[move_row + i*d_row][move_column + i*d_column] == color:
                            break
                        
            self.board[move_row][move_column] = color
            self.steps += 1
            
            if GameState._valid_positions(self,oppo_color) != []:
                self.turn = oppo_color

            elif GameState._valid_positions(self,oppo_color) == [] and GameState._valid_positions(self,color) == []:
                pass
            GameState.game_end(self)
                        
        return self

    def game_end(self): ###check if the game ends
        
        color = self.turn
        oppo_color = "B" if self.turn == "W" else "W"
        
        if GameState._valid_positions(self,color) == [] and GameState._valid_positions(self,oppo_color) != []:
            self.turn = oppo_color
            return False
        elif GameState._valid_positions(self,oppo_color) == [] and GameState._valid_positions(self,color) == []:
            self.winner = GameState.winner(self)
            return True
        else:
            return False
        
    def valid_move_deter(self,move_position): ###determain if the move is valid or not
        valid_positions = GameState._valid_positions(self,self.turn)

        if move_position in valid_positions:
            return True
        elif move_position not in valid_positions:
            return False
        

    def winner(self): ###determain the winner

        B_count = GameState.count_pieces(self,"B")
        W_count = GameState.count_pieces(self,"W")
        
        if self.deter == ">":
            winner = "B" if B_count > W_count else "W"
        elif self.deter == "<":
            winner = "B" if B_count < W_count else "W"
        if B_count == W_count:
            return "NONE"

        return winner

    def count_pieces(self,color): ###count the pieces of chess on the board
        pieces = 0
        for row in self.board:
            for chess_piece in row:
                if chess_piece == color:
                    pieces += 1
        return pieces
    
    def _valid_positions(self,color): ###return all valid positions for the color on the board
        valid_positions = []
        for i in range(self.height):
            for j in range(self.width):
                
                move_position = (i+1,j+1)

                if GameState._valid_move(self,move_position,color):
                    valid_positions.append(move_position)
                    
        return valid_positions
    
    def _piece_impact_directions(self,move_position:(int,int),color):###this function return the directions of the pieces' color will be changed after the intended move

        move_row,move_column = move_position[0]-1,move_position[1]-1
        try_dir = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        oppo_color = "B" if color == "W" else "W"

        valid_dir_index = GameState._around_others(self,move_position,color)
        
        change_directions = []
        for valid_dir in valid_dir_index:
            d_row,d_column = try_dir[valid_dir]
            
            i = 0
            while True:
                i += 1

                if self.height >move_row + i*d_row >= 0 and self.width> move_column + i*d_column >= 0:
                    if self.board[move_row + i*d_row][move_column + i*d_column] == ".":
                        break

                    if self.board[move_row + i*d_row][move_column + i*d_column] == color and i>1:
                        change_directions.append(valid_dir)
                        break
                else:

                    break
                
        return change_directions              
        
    def _valid_move(self,move_position:(int,int),color):###this function checks if the move is a valid move

        move_row,move_column = move_position[0]-1,move_position[1]-1
        try_dir = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        oppo_color = "B" if color == "W" else "W"
        
        valid_dir_index = GameState._around_others(self,move_position,color)

        if valid_dir_index == []:
            return False

        for valid_dir in valid_dir_index:
            d_row,d_column = try_dir[valid_dir]
            i = 0
            while True:
                i += 1
                if self.height > move_row + i*d_row >= 0 and self.width> move_column + i*d_column >= 0:
                    if self.board[move_row + i*d_row][move_column + i*d_column] == color and i>1:
                        return True
                    elif self.board[move_row + i*d_row][move_column + i*d_column] == oppo_color:
                        pass
                    elif self.board[move_row + i*d_row][move_column + i*d_column] == ".":
                        break
                else:
                    break
        
        return False     

    def _around_others(self,move_position:(int,int),color) ->list:###this function checks if there's any opposite-color chess around the intended move
        
        move_row,move_column = move_position[0]-1,move_position[1]-1
        try_dir = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        oppo_color = "B" if color == "W" else "W"
        
        move_position = self.board[move_row][move_column]
        if move_position != ".":
            return []
        
        valid_directions = []
        for i in range(8):
            d_row,d_column = try_dir[i]
            around_row,around_column = move_row+d_row,move_column+d_column
            if self.width-1 >= around_column >= 0 and self.height-1 >= around_row >= 0:
                try:
                    valid_directions.append(self.board[move_row+d_row][move_column+d_column])
                except IndexError:
                    valid_directions.append(None)
            else:
                valid_directions.append(None)

######    index of directions
######           0 1 2
######           3   4
######           5 6 7
        
        valid_dir_index = []

        for i in range(len(valid_directions)):
            if valid_directions[i] == oppo_color:
                valid_dir_index.append(i)
        return valid_dir_index

