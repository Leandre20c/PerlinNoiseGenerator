import matplotlib.pyplot as plt
import numpy as np
from generate_perlin_noise import *

if __name__ == "__main__":
    noise = perlin_noise_simple(256, 256, scale=20)
    noise = (noise - noise.min()) / (noise.max() - noise.min())  # Normaliser 0-1
    noise = (noise * 255).astype(np.uint8)  # Convertir en image

    plt.imshow(noise, cmap='gray')
    plt.show()