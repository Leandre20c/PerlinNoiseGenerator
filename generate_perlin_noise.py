import random
import math
from image_utils import *

def create_gradient_grid(grid_width, grid_height):
    """Crée une grille de vecteurs gradients aléatoires"""
    grid = []
    for y in range(grid_height):
        row = []
        for x in range(grid_width):
            # Angle aléatoire
            angle = random.random() * 2 * math.pi
            # Convertir en vecteur (x, y)
            gradient = (math.cos(angle), math.sin(angle))
            row.append(gradient)
        grid.append(row)
    return grid

def dot_grid_gradient(grid, grid_corner_x, grid_corner_y, pixel_grid_x, pixel_grid_y):
    """
    grid_corner_x, grid_corner_y: indices du coin dans la grille (entiers)
    pixel_grid_x, pixel_grid_y: position du pixel en coordonnées de grille (floats)
    """
    # Vecteur du coin vers le pixel
    dx = pixel_grid_x - grid_corner_x
    dy = pixel_grid_y - grid_corner_y
    
    # Gradient du coin
    gradient = grid[grid_corner_y][grid_corner_x]
    
    # Produit scalaire
    return dx * gradient[0] + dy * gradient[1]


def normalize_value(val, min_val=-1, max_val=1):
    new_min = 0
    new_max = 255

    old_range = (max_val - min_val)  
    new_range = (new_max - new_min)  
    new_value = int((((val - min_val) * new_range) / old_range) + new_min)
    
    return new_value


def smoothstep(w):
    if (w <= 0.0):
        return 0.0
    
    if (w >= 1.0):
        return 1.0
    
    return w * w * (3.0 - 2.0 * w)

# Fonction d'interpolation lisse entre a0 et a1
# Le poids w doit être dans l'intervalle [0.0, 1.0]
def interpolate(a0, a1, w):
    return a0 + (a1 - a0) * smoothstep(w)
    

def generate_noise(width, height, grid_size):
    """
    width, height: taille de l'image en pixels
    grid_size: taille d'une cellule de grille (ex: 32 = grille plus espacée)
    """
    image = create_image(width, height)
    
    # Calculer combien de points de grille on a besoin
    grid_width = width // grid_size + 2
    grid_height = height // grid_size + 2
    grid = create_gradient_grid(grid_width, grid_height)
    
    # Pour chaque pixel
    for pixel_y in range(height):
        for pixel_x in range(width):
            # 1. Trouver dans quelle cellule on est
            grid_x = pixel_x / grid_size  # Position en coord de grille (float)
            grid_y = pixel_y / grid_size
            
            # 2. Les 4 coins de la cellule
            x0 = int(grid_x)      # Coin gauche
            y0 = int(grid_y)      # Coin haut
            x1 = x0 + 1           # Coin droit
            y1 = y0 + 1           # Coin bas
            
            # 3. Calculer les 4 produits scalaires
            dot_tl = dot_grid_gradient(grid, x0, y0, grid_x, grid_y)  # top-left
            dot_tr = dot_grid_gradient(grid, x1, y0, grid_x, grid_y)  # top-right
            dot_bl = dot_grid_gradient(grid, x0, y1, grid_x, grid_y)  # bottom-left
            dot_br = dot_grid_gradient(grid, x1, y1, grid_x, grid_y)  # bottom-right
            
            # 5. Interpoler les 4 valeurs
            # Poids pour l'interpolation
            # (On pourrait utiliser des polynômes d'ordre supérieur ou d'autres fonctions lisses)
            sx = grid_x - x0
            sy = grid_y - y0
     
            # Interpolation horizontale
            ix0 = interpolate(dot_tl, dot_tr, sx)
            ix1 = interpolate(dot_bl, dot_br, sx)
                        
            val = interpolate(ix0, ix1, sy)
            
            # 6. Normaliser de [-1,1] vers [0,255]
            noise = normalize_value(val, -1, 1)
            
            set_pixel(image, width, pixel_x, pixel_y, noise)
    
    return image


if __name__ == "__main__":
    # Test
    x = 128
    y = 128
    
    noise_img = generate_noise(x, y, 8)
    save_png(noise_img, x, y, "output")
                
