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


def _worker(cam, wrld, row, cols, outqueue):
    print(f"Started as worker: {mp.current_process()}")
    for x in range(cols):
        r = ray_for_pixel(cam, x, row)
        col = world.color_at(wrld, r)
        outqueue.put((x, row, col))


def render(cam, wrld, *, progress_bar=False, **opts):
    img = canvas.canvas(cam.hsize, cam.vsize)

    manager = mp.Manager()
    outqueue = manager.Queue()

    with mp.Pool(mp.cpu_count()) as pool:
        # print(f"Starting workers ...")
        results = []
        for i in range(cam.vsize):
            results.append(pool.apply_async(_worker, args=(cam, wrld, i, cam.hsize, outqueue)))


        # print(f"No. of processes: {len(procs)}")

        if progress_bar:
            opts.update({'unit': "row"})
            row_range = tqdm(range(cam.vsize), **opts)
        else:
            row_range = range(cam.vsize)

        # print(f"Waiting for completed works ...")
        for i in row_range:
            # print(f"Waiting for pixel {i}")
            for _ in range(cam.hsize):
                x, y, col = outqueue.get()
                canvas.write_pixel(img, x, y, col)

        pool.close()
        pool.join()


    return img
