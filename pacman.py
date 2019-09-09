'''
Pacman Game Emulation
Matteo Carretta
Student Code: 265826
'''
from random import choice
from arena import *
from math import sqrt


class PacManArena(Arena):
    #Define if Actor is goin to the wall at the next step or not
    def going_to_wall(self, actor: Actor, dx: int, dy: int) -> bool: 
        x, y, w, h = actor.rect()
        return self.rect_in_wall((x + dx, y + dy, w, h))

    #Define if the rect containing the actors collide with the wall
    def rect_in_wall(self, rect: (int, int, int, int)) -> bool:
        for other in self.actors():
            if isinstance(other, Wall):
                x1, y1, w1, h1 = rect
                x2, y2, w2, h2 = other.rect()
                if (y2 < y1 + h1 and y1 < y2 + h2 and
                    x2 < x1 + w1 and x1 < x2 + w2):
                    return True
            else:
                return False
    
    
    

class Wall(Actor):  

    def __init__(self, arena, x: int, y: int, width: int, height: int):
        self._x, self._y = x, y
        self._width, self._height = width, height
        self._arena = arena
        arena.add(self)

    def move(self):
        pass

    def collide(self, other):
        pass

    def rect(self) -> (int, int, int, int):
        return self._x, self._y, self._width, self._height

    def symbol(self):
        pass


class Cookie(Actor):  
    W, H = 4, 4

    def __init__(self, arena, x: int, y: int):
        self._x, self._y = x, y
        self._arena = arena
        arena.add(self)
        
    def move(self):
        pass
    
    def rect(self) -> (int, int, int, int):
        return self._x, self._y, Cookie.W, Cookie.H

    def collide(self, other):
        if isinstance(other, PacMan):
            self._arena.remove(self)
            
        
    def symbol(self):
        return 166, 54


class Power(Actor):  # ...
    W, H = 8, 8
    def __init__(self, arena, x: int, y: int): 
        self._x = x
        self._y = y
        self._arena = arena 
        arena.add(self)

    def move(self):
        pass

    def collide(self, other):
        if isinstance(other, PacMan):
            self._arena.remove(self)
            
        
    def rect(self) -> (int, int, int, int):
        return self._x, self._y, Power.W, Power.H
    
    def symbol(self):
        return 180, 52


class Ghost(Actor): 
    W, H = 16, 16
    SPEED = 2
    SYMBOL = [[(0, 64), (32, 64), (64, 64), (96, 64)],
              [(0, 80), (32, 80), (64, 80), (96, 80)],
              [(0, 96), (32, 96), (64, 96), (96, 96)],
              [(0, 112), (32, 112), (64, 112), (96, 112)]]
    
    SCATTER_CONST = 270
    CHASE_CONST = 390
    
    def __init__(self, arena, x: int, y: int, corner_coord: int, color: int):
        self._x, self._y = x, y
        self._dx, self._dy = 1, 1
        self._corner_x, self._corner_y = corner_coord #corner (x,y) to which ghosts will get close to
        self._scatter, self._chase = Ghost.SCATTER_CONST, Ghost.CHASE_CONST
        self._move_mode = True #True: Scatter mode, False: Chaser mode
        self._color = color
        self._eaten = 0
        self._arena = arena
        arena.add(self)

    def collide(self, other):
        pass

    def frightened(self): #Ghost move randomly if PacMan has recently eaten the power coockie
        
        ghost_moves = [(0, -self.SPEED),
                        (self.SPEED, 0),
                        (0, self.SPEED),
                        (-self.SPEED, 0)]
        if self._x % 8 == 0 and self._y % 8 == 0:
            rand_dx, rand_dy = choice(ghost_moves)
            
            while PacManArena.going_to_wall(self._arena, self, rand_dx, rand_dy) or (rand_dx == - self._dx and rand_dy == - self._dy):
                rand_dx, rand_dy = choice(ghost_moves)
            self._dx, self._dy = rand_dx, rand_dy
                                                                   
        
    def approach(self, point_x: int, point_y: int):
        ghost_moves = [(0, -self.SPEED),
                        (self.SPEED, 0),
                        (0, self.SPEED),
                        (-self.SPEED, 0)]
        move_dx = []
        move_dy = []
        distance = []
        if self._x % 8 == 0 and self._y % 8 == 0:
             for i in ghost_moves:
                dx, dy = i
                new_x = self._x + dx
                new_y = self._y + dy
                dist_new_x = sqrt((new_x - point_x)**2 + (new_y - point_y)**2)
                if (not PacManArena.going_to_wall(self._arena, self, dx, dy)) and  (dx != -self._dx or dy != -self._dy):
                    move_dx.append(dx)
                    move_dy.append(dy)
                    distance.append(dist_new_x)
             dist_min = distance[0]
             for count in range(len(distance)):
                 if distance[count] <= dist_min:
                     self._dx, self._dy = move_dx[count], move_dy[count]
                     
    def scatter(self): #each ghost chooses a corner to go near to
        self.approach(self._corner_x, self._corner_y)
        
      
    def chase(self):
        pacman_pos_x, pacman_pos_y, pacman_w, pacman_h = PacMan.rect(self)
        
        self.approach(pacman_pos_x, pacman_pos_y)
        
        

    def move(self):
        ARENA_W, ARENA_H = self._arena.size()
        for other in self._arena.actors():
            if isinstance(other, PacMan):
                if other.check_power():
                    self.frightened()
                elif self._move_mode:
                    self.scatter()
                    if self._scatter > 0:
                        self._scatter -= 1
                    else:
                        self._scatter = Ghost.SCATTER_CONST
                        self._move_mode = False
                else:
                    self.chase()
                    if self._chase > 0:
                        self._chase -= 1
                    else:
                        self._chase = Ghost.CHASE_CONST
                        self._move_mode = True
            
        self._x = (self._x + self._dx) % ARENA_W
        self._y += self._dy                         
   
    def rect(self) -> (int, int, int, int):
        return self._x, self._y, Ghost.W, Ghost.H
    
    def symbol(self):
        for other in self._arena.actors():
            if isinstance(other, PacMan):
                if other.check_power():
                    symbol = (128, 64)
                elif self._dx == 0 and self._dy == 0:
                    symbol = Ghost.SYMBOL[self._color][0]
                elif self._dx > 0:
                    symbol = Ghost.SYMBOL[self._color][0]
                elif self._dx < 0:
                    symbol = Ghost.SYMBOL[self._color][1]
                elif self._dy < 0:
                    symbol = Ghost.SYMBOL[self._color][2]
                elif self._dy > 0:
                    symbol = Ghost.SYMBOL[self._color][3]
        return symbol


class PacMan(Actor):  
    W, H = 16, 16
    SPEED = 2
    STARTING_LIVES = 2
    POWER_CONST = 180
    STARTING_POS_X, STARTING_POS_Y = 112, 184
    SYMBOL = [[(0, 0), (16, 0), (32, 0)],
              [(0, 16), (16, 16), (32, 0)],
              [(0, 32), (16, 32), (32, 0)],
              [(0, 48), (16, 48), (32, 0)]]
    
    def __init__(self, arena, x: int, y: int):
        self._x, self._y = x, y
        self._dx, self._dy = 0, 0
        self._next_dx, self._next_dy = 0, 0
        self._power = 0
        self._arena = arena
        self._lives = PacMan.STARTING_LIVES
        self._symbol_count = 0
        arena.add(self)

    def check_power(self):
        if self._power > 0:
            return True
        else:
            return False

    def move(self):
        ARENA_W, ARENA_H = self._arena.size()
        if not PacManArena.going_to_wall(self._arena, self, self._next_dx, self._next_dy): #if not going to wall, then move!
            self._dx, self._dy = self._next_dx, self._next_dy
            self._y += self._dy
            self._x = (self._x + self._dx) % ARENA_W                #check if PacMan has gone through the "tunnel"
        elif not PacManArena.going_to_wall(self._arena, self, self._dx, self._dy):
            self._y += self._dy
            self._x = (self._x + self._dx) % ARENA_W
        if self.check_power():
            self._power -= 1
            
   
   
    def collide(self, other):
        if isinstance(other, Power):
            self._power = PacMan.POWER_CONST
        if isinstance(other, Ghost) and not self.check_power():
            if self._lives > 0:
                self._lives -= 1
                self._x, self._y = PacMan.STARTING_POS_X, PacMan.STARTING_POS_Y
            else:
                self._arena.remove(self)
        elif isinstance(other, Ghost) and self.check_power():
            self._arena.remove(other)
                                
                
    
    def go_left(self):
        self._next_dx, self._next_dy = -PacMan.SPEED, 0            
                
    def go_right(self):
        self._next_dx, self._next_dy = +PacMan.SPEED, 0        

    def go_up(self):
        self._next_dx, self._next_dy = 0, -PacMan.SPEED
              
    def go_down(self):
        self._next_dx, self._next_dy = 0, +PacMan.SPEED
           
    def rect(self) -> (int, int, int, int):
        return self._x, self._y, PacMan.W, PacMan.H

    def symbol(self):
        if self._dx == 0 and self._dy == 0:
            symbol = 0, 0
        elif self._dx > 0:
            symbol = PacMan.SYMBOL[0][self._symbol_count]
        elif self._dx < 0:
            symbol = PacMan.SYMBOL[1][self._symbol_count]
        elif self._dy < 0:
            symbol = PacMan.SYMBOL[2][self._symbol_count]
        elif self._dy > 0:
            symbol = PacMan.SYMBOL[3][self._symbol_count]
        self._symbol_count += 1
        if self._symbol_count == 3:
            self._symbol_count = 0
        return symbol

