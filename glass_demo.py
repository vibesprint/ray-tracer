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
    s2.transform = transform.translation(.7, 0, 0)

    return csg.csg('union', s1, s2)

def make_planes():
    wall = shapes.plane();
    wall.material.color = color.color(.6, .7, .8)
    wall.transform = transform.compose(
            transform.rotation_x(math.pi/2)
            )

    floor = shapes.plane()
    floor.material.color = color.color(.5, .6, .7)

    return wall, floor


def main():
    obj = make_csg()
    planes = make_planes()
    wrld = world.world()
    wrld.add_objs(obj, *planes)
    wrld.light_source = light.point_light(
            base.point(-10, 10, -10),
            color.color(1, 1, 1)
            )

    cam = camera.camera(300, 150, math.pi/2)
    cam.transform = transform.view_transform(
            base.point(0, 2, -3.5),
            base.point(0, .5, 0),
            base.vector(0, 1, 0)
            )

    print('[*] Rendering canvas ...')
    canv = camera.render(cam, wrld, progress_bar=True, desc="rendering")
    print('[*] Generating ppm data ...')
    ppm_data = ppm.canvas_to_ppm(canv)
    write_to_file(ppm_data, "glass_demo.ppm")
    print('[+] DONE')

def write_to_file(ppm_data, filename):
    try:
        print(f"[*] Writing image to file {filename} ...")
        open(filename, "w").write(ppm_data)
    except Exception as ex:
        print(f"[-] Error: {ex}")



if __name__ == '__main__':
    main()
