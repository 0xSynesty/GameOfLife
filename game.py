from core import computeNextFrame
from patterns import insertPattern, animationQuiClaque
from game_constants import *

import sys
import pygame as PG
import numpy as np


PG.init()

# Taille de la fenêtre par défaut
size = width, height = 1024, 576
screen = PG.display.set_mode(size, PG.RESIZABLE) # L'utilisateur peut redimensionner la fenêtre
PG.display.set_caption('Conway\'s Game Of Life')

# Positions des images de l'écran d'accueil du jeu
logo = PG.transform.scale(PG.image.load('logo.png'), (400, 200)).convert_alpha()
logo_rect = logo.get_rect()
logo_rect.center = width // 2, height // 2.5

start_button = PG.transform.scale(PG.image.load('start_button.png'), (173, 67)).convert_alpha()
start_button_rect = start_button.get_rect()
start_button_rect.center = width // 2, height // 1.3

keybinds_banner = PG.image.load('keybinds_banner.png').convert_alpha()
keybinds_banner_rect = keybinds_banner.get_rect(topleft=(0,0))
keybinds_banner_rect.topleft = width * 0.02, height * 0.02

# Maximum de carrés possibles pour la résolution par défaut
max_rects = (width // (cell_width + cells_margin), height // (cell_height + cells_margin))

# Initialisation de la matrice du jeu de la vie
binary_grid = np.zeros(max_rects)


# Crée un objet Clock qui permettra plus tard de régler les FPS max du jeu
clock = PG.time.Clock()


# Permet de mettre la simulation en pause
hold = False


# Permet d'afficher l'écran d'accueil du jeu
started = False

while 1:
    for event in PG.event.get():
        if event.type == PG.QUIT: sys.exit()

        # Actions réalisées lorsque l'utilisateur appuie sur une touche
        elif event.type == PG.KEYDOWN:

            if event.key == PG.K_SPACE:
                binary_grid = computeNextFrame(binary_grid)
                hold = False

            elif event.key == PG.K_ESCAPE:
                hold = False
                started = False
                binary_grid = np.zeros(max_rects)

            elif (event.key == PG.K_BACKSPACE) & started:
                hold = True
                binary_grid = np.zeros(max_rects)

            # Prend une touche qui existe dans patterns.py pour insérer un pattern à l'endroit où se trouve la souris
            elif (PG.key.name(event.key) in pattern_keys) & started:
                mouse_pos = PG.mouse.get_pos()
                binary_grid = insertPattern(binary_grid, pattern_keys[PG.key.name(event.key)], mouse_pos)

        # Lorsque l'utilisateur clique
        elif event.type == PG.MOUSEBUTTONDOWN:

            mouseX, mouseY = PG.mouse.get_pos()

            #Position de la cellule cliquée
            column = mouseX // (cells_margin + cell_width)
            row = mouseY// (cells_margin + cell_height)

            if not started:
                # Le bouton start permet de lancer le jeu
                if start_button_rect.collidepoint(mouseX, mouseY): 
                    started = True
                    binary_grid = np.zeros(max_rects)

            # Change les cellules cliquées
            else:
                if binary_grid[column, row] == 0:
                    binary_grid[column, row] = 1
                else:
                    binary_grid[column, row] = 0

        # Redimensionnement de la grille si l'utilisateur redimensionne la fenêtre
        elif event.type == PG.VIDEORESIZE:
            
            # On prend la resolution actuelle de l'écran pour dessiner nos carrés
            res = PG.display.get_surface().get_width(), PG.display.get_surface().get_height()
            width, height = res

            # Positions des images de l'écran d'accueil
            logo_rect.center = width // 2, height // 2.5
            start_button_rect.center = width // 2, height // 1.3
            keybinds_banner_rect.topleft = width * 0.02, height * 0.02

            # Nombre maximum de rectangles pouvant être crées avec la taille de fenêtre donnée
            max_rects = (width // (cell_width + cells_margin), height // (cell_height + cells_margin))
            binary_grid = np.zeros(max_rects)

    # Lance la simulation
    if not hold:
        binary_grid = computeNextFrame(binary_grid)

    screen.fill(GREY)

    # On stop la simulation s'il n'y a plus de celulle vivante
    if (1 not in binary_grid) & started: hold = True
    

    #Création des cellules
    for i in range(binary_grid.shape[0]):
        for j in range(binary_grid.shape[1]):
            if binary_grid[i][j] == 0:
                color = WHITE
            else:
                color = BLACK
            
            PG.draw.rect(screen, color, 
            [cells_margin + (cell_width + cells_margin) * i, 
            cells_margin + (cells_margin  + cell_height) * j, 
            cell_width, cell_height])

    # Menu d'accueil du jeu
    if not started:
        screen.blit(logo, logo_rect)
        screen.blit(start_button, start_button_rect)
        screen.blit(keybinds_banner, keybinds_banner_rect)


        # Animation du logo
        logo_rect.centery += delta_logo
        
        if logo_rect.centery <= height // 2.6:
            delta_logo = 1

        elif logo_rect.centery >= height // 2.5:
            delta_logo = -1

        binary_grid = animationQuiClaque(binary_grid)

    # On actualise l'écran du jeu
    PG.display.flip()

    # Cap des FPS
    if (not hold) & started: clock.tick(FPS_started)
    elif not started: clock.tick(FPS_menu)
    else: clock.tick(FPS_draw)