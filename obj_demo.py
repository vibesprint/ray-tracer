import base
import light
import shapes
import group
import transformation as transform
import camera
import world
import objparser
import color
import ppm

import sys
import math

def get_model():
    print(f'[*] Loading the model into memory ...')
    file, err = load_model_file()

    if err is not None:
        print(f"[-] Unable to load model: {err}")
        sys.exit(-1)

    print(f'[*] Parsing the model file ...')
    parse_res = objparser.parse_obj_file(file)
    print(f"[*] No. of lines ignored: {parse_res.ignored_lines}")
    print(f"[+] Parsing done")
    return objparser.obj_to_group(parse_res)


def load_model_file():
    filename = get_model_filename()
    try:
        return open(filename, 'r').read(), None
    except Exception as ex:
        return "", ex

def get_model_filename():
    if len(sys.argv) >= 2:
        return sys.argv[1]

    print(f"[*] No model file provided. Defaulting to resources/model.obj")
    return "resources/model.obj"


def main():
    model = get_model()

    wrld = world.world()
    wrld.light_source = light.point_light(base.point(-10, 10, -10), color.color(1, 1, 1))
    wrld.add_objs(model)

    cam = camera.camera(300, 150, math.pi/2)
    cam.transform = transform.view_transform(
            base.point(1, 2, -6),
            base.point(0, 0, 0),
            base.vector(0, 1, 0)
            )

    print('[*] Generating canvas ...')
    canvas = camera.render(cam, wrld, progress_bar=True, desc="rendering")
    print('[+] Generating ppm data ...')
    ppm_data = ppm.canvas_to_ppm(canvas)
    write_to_file(ppm_data, "obj_demo.ppm")
    print('[+] SUCCESS')

def write_to_file(data, filename):
    print(f'[*] Writing ppm data to file {filename}')
    try:
        open(filename, "w").write(data)
        print(f'[*] Successfully written file {filename}')

    except Exception as ex:
        print(f'[-] Error while writing file: {ex}')



if __name__ == '__main__':
    main()
