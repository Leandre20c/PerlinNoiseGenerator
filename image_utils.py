#########################
###### IMAGE UTILS ######
#########################
# From claude & Leandre #
# 1D list -> efficiency #
#########################


def create_image(width, height):
    """Image = liste plate, on calcule l'index"""
    return [0] * (width * height)

def set_pixel(image, width, x, y, value):
    image[y * width + x] = value

def get_pixel(image, width, x, y):
    return image[y * width + x]

def save_ppm(image, width, height, filename):
    """Sauvegarde en format PPM binaire (P6)"""
    # Ajouter l'extension .ppm si pas présente
    if not filename.endswith('.ppm'):
        filename += '.ppm'
    
    with open(filename, 'wb') as f:  # Mode binaire 'wb'
        # Header en ASCII
        header = f'P6\n{width} {height}\n255\n'
        f.write(header.encode('ascii'))
        
        # Pixels en binaire
        for y in range(height):
            for x in range(width):
                val = int(get_pixel(image, width, x, y))
                # Clamper entre 0-255
                val = max(0, min(255, val))
                # RGB (3 bytes identiques pour du gris)
                f.write(bytes([val, val, val]))
                

from PIL import Image

def save_png(image, width, height, filename):
    if not filename.endswith('.png'):
        filename += '.png'
    
    # Créer une image PIL
    img_data = []
    for y in range(height):
        for x in range(width):
            val = int(get_pixel(image, width, x, y))
            val = max(0, min(255, val))
            img_data.append(val)
    
    img = Image.new('L', (width, height))  # 'L' = grayscale
    img.putdata(img_data)
    img.save(filename)