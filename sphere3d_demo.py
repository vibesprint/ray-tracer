import shapes
import matrix
import base
import ray
import canvas
import ppm
import color
import light
import transformation as transform

import math


def main():
    CANVAS_WIDTH, CANVAS_HEIGHT = 600, 600
    canv = canvas.canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    red = color.color(1, 0, 0)
    sphere = shapes.sphere()
    transformation = transform.compose(
            transform.rotation_y(math.pi/6),
            transform.rotation_z(math.pi/6),
            transform.scale(1, 0.2, 1)
            )
    sphere.transform = transformation
    sphere.material.color = color.color(1, 0.2, 1)
    ray_origin = base.point(0, 0, -5)

    lght_pos = base.point(7, 5, -10)
    lght_color = color.color(0.75, 1, 1)
    lght = light.point_light(lght_pos, lght_color)

    canvas_pixels = CANVAS_WIDTH
    wall_z = 10
    wall_size = 7
    pixel_size = wall_size / canvas_pixels
    half = wall_size / 2

    print("[+] Generating canvas ...")
    for y in range(canvas.height(canv)):
        world_y = half - pixel_size*y

        for x in range(canvas.width(canv)):
            world_x = -half + pixel_size * x
            pos = base.point(world_x, world_y, wall_z)
            r = ray.ray(ray_origin, base.normalize(
                base.sub(pos, ray_origin)
                )
                )
            r = ray.ray(r.origin,
                    base.normalize(r.direction)
                    )

            ints = ray.intersect(sphere, r)

            hit = ray.hit(ints)
            if hit != None:
                pt = ray.position(r, hit.t)
                normal = shapes.normal_at(hit.object, pt)
                eye = base.negate(r.direction)

                col = light.lightning(hit.object.material, lght, pt, eye, normal)
                canvas.write_pixel(canv, x, y, col)


    print("[+] Canvas generated")
    print("[+] Generating ppm file data ...")
    ppm_data = ppm.canvas_to_ppm(canv)
    print("[+] Generated ppm file data")
    write_to_file(ppm_data, "sphere.ppm")
    print("[+] Done")

def write_to_file(data, filename):
    print("[+] Writing ppm data to file")
    try:
        open(filename, 'w').write(data)
    except Exception as ex:
        print(f"[-] Error: {ex}")
    else:
        print(f"[+] Image file successfully written to {filename}")


if __name__ == '__main__':
    main()
