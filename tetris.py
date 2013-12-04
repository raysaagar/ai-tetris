# Author: adhit
# https://github.com/adhit/tetris/blob/master/tetris.py
# Modified version removes music

import os,sys
import random
import math

from colorama import init, Fore
init()

#define colors
RED=255,0,64
ORANGE=255,64,0
YELLOW=191,255,0
GREEN=64,255,0
BLUE=0,64,255
CYAN=0,255,255
PURPLE=191,0,255
PINK=255,0,191
WHITE=255,255,255
BLACK=0,0,0
BG_COLOR=204,255,255
GUI_COLOR=224,224,224
LINE_COLOR=BLACK

#define measures
HEIGHT,WIDTH=400,200
HALF_WIDTH=10
FULL_WIDTH=2*HALF_WIDTH
LINE_WIDTH=2
MID_X=WIDTH/2
PREVIEW_POS=[(WIDTH+7*FULL_WIDTH,3*FULL_WIDTH),(WIDTH+12*FULL_WIDTH,3*FULL_WIDTH),(WIDTH+17*FULL_WIDTH,3*FULL_WIDTH)]
SAVED_POS=(WIDTH+7*FULL_WIDTH,9*FULL_WIDTH)

"""
Added by Louis
Pretty print tetris
"""

# Map the RGB colors to terminal colors
# Arbitrary assignments. Find more color codes if they conflict, I'm not sure
# if colors are duplicated
TERM_COLORS = {
    RED: Fore.RED,
    ORANGE: Fore.MAGENTA,
    YELLOW: Fore.YELLOW,
    GREEN: Fore.GREEN,
    BLUE: Fore.BLUE,
    CYAN: Fore.CYAN,
    PURPLE: Fore.BLUE,
    WHITE: Fore.WHITE
        }

#timing things
last_move=0
last_rotate=0

class Square():
    def __init__(self,color,pos):
        self.color=color
        self.x=pos[0]
        self.y=pos[1]

    def __repr__(self):
        """
        Added by Louis. For printing ASCII squares
        """

        return TERM_COLORS[self.color] + "#" + Fore.RESET
        
    def move_up(self):
        self.y=self.y-FULL_WIDTH
    def move_down(self):
        self.y=self.y+FULL_WIDTH
    def move_left(self):
        self.x=self.x-FULL_WIDTH
    def move_right(self):
        self.x=self.x+FULL_WIDTH
    def rotate_CW(self):
        temp=self.x
        self.x=-self.y
        self.y=temp
    def rotate_CCW(self):
        temp=self.x
        self.x=self.y
        self.y=-temp
    def draw(self):
        corners=[]
        corners.append((self.x-HALF_WIDTH,self.y-HALF_WIDTH))
        corners.append((self.x+HALF_WIDTH,self.y-HALF_WIDTH))
        corners.append((self.x+HALF_WIDTH,self.y+HALF_WIDTH))
        corners.append((self.x-HALF_WIDTH,self.y+HALF_WIDTH))
        screen.lock()
        screen.unlock()
    def draw_moved(self,dx,dy):
        x=self.x+dx
        y=self.y+dy
        corners=[]
        corners.append((x-HALF_WIDTH,y-HALF_WIDTH))
        corners.append((x+HALF_WIDTH,y-HALF_WIDTH))
        corners.append((x+HALF_WIDTH,y+HALF_WIDTH))
        corners.append((x-HALF_WIDTH,y+HALF_WIDTH))
        screen.lock()
        screen.unlock()

# Added by Louis
LINE_SHAPE = 0
T_SHAPE = 1
SQUARE_SHAPE = 2
INVERT_Z_SHAPE = 3
Z_SHAPE = 4
INVERT_L_SHAPE = 5
L_SHAPE = 6

SHAPES = [LINE_SHAPE, T_SHAPE, SQUARE_SHAPE, INVERT_Z_SHAPE, Z_SHAPE, INVERT_L_SHAPE, L_SHAPE]

class Block():
    def __init__(self,type):
#type=0
        self.type=type
        self.squares=[]
        if(type==0): #4 squares vertical
            self.color=CYAN
            self.y=0
            self.x=MID_X
            self.squares.append(Square(self.color,(self.x-3*HALF_WIDTH,self.y-HALF_WIDTH)))
            self.squares.append(Square(self.color,(self.x-HALF_WIDTH,self.y-HALF_WIDTH)))
            self.squares.append(Square(self.color,(self.x+HALF_WIDTH,self.y-HALF_WIDTH)))
            self.squares.append(Square(self.color,(self.x+3*HALF_WIDTH,self.y-HALF_WIDTH)))
        elif(type==1): #T
            self.color=PURPLE
            self.y=-HALF_WIDTH
            self.x=3*HALF_WIDTH
            self.squares.append(Square(self.color,(self.x,self.y-FULL_WIDTH)))
            self.squares.append(Square(self.color,(self.x-FULL_WIDTH,self.y)))
            self.squares.append(Square(self.color,(self.x,self.y)))
            self.squares.append(Square(self.color,(self.x+FULL_WIDTH,self.y)))
        elif(type==2): #square squares
            self.color=YELLOW
            self.y=-FULL_WIDTH
            self.x=MID_X
            self.squares.append(Square(self.color,(self.x-HALF_WIDTH,self.y-HALF_WIDTH)))
            self.squares.append(Square(self.color,(self.x+HALF_WIDTH,self.y-HALF_WIDTH)))
            self.squares.append(Square(self.color,(self.x+HALF_WIDTH,self.y+HALF_WIDTH)))
            self.squares.append(Square(self.color,(self.x-HALF_WIDTH,self.y+HALF_WIDTH)))
        elif(type==3): #inversed z
            self.color=GREEN
            self.y=-HALF_WIDTH
            self.x=3*HALF_WIDTH
            self.squares.append(Square(self.color,(self.x-FULL_WIDTH,self.y)))
            self.squares.append(Square(self.color,(self.x,self.y)))
            self.squares.append(Square(self.color,(self.x,self.y-FULL_WIDTH)))
            self.squares.append(Square(self.color,(self.x+FULL_WIDTH,self.y-FULL_WIDTH)))
        elif(type==4): #z
            self.color=RED
            self.y=-HALF_WIDTH
            self.x=3*HALF_WIDTH
            self.squares.append(Square(self.color,(self.x+FULL_WIDTH,self.y)))
            self.squares.append(Square(self.color,(self.x,self.y)))
            self.squares.append(Square(self.color,(self.x,self.y-FULL_WIDTH)))
            self.squares.append(Square(self.color,(self.x-FULL_WIDTH,self.y-FULL_WIDTH)))
        elif(type==5): #inversed L
            self.color=BLUE
            self.y=-HALF_WIDTH
            self.x=3*HALF_WIDTH
            self.squares.append(Square(self.color,(self.x-FULL_WIDTH,self.y-FULL_WIDTH)))
            self.squares.append(Square(self.color,(self.x-FULL_WIDTH,self.y)))
            self.squares.append(Square(self.color,(self.x,self.y)))
            self.squares.append(Square(self.color,(self.x+FULL_WIDTH,self.y)))
        elif(type==6): #L
            self.color=ORANGE
            self.y=-HALF_WIDTH
            self.x=3*HALF_WIDTH
            self.squares.append(Square(self.color,(self.x-FULL_WIDTH,self.y)))
            self.squares.append(Square(self.color,(self.x,self.y)))
            self.squares.append(Square(self.color,(self.x+FULL_WIDTH,self.y)))
            self.squares.append(Square(self.color,(self.x+FULL_WIDTH,self.y-FULL_WIDTH)))
    def move_up(self,grid):
        if(not self.can_move(0,-1,grid)): return False
        self.y-=FULL_WIDTH
        for square in self.squares:
            square.move_up()
        return True

    def move_down(self,grid):
        if(not self.can_move(0,1,grid)): return False
        self.y+=FULL_WIDTH
        for square in self.squares:
            square.move_down()
        return True
    def move_left(self,grid):
        if(not self.can_move(-1,0,grid)): return False
        self.x-=FULL_WIDTH
        for square in self.squares:
            square.move_left()
        return True

    def move_right(self,grid):
        if(not self.can_move(1,0,grid)): return False
        self.x+=FULL_WIDTH
        for square in self.squares:
            square.move_right()
        return True

    def draw(self):
        for square in self.squares:
            square.draw()
    def draw_moved(self,dx,dy):
        for square in self.squares:
            square.draw_moved(dx,dy)
    def rotate_CW(self,grid):
        if(not self.can_CW(grid)):
            return
        for square in self.squares:
            square.x-=self.x
            square.y-=self.y
            square.rotate_CW()
            square.x+=self.x
            square.y+=self.y
    def rotate_CCW(self,grid):
        if(not self.can_CCW(grid)): return
        for square in self.squares:
            square.x-=self.x
            square.y-=self.y
            square.rotate_CCW()
            square.x+=self.x
            square.y+=self.y
    def can_move(self,dx,dy,grid):
        for square in self.squares:
            x=(square.x/FULL_WIDTH)+dx
            y=(square.y/FULL_WIDTH)+dy
            if(y>=20 or x<0 or x>=10 or (y>=0 and grid[y][x] is not None)):
                return False
        return True
    def can_CW(self,grid):
        for square in self.squares:
            x=square.x-self.x
            y=square.y-self.y
            temp=x
            x=-y
            y=temp
            x=(x+self.x)/FULL_WIDTH
            y=(y+self.y)/FULL_WIDTH
            if(y>=20 or x<0 or x>=10 or (y>=0 and grid[y][x] is not None)): return False
        return True
    def can_CCW(self,grid):
        for square in self.squares:
            x=square.x-self.x
            y=square.y-self.y
            temp=x
            x=y
            y=-temp
            x=(x+self.x)/FULL_WIDTH
            y=(y+self.y)/FULL_WIDTH
            if(y>=20 or x<0 or x>=10 or (y>=0 and grid[y][x] is not None)): return False
        return True 

