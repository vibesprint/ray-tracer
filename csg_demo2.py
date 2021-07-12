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
import group
import csg
import patterns

import math


def make_csg():
    s1 = shapes.glass_sphere()
    s2 = shapes.glass_sphere()
    s1.material.color = color.color(1, 0, 0)
    s2.material.color = color.color(0, 0, 1)
    s2.transform = transform.translation(.7, 0, 0)

    c = csg.csg('union', s1, s2)
    c.transform = transform.translation(0, 1, -1)

    return c

def make_planes():
    floor = shapes.plane()
    floor.material.pattern = patterns.checkers_pattern(
            color.color(1, 1, 1),
            color.color(.1, .1, .1)
            )

    wall = shapes.plane()
    wall.material.pattern = floor.material.pattern
    wall.transform = transform.rotation_x(math.pi/2)

    return floor, wall


def main():
    obj = make_csg()
    wrld = world.world()
    walls = make_planes()
    wrld.add_objs(obj)
    wrld.add_objs(*walls)
    wrld.light_source = light.point_light(
            base.point(-10, 10, -10),
            color.color(1, 1, 1)
            )

    cam = camera.camera(600, 300, math.pi/2)
    cam.transform = transform.view_transform(
            base.point(0, 2, -4),
            base.point(0, .5, 0),
            base.vector(0, 1, 0)
            )

    print('[*] Rendering canvas ...')
    canv = camera.render(cam, wrld, progress_bar=True, desc="rendering")
    print('[*] Generating ppm data ...')
    ppm_data = ppm.canvas_to_ppm(canv)
    write_to_file(ppm_data, "csg_demo2.ppm")
    print('[+] DONE')

def write_to_file(ppm_data, filename):
    try:
        print(f"[*] Writing image to file {filename} ...")
        open(filename, "w").write(ppm_data)
    except Exception as ex:
        print(f"[-] Error: {ex}")



if __name__ == '__main__':
    main()
