"""
---------------------------------
Naughts & Crosses based on MENACE
--------------------------------
"""
print '==========================================='
print '==== Naughts & Crosses based on MENACE ===='
print '= Note: 1s are naughts and 2s are crosses ='
print '==========================================='
# -----------------
# Import modules
# -----------------
import numpy as np
import random
import math
import time
import matplotlib.pyplot as plt

# -----------------
# Inputs
# -----------------
reward_win = 1
reward_draw = 0
reward_lose = -1
print 'Beginer = 50 '
print 'Novice  = 150'
print 'Expert  = 500'
iterations = int(raw_input('Enter the number of iterations: '))
print_games = False
print_mode = False

print '---------'
print 'menace.py'
print '---------'
print 'Reward win: %s' % reward_win
print 'Reward draw: %s' % reward_draw
print 'Reward lose: %s' % reward_lose
print 'Number of iterations: %s' % iterations

# Memory of player 1
memory_boards_A = []
memory_weights_A = []

# Memory of player 2
memory_boards_B = []
memory_weights_B = []

# Set up the results graph
graph_win = []
graph_lose = []
graph_draw = []
status_counts = [0,0,0] # Win, Lose, Draw

def print_weights(boards,weights_a):
    for i in range(len(boards)):
        print 'Board layout | Weights A (%s)' % i
        print boards[i][0:3], "|" , weights_a[i][0:3]
        print boards[i][3:6], "|" , weights_a[i][3:6]
        print boards[i][6:9], "|" , weights_a[i][6:9]

def make_graph(win,lose,draw):    
    plt.plot(win, 'r-', label='Win')
    plt.plot(lose, 'b-', label='Lose')
    plt.plot(draw, 'g-', label='Draw')    
    plt.ylabel('Result')
    plt.xlabel('Iterations')
    title = plt.title('Cumulative results for Player 1')
    legend = plt.legend(loc='lower right', shadow=False)
    plt.show()        
        
def memory_check(game_board,mem_boards,mem_weights):
    opt = []
    opt_weights = []
    f_opt = []
    
    # Find the possible moves
    opt = [i for i, x in enumerate(game_board) if x == 0]
    
    # Find the maximum out of the possible moves
    if game_board in mem_boards:
        opt_weights = []
        pos = mem_boards.index(game_board)
        for p in opt:
            opt_weights.append(mem_weights[pos][p])
        m = max(opt_weights)
        
        for p in range(len(opt)):
            ind = opt[p]
            if m == mem_weights[pos][ind]:
                f_opt.append(opt[p])
        opt = f_opt
        
    move = random.choice(opt)
    return move

def make_move(game_board,player,move,temp_memory_boards,temp_memory_moves):
    # Make the move
    game_board[move] = player
    
    # Temporarily record the move and board
    temp_game_board = [0,0,0,0,0,0,0,0,0]
    for i in range(len(game_board)):
        temp_game_board[i] = game_board[i]
    temp_move = [0,0,0,0,0,0,0,0,0]
    temp_move[move] = 1
    temp_memory_boards.append(temp_game_board)
    temp_memory_moves.append(temp_move)
    
    # Print the move
    if print_mode == True:
        print game_board[0:3]
        print game_board[3:6]
        print game_board[6:9]
        print '-----------------'

def assign_weights(status,temp_memory_boards,temp_memory_moves):
    for i in range(len(temp_memory_boards)):   
        
        # Setting the reward values    
        if status == 1:
            reward_a = reward_win
            reward_b = reward_lose
        elif status == 2:
            reward_a = reward_lose
            reward_b = reward_win
        else:
            reward_a = reward_draw
            reward_b = reward_draw
        
        weight_a = [0,0,0,0,0,0,0,0,0]
        weight_b = [0,0,0,0,0,0,0,0,0]
        for u in range(len(temp_memory_moves[i])):
            weight_a[u] = temp_memory_moves[i][u] * reward_a
            weight_b[u] = temp_memory_moves[i][u] * reward_b
        
        # Remove the move from the board position
        index = temp_memory_moves[i].index(1)
        temp_memory_boards[i][index] = 0
        
        # Save the weights in memory_boards_A
        # -----------------------------------
        if temp_memory_boards[i] in memory_boards_A:
            # Find the position of the match
            pos = memory_boards_A.index(temp_memory_boards[i])
            if len(memory_weights_A[pos]) == 0:
                memory_weights_A[pos] = [0,0,0,0,0,0,0,0,0]
            if i % 2 == 0:
                memory_weights_A[pos] = [x + y for x, y in zip(memory_weights_A[pos], weight_a)]
        else:
            if i % 2 == 0:
                memory_boards_A.append(temp_memory_boards[i])
                memory_weights_A.append(weight_a)
                
        # Save the weights in memory_boards_B
        # -----------------------------------
        if temp_memory_boards[i] in memory_boards_B:
            # Find the position of the match
            pos = memory_boards_B.index(temp_memory_boards[i])
            if len(memory_weights_B[pos]) == 0:
                memory_weights_B[pos] = [0,0,0,0,0,0,0,0,0]
            if i % 2 != 0:
                memory_weights_B[pos] = [x + y for x, y in zip(memory_weights_B[pos], weight_b)]
        else:
            if i % 2 != 0:
                memory_boards_B.append(temp_memory_boards[i])
                memory_weights_B.append(weight_b)
        
def win_check(game_board):
    # Check if a player has won or the game has drawn
    b = game_board
    if b[0] == b[1] == b[2] and b[0] != 0:
        game = b[0]
    elif b[3] == b[4] == b[5] and b[3] != 0:
        game = b[3]
    elif b[6] == b[7] == b[8] and b[6] != 0:
        game = b[6]
    elif b[0] == b[3] == b[6] and b[0] != 0:
        game = b[0]
    elif b[1] == b[4] == b[7] and b[1] != 0:
        game = b[1]
    elif b[2] == b[5] == b[8] and b[2] != 0:
        game = b[2]
    elif b[2] == b[4] == b[6] and b[2] != 0:
        game = b[2]
    elif b[0] == b[4] == b[8] and b[0] != 0:
        game = b[0]
    elif 0 not in b:
        game = 0
    else:
        game = 'on'
        
    if game != 'on' and game != 0 and print_mode == True:
        print 'Game won by player: %s' % game
    elif game == 0 and print_mode == True:
        print 'The game was drawn'
        
    # Save the game for the graph
    if game != 'on' and game == 1:
        int_win = 1
        int_lose = 0
        int_draw = 0
    elif game != 'on' and game == 2:
        int_win = 0
        int_lose = 1
        int_draw = 0
    else:
        int_win = 0
        int_lose = 0
        int_draw = 1
    
    if game != 'on':
        status_counts[0] += int_win
        status_counts[1] += int_lose
        status_counts[2] += int_draw
        graph_win.append(status_counts[0])
        graph_lose.append(status_counts[1])
        graph_draw.append(status_counts[2])
        
    return game
    
def training(iterations):
    for i in range(0,iterations):
        if print_games == True:
            print 'Game: %s' % i
        game_board = [0,0,0,0,0,0,0,0,0]
        temp_memory_boards = []
        temp_memory_moves = []
        game = "on"
        while game == 'on':
            # Player 1 turn:
            # --------------
            move = memory_check(game_board,memory_boards_A,memory_weights_A)
            make_move(game_board,1,move,temp_memory_boards,temp_memory_moves)
            game = win_check(game_board)
            if game == 'on':
                # Player 2 turn:
                # --------------
                move = memory_check(game_board,memory_boards_B,memory_weights_B)
                make_move(game_board,2,move,temp_memory_boards,temp_memory_moves)
                game = win_check(game_board)
        assign_weights(game,temp_memory_boards,temp_memory_moves)
            
        if print_mode == True and iterations > 1:
            print ' ----------------- Next Game ----------------- '

def game():
    game_board = [0,0,0,0,0,0,0,0,0]
    temp_memory_boards = []
    temp_memory_moves = []
    game = "on"
    while game == 'on':        
        # Player 1 turn:
        # --------------
        move = memory_check(game_board,memory_boards_A,memory_weights_A)
        make_move(game_board,1,move,temp_memory_boards,temp_memory_moves)
        game = win_check(game_board)
        print game_board[0:3]
        print game_board[3:6]
        print game_board[6:9]
        print '-----------------'
        if game == 'on':
            move = int(raw_input('Where would you like to go (1 - 9): '))
            move = move - 1;
            game_board[move] = 2
            game = win_check(game_board)
    if game == 1:
        print 'The computer won the game'
    elif game == 2:
        print 'You won the game'
    else:
        print 'It was a draw'
    assign_weights(game,temp_memory_boards,temp_memory_moves)
    print 'Type \'game()\' to start a new game'
            
# ------------------       
# Executing the code
# ------------------
training(iterations)
print '- Training complete -'
ans1 = raw_input('Plot a graph of training? (y/n) ')
if ans1 == 'y':
    make_graph(graph_win, graph_lose, graph_draw)
print '-------------------------------------------------'
print '        Starting computer vs. human game'
print '-------------------------------------------------'
print 'Notes:'
print 'You can overwrite the computers moves but don\'t'
print 'The computer will learn from the games'
print 'Select your move with the number keys'
print '-------------------------------------------------'
game()
