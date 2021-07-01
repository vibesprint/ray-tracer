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


def _worker(cam, wrld, inqueue, outqueue):
    print(f"Started as worker: {mp.current_process()}")
    for x, y in iter(inqueue.get, "STOP"):
        r = ray_for_pixel(cam, x, y)
        col = world.color_at(wrld, r)
        outqueue.put((x, y, col))


def render(cam, wrld, *, progress_bar=False, **opts):
    img = canvas.canvas(cam.hsize, cam.vsize)

    inqueue = mp.Queue()
    outqueue = mp.Queue()

    # print(f"Starting workers ...")
    procs = [mp.Process(target=_worker, args=(cam, wrld, inqueue, outqueue)) for _ in range(mp.cpu_count())]

    # print(f"No. of processes: {len(procs)}")

    # print(f"Starting processes ...")
    for p in procs:
        p.start()

    # print(f"Distributing work ...")
    for y in range(cam.vsize):
        for x in range(cam.hsize):
            inqueue.put((x, y))

    # print(f"Putting stop marker ...")
    for i in range(mp.cpu_count()+10):
        inqueue.put("STOP")

    if progress_bar:
        opts.update({'unit': "pixel"})
        pixel_range = tqdm(range(cam.vsize*cam.hsize), **opts)
    else:
        pixel_range = range(cam.vsize*cam.hsize)

    # print(f"Waiting for completed works ...")
    for i in pixel_range:
        # print(f"Waiting for pixel {i}")
        x, y, col = outqueue.get()
        canvas.write_pixel(img, x, y, col)

    # print(f"Joining the processes ...")
    for p in procs:
        p.join()

    return img
