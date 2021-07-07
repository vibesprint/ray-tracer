import color
import base
import ray
import transformation as transform
import shapes
import light
import world
import camera
import ppm
import utils

import math


def make_walls():
    wall = shapes.plane()
    wall.material.color = color.color(1, 1, 1)
    wall.transform = transform.rotation_x(math.pi/2)

    right_wall = shapes.plane()
    right_wall.material.color = color.color(1, 1, 1)
    right_wall.transform = transform.compose(
            transform.rotation_x(math.pi/2),
            transform.rotation_y(math.pi/2)
            )

    floor = shapes.plane()
    floor.material.color = color.color(1, 1, 1)

    return [wall, right_wall, floor]

def make_cylinders():
    cyl = shapes.cylinder()
    cyl.closed = True
    cyl.maximum = 1
    cyl.minimum = 0
    cyl.material.color = color.color(1, 1, 1)
    cyl.transform = transform.translation(-.5, 0, -.8)

    return [cyl]


def main():
    walls = make_walls()
    cyls = make_cylinders()

    wrld = world.world()
    wrld.add_objs(*walls, *cyls)
    wrld.light_source = light.point_light(
            base.point(-10, 5, -10),
            color.color(1, 1, 1)
            )

    cam = camera.camera(600, 300, math.pi/3)
    cam.transform = transform.view_transform(
            base.point(-1, 3, -2),
            base.point(0, 1, 0),
            base.vector(0, 1, 0)
            )

    print('[*] Rendering canvas ...')
    canv = camera.render(cam, wrld, progress_bar=True, desc="rendering")
    print('[*] Generating ppm data ...')
    ppm_data = ppm.canvas_to_ppm(canv)
    write_to_file(ppm_data, "cylinder_demo.ppm")
    print('[+] DONE')

def write_to_file(ppm_data, filename):
    try:
        print(f"[*] Writing image to file {filename} ...")
        open(filename, "w").write(ppm_data)
    except Exception as ex:
        print(f"[-] Error: {ex}")



if __name__ == '__main__':
    main()
