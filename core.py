import numpy as np

def computeNumNeighbours(pFrame, index_line, index_col):
    """
    Calcule et retourne le nombre de voisins vivants de chaque cellule.

    - pFrame = padded frame qui correspond à la grille du jeu avec une bordure de 1 pixel virtuel
    - index_line, index_col = indexs de la cellule dont on veut calculer les voisins
    """

    x, y = index_line -1, index_col-1
    
    countAlive = 0

    # On scanne une grille 3x3 autour de la cellule donnée
    for l in range(3):
        for c in range(3):
            countAlive += 1 if pFrame[x+l][y+c] == 1 else 0
    
    # On enlève 1 au compteur si la cellule principale est vivante pour qu'elle ne compte pas
    countAlive -= 1 if pFrame[index_line][index_col] == 1 else 0

    return countAlive


def computeNextFrame(frame):
    """
    Vérifie pour chaque cellule de la grille si elle sera créée, 
    tuée ou laissée en vie selon les règles du jeu de la vie.

    - frame = grille du jeu
    """

    # On ajoute une bordure de 1 pixel virtuel autour de la matrice pour éviter les problèmes de calculs
    pFrame = np.pad(frame, 1, mode='constant')

    for l in range(pFrame.shape[0]-2):
        for c in range(pFrame.shape[1]-2):

            currentCell = pFrame[l+1][c+1] # Coordonnées de la cellule traitée

            countAlive = computeNumNeighbours(pFrame, l+1, c+1)

            # Règles du jeu de la vie
            if (countAlive == 3) and (currentCell == 0):
                frame[l][c] = 1
            elif (currentCell == 1) and (countAlive == 2 or countAlive == 3):
                frame[l][c] = 1
            else: 
                frame[l][c] = 0

    return frame









