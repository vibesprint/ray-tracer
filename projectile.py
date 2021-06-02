import base
import canvas
import color
import ppm

class Projectile:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity


class Environment:
    def __init__(self, grav, wind):
        self.gravity = grav
        self.wind = wind

def tick(environ, proj):
    proj.position = base.add(proj.position, proj.velocity)
    proj.velocity = base.add(base.add(proj.velocity, environ.gravity), environ.wind)

def run():
    velocity = base.normalize(base.vector(1, 1.8, 0))
    velocity = base.scalar_mul(velocity, 11.25)
    proj = Projectile(base.point(0, 1, 0), velocity)
    proj_color = color.color(1, 1, 1)
    CANVAS_WIDTH = 900
    CANVAS_HEIGHT = 550
    canv = canvas.canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    env = Environment(base.vector(0, -0.1, 0), base.vector(-0.01, 0, 0))

    while proj.position[1] > 0:
        print(f"Projectile: {proj.position}")
        tick(env, proj)
        x = int(proj.position[0])
        y = int(canvas.height(canv) - proj.position[1])
        if x < 0 or x > CANVAS_WIDTH:
            continue
        if y < 0 or y > CANVAS_HEIGHT:
            continue
        canvas.write_pixel(canv, x, y, proj_color)

    print("Generating the ppm file ...")
    ppm_data = ppm.canvas_to_ppm(canv)
    print("PPM generated!")
    write_ppm("projectile.ppm", ppm_data)


def write_ppm(filename, data):
    print(f"[+] Writing ppm data to file {filename}")
    try:
        open(filename, 'w').write(data)
    except Exception as err:
        print(f"Error while writing: {err}")
        return
    print("File successfully written!")

if __name__ == '__main__':
    run()
