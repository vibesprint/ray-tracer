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
import random


def make_walls():
    plane = shapes.plane()
    plane.material.color = color.color(1, 0.9, 0.9)
    plane.material.specular = 0
    plane.material.pattern = random_pattern()

    return (plane, )




def make_spheres(n=100):
    spheres = [None]*n

    for i in range(n):
        sph = shapes.sphere()
        sph.transform = random_transform()
        sph.material.color = random_color()
        sph.material.pattern = random_pattern()
        sph.material.diffuse = 0.7
        sph.material.specular = 0.3
        spheres[i] = sph

    return tuple(spheres)

def random_transform():
    translation = transform.translation(
            random.choice([1, -1]) * random.random() * random.randint(1, 100),
            random.choice([1, -1]) * random.random() * random.randint(1, 100),
            random.choice([1, -1]) * random.random() * random.randint(1, 100)
            )
    scale = transform.scale(
            random.choice([1, -1]) * random.random() * random.randint(1,2),
            random.choice([1, -1]) * random.random() * random.randint(1,2),
            random.choice([1, -1]) * random.random() * random.randint(1,2)
            )

    return transform.compose(translation, scale)

def random_color():
    return color.color(random.random(), random.random(), random.random())

def random_pattern():
    pats = [patterns.ring_pattern,
            patterns.checkers_pattern,
            patterns.gradient_pattern,
            patterns.stripe_pattern]

    rand_pat = random.choice(pats)(random_color(), random_color())

    rotation = transform.rotation_x(math.pi/(random.randint(1, 5)))
    rand_pat.transform = rotation
    return rand_pat

def main():
    walls = make_walls()
    spheres = make_spheres()

    wrld = world.world()
    wrld.light_source = light.point_light(base.point(-10, 10, -10), color.color(1, 1, 1))
    wrld.add_objs(*(walls + spheres))

    cam = camera.camera(600, 300, math.pi/2)
    cam.transform = transform.view_transform(
            base.point(0, 5, -20),
            base.point(0, 1, 0),
            base.vector(0, 1, 0)
            )


    print("[*] Generating canvas ...")
    canv = camera.render(cam, wrld, progress_bar=True, unit="row", desc="rendering")
    print("[*] Generating the ppm data ...")
    ppm_data = ppm.canvas_to_ppm(canv)
    write_to_file(ppm_data, "pattern_demo5.ppm")
    print("[+] Done")


def write_to_file(ppm_data, filename):
    try:
        print("[*] Writing the ppm_data to the file %s" % (filename, ))
        open(filename, 'w').write(ppm_data)
    except Exception as ex:
        print("[-] Error occured: %s" % (str(ex), ))
    else:
        print("[+] File successfully written to %s" % (filename, ))

if __name__ == '__main__':
    main()
