"""
The module to make Knight moves on the Chess board till all cells are covered and count the moves

The entities:
- board: an array NxN (by_default ) 
- init_post: the initial position and logic of movement
- Chess_game: the main class, defined by the board size and the initial position of the Knight
- move_otion: 8 ways to change the position according to the game rules.
"""

import numpy as np
import random as rd

 #constants
BOARD_SIZE = 8

class Chess_game:
    def __init__(self, knight_pos=[0,0]):
        self.init_pos = knight_pos
        self.b_size = BOARD_SIZE
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=np.int8)
        self.board[self.init_pos[0],self.init_pos[1]]=1
        self.move_option = [
            (2,1),
            (-2,1),
            (2,-1),
            (-2,-1),
            (1,2),
            (-1,2), 
            (1,-2),
            (-1,-2)
            ]
        self.move_count = 0

def update_init(game: Chess_game, new_pos):
    """Updates the initial position of the Knight"""
    game.board[game.init_pos[0],game.init_pos[1]] = 0
    game.board[new_pos[0],new_pos[1]] = 1
    game.init_pos = new_pos[:]

def board_reset(game: Chess_game):
    """Reset the board to initial position"""
    game.board.fill(0)
    game.board[game.init_pos[0],game.init_pos[1]] = 1

def make_move_reg(game: Chess_game, cur_pos):
    """The function makes a random possible move and returns a new position"""
    new_pos = [8,8]
    while (new_pos[0]>game.b_size-1) or (new_pos[1]>game.b_size-1) or (new_pos[0]<0) or (new_pos[1]<0):  
        direction_num = rd.randint(0,7)
        move_option = game.move_option[direction_num]
        new_pos[0] = cur_pos[0] + move_option[0]
        new_pos[1] = cur_pos[1] + move_option[1]

    return new_pos

def make_move_opt(game: Chess_game, cur_pos):
    """The function makes a random OPTIMAL possible move and returns a new position
    The idea of the optimal move is not to repeat a move to a previously visited cell
    So we use game.board
    But there is a risk to get to a DEADEND with no option, so we need to control with using a buffer"""
    move_possibility = False

    #buffer to collect the possible moves
    pos_buffer = []

    new_pos=cur_pos[:]
    #print(f"Current buffer: {pos_buffer}")
    #print(f"current pos: {cur_pos}")
    #iterate while the move is not possible and board cell was visited
    for direction_num in range(0,8): 
        move_option_x,move_option_y  = game.move_option[direction_num]
        new_pos[0] = cur_pos[0] + move_option_x
        new_pos[1] = cur_pos[1] + move_option_y
        #print(new_pos)
        move_possibility = ((new_pos[0]<game.b_size) and (new_pos[1]<game.b_size) and (new_pos[0]>=0) and (new_pos[1]>=0))
        #print(f"possible: {move_possibility}") 
        if move_possibility==True: 
            #print(f"I add a point {new_pos}, visited: {game.board[new_pos[0],new_pos[1]]}")
            #WOW-WOW! you can not just append a hole list pos_buffer.append(new_pos) 
            #because it will add the pointer to the list and all elements will be equal. 
            pos_buffer.append([new_pos[0],new_pos[1]])
            #print(f"Current buffer: {pos_buffer}") 
            if game.board[new_pos[0],new_pos[1]] == 0:
                return new_pos
    #print(f"Final buffer: {pos_buffer}")  
    return rd.choice(pos_buffer)


def knight_trip(game: Chess_game, make_move_strategy):
    """The function returns the amount of moves to cover all the cells of the board
    The purpose of the function is to make the entire trip of knight moves 
    till all the cells are covered.
        -----------
    On each move we repeat the pattern 
    while there are any not visited cell on the board:
    - choose a random move 
    - check if the move is possible, if not try one more till possible (done in the helper function)
    - update the current position and update the board cell status as visited
    - increment the counter

    Helper function make_move is used check if the random move is possible and update position
    """
    #init the counter of the moves
    count = 0
    #calculate the total area to control when we finish to visit every cell
    board_area = game.b_size * game.b_size
    #get current position
    cur_pos = game.init_pos[:]
    
    #start tripping xo-xo-xo
    while game.board.sum() < board_area:
        #a decoration implemented here to have the possibility to use different move strategy
        cur_pos = make_move_strategy(game,cur_pos)
        try:
            game.board[cur_pos[0],cur_pos[1]]=1
        except ValueError:
            print(f"The position: {cur_pos}")
        count += 1

    return count 



