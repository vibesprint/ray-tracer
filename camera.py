import base
import matrix
import ray
import canvas
import color
import world

import math
from tqdm import tqdm
import multiprocessing as mp


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
    blocks = divide(cam.hsize, cam.vsize, mp.cpu_count())

    # print("No. of blocks: ", blocks)


    with mp.Pool(processes=mp.cpu_count()) as pool:
        # args = [(cam, wrld, hrange, vrange, img, queue) for hrange, vrange in blocks]
        queue = mp.Queue()
        args = [(cam, wrld, row, cam.hsize, img, queue) for row in range(cam.vsize)]

        results = [ pool.apply_async(_render, arg) for arg in args ]
        # results = pool.imap(_render, args)

        # print(f"No. of processes: {len(procs)}")
        # for proc in procs:
        #     proc.start()

        # for _ in tqdm(range(cam.vsize * cam.hsize)):
        #     queue.get()

        print(f"No. of cells expected: {cam.hsize * cam.vsize}")
        if progress_bar:
            pixel_range = tqdm(range(cam.hsize*cam.vsize), **opts)
        else:
            pixel_range = range(cam.hsize * cam.vsize)

        for i in pixel_range:
            print(f"Waiting for pixel: {i}")
            x, y, col = queue.get()
            print(f"Coordinates: {x}, {y}")
            canvas.write_pixel(img, x, y, col)

        pool.join()

    # for proc in procs:
    #     proc.join()

    return img



def _render(cam, wrld, row, cols, img, queue):

    print(f"Started render function: {mp.current_process()}")
    for y in range(cols):
        r = ray_for_pixel(cam, y, row)
        col = world.color_at(wrld, r)
        queue.put((y, row, col))


def divide(width, height, count):
    block_width = width // count
    block_height = height // count

    if block_width == 0 or block_height == 0:
        return [(range(width), range(height))]

    result = []

    cur_w = 0
    while cur_w < width:
        cur_h = 0
        while cur_h < height:
            result.append((range(cur_w, cur_w + block_width), range(cur_h, cur_h + block_height)))
            cur_h += block_height
        cur_w += block_width

    return result
