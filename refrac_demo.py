import world
import color
import transformation as transform
import base
import shapes
import camera
import ppm
import patterns
import light

import math

def make_planes():
    vertical = shapes.plane()
    vertical.transform = transform.rotation_x(math.pi/2)
    vertical.material.transparency = 1
    vertical.material.reflectivity = 1
    vertical.material.refractive_index = 1.5
    vertical.material.color = color.color(.5, .5, .5)
    vertical.material.diffuse = 0.1
    vertical.material.specular = 1
    vertical.material.shininess = 300

    horizontal = shapes.plane()
    horizontal.material.reflectivity = 1
    horizontal.material.color = color.color(.5, .5, .5)

    return horizontal, vertical


def make_spheres():
    back = shapes.glass_sphere()
    back.transform = transform.translation(0, 1, -2)

    front = shapes.sphere()
    front.transform = transform.translation(0, 1, 2)

    return front, back



def main():
    planes = make_planes()
    spheres = make_spheres()

    wrld = world.world()
    wrld.light_source = light.point_light(base.point(-10, 10, 10), color.color(1, 1, 1))
    wrld.add_objs(*(planes + spheres))

    cam = camera.camera(600, 300, math.pi/2)
    cam.transform = transform.view_transform(
            base.point(-1, 3, 3),
            base.point(0, 1, 0),
            base.vector(0, 1, 0)
            )

    print('[*] Generating canvas ...')
    canv = camera.render(cam, wrld, progress_bar=True, desc="rendering")
    print("[*] Generating ppm data ...")
    ppm_data = ppm.canvas_to_ppm(canv)
    write_to_file(ppm_data, "refrac_demo.ppm")
    print('[*] Done')

def write_to_file(ppm_data, filename):
    try:
        print(f"[*] Writing ppm data to file {filename}")
        open(filename, "w").write(ppm_data)
        print(f"[+] Successfully written ppm data to file {filename}")
    except Exception as ex:
        print(f"[-] Error: {ex}")


if __name__ == '__main__':
    main()
