# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 23:40:00 2018

@author: z
"""
import numpy as np
import random

def create_board():
    board = np.zeros((3,3))
    return board

def place(board, player, position):
    (x,y) = position
    if board[x,y] == 0 :
        board[x,y] = player
    elif board[x,y] > 0 :
        return 1
    return 0

def possibilities(board):
    posb = []
    (x,y) = np.where(board == 0)
    for i in range(len(x)):
        tposb = (x[i],y[i])
        posb.append(tposb)
    return tuple(posb)

def random_place(board, player):
    posb = possibilities(board)
    (x,y) = random.choice(posb)
    board[x,y] = player
    return

def row_win(board, player):
    (x,y) = np.where(board == player)
    x = list(x)
    for i in range(max(x)+1):
        if x.count(i) == 3:
            return True
    return False

def col_win(board, player):
    (x,y) = np.where(board == player)
    y = list(y)
    for i in range(max(y)+1):
        if y.count(i) == 3:
            return True
    return False

def diag_win(board, player):
    (x,y) = np.where(board == player)
    f = 0
    for i in range(len(x)):
        if y[i] == x[i]:
            f = f + 1
    if f == 3:
        return True
    f = 0
    for i in range(len(x)):
        if y[i] + x[i] == 2:
            f = f + 1
    if f == 3:
        return True
    return False
    
def evaluate(board):
    winner = 0
    for player in [1, 2]:
        # Check if `row_win`, `col_win`, or `diag_win` apply. 
        # If so, store `player` as `winner`.
        if row_win(board,player) or col_win(board,player) or diag_win(board,player):
            winner = player
    if np.all(board != 0) and winner == 0:
        winner = -1
    return winner

def play_game():
    b,state = create_board(),0
    players = [1,2]
    while state == 0 :
        for player in players:
            random_place(b,player)
            state = evaluate(b)
            if state != 0:
                break
    return state
                

print(play_game())
        