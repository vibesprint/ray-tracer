import base
import matrix
import ray
import canvas
import color
import world

import math
from tqdm import tqdm


class camera:
    def __init__(self, hsize, vsize, field_of_view):
        self.hsize = hsize
        self.vsize = vsize
        self.field_of_view = field_of_view
        self.transform = matrix.identity_matrix()
        self._calc_pixel_size()

    def _calc_pixel_size(self):
        half_view = math.tan(self.field_of_view/2)
        aspect = self.hsize / self.vsize

        if aspect >= 1:
            self.half_width = half_view
            self.half_height = half_view / aspect
        else:
            self.half_width = half_view * aspect
            self.half_height = half_view

        self.pixel_size = (self.half_width * 2) / self.hsize


def ray_for_pixel(cam, px, py):
    xoffset = (px + 0.5) * cam.pixel_size
    yoffset = (py + 0.5) * cam.pixel_size

    world_x = cam.half_width - xoffset
    world_y = cam.half_height - yoffset

    pixel = matrix.mul(
               matrix.inverse(cam.transform),
               base.point(world_x, world_y, -1)
               )

    origin = matrix.mul(
            matrix.inverse(cam.transform),
            base.point(0, 0, 0)
            )
    direction = base.normalize(base.sub(pixel, origin))
    return ray.ray(origin, direction)


def render(cam, wrld, *, progress_bar=False, **opts):
    img = canvas.canvas(cam.hsize, cam.vsize)
    if progress_bar:
        vrange = tqdm(range(cam.vsize), **opts)
    else:
        vrange = range(cam.vsize)

    for y in vrange:
        for x in range(cam.hsize):
            r = ray_for_pixel(cam, x, y)
            col = world.color_at(wrld, r)
            canvas.write_pixel(img, x, y, col)
    return img
