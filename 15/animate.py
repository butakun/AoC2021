import numpy as np
import argparse
from PIL import Image, ImageDraw, ImageFont


def main(grid_filename, g_filename, prev_filename, visited_filename):

    grid = np.load(open(grid_filename, "rb"))
    prev = np.load(open(prev_filename, "rb"))
    G = np.load(open(g_filename, "rb"))
    with open(visited_filename) as f:
        visited = []
        for line in f:
            _, i, j = line.strip().split()
            visited.append((i, j))

    idim, jdim = G.shape

    font = ImageFont.load_default()
    dx, dy = font.getsize("W")
    d = max(dx, dy)
    print(d, d)
    img_bg = Image.new(mode="RGBA", size=(d * jdim, d * idim))

    img = img_bg.copy()
    draw = ImageDraw.Draw(img)
    for i in range(idim):
        for j in range(jdim):
            g = grid[i, j]
            draw.text((j * d, i * d), str(g), font=font)
    img.convert("RGB").save(open("anim.jpg", "wb"))



if __name__ == "__main__":
    main("grid.npy", "G.npy", "prev.npy", "visited.txt")
