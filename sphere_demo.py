import shapes
import matrix
import base
import ray
import canvas
import ppm
import color


def main():
    CANVAS_WIDTH, CANVAS_HEIGHT = 100, 100
    canv = canvas.canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    red = color.color(1, 0, 0)
    sphere = shapes.sphere()
    ray_origin = base.point(0, 0, -5)

    canvas_pixels = 100
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
            ints = ray.intersect(sphere, r)

            if ray.hit(ints) is not None:
                canvas.write_pixel(canv, x, y, red)


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
