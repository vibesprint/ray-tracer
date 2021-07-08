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

import math


def hexagon_corner():
    corner = shapes.sphere()
    corner.transform = transform.compose(
            transform.translation(0, 0, -1),
            transform.scale(0.25, 0.25, 0.25)
            )

    return corner

def hexagon_edge():
    edge = shapes.cylinder()
    edge.minimum = 0
    edge.maximum = 1
    edge.transform = transform.compose(
            transform.translation(0, 0, -1),
            transform.rotation_y(-math.pi/6),
            transform.rotation_z(-math.pi/2),
            transform.scale(.25, 1, .25)
            )

    return edge


def hexagon_side():
    side = group.group()
    side.add_child(hexagon_corner())
    side.add_child(hexagon_edge())

    return side


def hexagon():
    hxgn = group.group()

    for i in range(6):
        side = hexagon_side()
        side.transform = transform.rotation_y(i * math.pi/3)
        hxgn.add_child(side)

    return hxgn


def main():
    wrld = world.world()
    wrld.add_objs(hexagon())
    wrld.light_source = light.point_light(
            base.point(-10, 10, -10),
            color.color(1, 1, 1)
            )

    cam = camera.camera(600, 300, math.pi/2)
    cam.transform = transform.view_transform(
            base.point(-1, 3, -5),
            base.point(0, 1, 0),
            base.vector(0, 1, 0)
            )

    print('[*] Rendering canvas ...')
    canv = camera.render(cam, wrld, progress_bar=True, desc="rendering")
    print('[*] Generating ppm data ...')
    ppm_data = ppm.canvas_to_ppm(canv)
    write_to_file(ppm_data, "group_demo.ppm")
    print('[+] DONE')

def write_to_file(ppm_data, filename):
    try:
        print(f"[*] Writing image to file {filename} ...")
        open(filename, "w").write(ppm_data)
    except Exception as ex:
        print(f"[-] Error: {ex}")



if __name__ == '__main__':
    main()
