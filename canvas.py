import color


def canvas(width, height):
    canv = []
    for i in range(height):
        row = list()
        for j in range(width):
            row.append(color.color(0, 0, 0))
        canv.append(row)
    return canv

def pixel_at(canv, width, height):
    return canv[height][width]


def width(c):
    return len(c[0])

def height(c):
    return len(c)


def write_pixel(c, width, height, col):
    c[height][width] = col
