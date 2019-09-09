'''
Pacman Game 
Matteo Carretta
Student Code: 265826
'''
import pygame
from arena import *
from pacman import *
from pacman_map import *

arena = PacManArena(232, 280)


for x, y, w, h in walls_pos:
    Wall(arena, x, y, w, h)
for x, y in cookies_pos:
    Cookie(arena, x, y)
for x, y in powers_pos:
    Power(arena, x, y)
##
corner = [(0, 0),           #corner (x,y) to which each ghost will
          (232, 0),
          (232, 256),
          (0, 256)]
ghost_symbol = [(0), (1), (2), (3)]

pacman = PacMan(arena, 112, 184)
Ghost(arena, 112, 88, corner[0], ghost_symbol[0])
Ghost(arena, 112, 88, corner[1], ghost_symbol[1])
Ghost(arena, 112, 88, corner[2], ghost_symbol[2])
Ghost(arena, 112, 88, corner[3], ghost_symbol[3])

number_of_players = int(input('Insert number of players (1/2): '))
if number_of_players == 2:
    multiplayer = True
    paclady = PacMan(arena, 106, 184)
else:
    multiplayer = False

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(arena.size())
background = pygame.image.load('pacman_background.png')
sprites = pygame.image.load('pacman_sprites.png')

playing = True
win, lost = False, False

while playing and not win and not lost:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            playing = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP:
                pacman.go_up()
            elif e.key == pygame.K_DOWN:
                pacman.go_down()
            elif e.key == pygame.K_LEFT:
                pacman.go_left()
            elif e.key == pygame.K_RIGHT:
                pacman.go_right()
            if multiplayer:
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_w:
                        paclady.go_up()
                    elif e.key == pygame.K_s:
                        paclady.go_down()
                    elif e.key == pygame.K_a:
                        paclady.go_left()
                    elif e.key == pygame.K_d:
                        paclady.go_right()
    
        
    arena.move_all()  # Game logic

    screen.blit(background, (0, 0))
    for a in arena.actors():
        if not isinstance(a, Wall):
            x, y, w, h = a.rect()
            xs, ys = a.symbol()
            screen.blit(sprites, (x, y), area=(xs, ys, w, h))
    
    pygame.display.flip()
    clock.tick(30)
    
pygame.quit()

if win:
    print('You won!')
if lost:
    print('Game Over!')
    
    

