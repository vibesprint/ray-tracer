import camera
import world
import shapes
import color
import light
import base
import transformation as transform
import ppm
import patterns

import math


def make_walls():
    plane = shapes.plane()
    plane.material.color = color.color(1, 0.9, 0.9)
    plane.material.specular = 0
    plane.material.pattern = patterns.checkers_pattern(
            color.color(0.9, 0.75, 0.8),
            color.color(0.9, 0.9, 0.9)
            )

    plane.material.pattern.transform = transform.rotation_y(math.pi/3)
    plane.material.reflective = 0.7

    return (plane, )


def make_spheres():
    middle = shapes.sphere()
    middle.transform = transform.compose(
            transform.translation(-0.5, 1, 0.5)
            )

    middle.material.color = color.color(0.1, 1, 0.5)
    middle.material.diffuse = 0.7
    middle.material.specular = 0.3
    middle.material.pattern = patterns.ring_pattern(
            color.color(0.9, 0.75, 0.8),
            color.color(0.9, 0.9, 0.9)
            )
    middle.material.pattern.transform = transform.rotation_z(math.pi/3)

    right = shapes.sphere()
    right.transform = transform.compose(
            transform.translation(1.5, 0.5, -0.5),
            transform.scale(0.5, 0.5, 0.5)
            )
    right.material.color = color.color(0.5, 1, 0.1)
    right.material.diffuse = 0.7
    right.material.specular = 0.3
    right.material.pattern = middle.material.pattern

    left = shapes.sphere()
    left.transform = transform.compose(
            transform.translation(-1.5, 0.33, -0.75),
            transform.scale(0.33, 0.33, 0.33)
            )
    left.material.color = color.color(1, 0.8, 0.1)
    left.material.diffuse = 0.7
    left.material.specular = 0.3
    left.material.pattern = right.material.pattern

    return left, middle, right


def main():
    walls = make_walls()
    spheres = make_spheres()

    wrld = world.world()
    wrld.light_source = light.point_light(base.point(-10, 10, -10), color.color(1, 1, 1))
    wrld.add_objs(*(walls + spheres))

    cam = camera.camera(600, 300, math.pi/3)
    cam.transform = transform.view_transform(
            base.point(0, 1.5, -5),
            base.point(0, 1, 0),
            base.vector(0, 1, 0)
            )


    print("[*] Generating canvas ...")
    canv = camera.render(cam, wrld, progress_bar=True, unit="row", desc="rendering")
    print("[*] Generating the ppm data ...")
    ppm_data = ppm.canvas_to_ppm(canv)
    write_to_file(ppm_data, "pattern_demo4.ppm")
    print("[+] Done")


def write_to_file(ppm_data, filename):
    try:
        print(f"[*] Writing the ppm_data to the file {filename}")
        open(filename, 'w').write(ppm_data)
    except Exception as ex:
        print(f"[-] Error occured: {ex}")
    else:
        print(f"[+] File successfully written to {filename}")

if __name__ == '__main__':
    main()
