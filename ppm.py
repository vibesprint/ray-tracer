import canvas
import color

import math

MAX_COLOR_VALUE = 255

def make_header(canv, max_color):
    return """P3\n{} {}\n{}\n""".format(canvas.width(canv), canvas.height(canv), max_color)


def scale(col, factor):
    scaled = color.color(
            math.ceil(color.red(col) * factor),
            math.ceil(color.green(col) * factor),
            math.ceil(color.blue(col) * factor)
            )
    return clamp_color(scaled, low=0, high=MAX_COLOR_VALUE)

def clamp_color(col, *, low, high):
    red = clamp(color.red(col), low, high)
    green = clamp(color.green(col), low, high)
    blue = clamp(color.blue(col), low, high)
    return color.color(red, green, blue)

def clamp(val, low, high):
    if val < low:
        return low
    elif val > high:
        return high
    return val


def canvas_to_ppm(canv):
    header = make_header(canv, MAX_COLOR_VALUE);
    fixed_liner = FixedLiner(70)
    for row in canv:
        for pixel in row:
            scaled_pix = scale(pixel, MAX_COLOR_VALUE)
            fixed_liner.add(str(color.red(scaled_pix)))
            fixed_liner.add(str(color.green(scaled_pix)))
            fixed_liner.add(str(color.blue(scaled_pix)))

        fixed_liner.new_row()

    return header + str(fixed_liner)


class FixedLiner:
    def __init__(self, max_width):
        self._width = max_width
        self._cur_len = 0
        self._data = ""

    def add(self, obj):
        if self._cur_len + len(obj) >= self._width:
            self._data = self._data + '\n'
            self._cur_len = 0

        if self._cur_len == 0:
            self._data += obj
        else:
            self._data = self._data + ' ' + obj
            # Account for ' '
            self._cur_len += 1

        self._cur_len += len(obj)

    def new_row(self):
        self._data = self._data + '\n'
        self._cur_len = 0

    def __str__(self):
        return self._data + '\n'
