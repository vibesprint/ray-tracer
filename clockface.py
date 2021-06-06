import transformation as transform
import base
import canvas
import color
import ppm

import math

def clock_hand_generator(init_hand):
    rot = transform.rotation_z(math.pi/6)
    hand = init_hand
    def generator():
        nonlocal hand
        hand = transform.apply(rot, hand)
        if base.equals(hand, init_hand):
            return None
        return hand

    return generator

def main():
    print('[+] Making canvas of 20 by 20 pixels')
    canv = canvas.canvas(200, 200)
    generate_hands(canv)
    print('[+] Generating ppm data ...')
    ppm_data = ppm.canvas_to_ppm(canv)
    write_to_file(ppm_data, 'clockface.ppm')
    print('[+] Done')

def generate_hands(canv):
    print('[+] Generating clock hands')
    cwidth = canvas.width(canv)
    cheight = canvas.height(canv)
    cmidpt = (cwidth//2, cheight//2)
    radius = int(3/8 * cwidth)

    init_hand = base.point(0, 1, 0)

    white = color.color(1, 1, 1)
    set_pixel(canv, translate_to_canvas(canv, init_hand, radius), white)

    generator = clock_hand_generator(init_hand)
    next_hand = generator()

    while next_hand is not None:
        set_pixel(canv, translate_to_canvas(canv, next_hand, radius), white)
        next_hand = generator()

    print('[+] Done generating hands of the clock')


def translate_to_canvas(canv, pt, radius):
    res = base.point(pt[0], pt[1], pt[2])
    res = base.scalar_mul(res, radius)
    res = base.add(res,
            base.point(
                canvas.width(canv)//2,
                canvas.height(canv)//2,
                0)
            )
    return res


def write_to_file(ppm_data, filename):
    print('[+] Writing ppm data to file ...')
    try:
        open(filename, 'w').write(ppm_data)
    except Exception as ex:
        print("[-] Error: {ex}")
        return
    print(f'[+] Successfully written ppm data to file {filename}')


def set_pixel(canv, pt, col):
    width = canvas.width(canv)
    height = canvas.height(canv)

    if pt[0] <= 0 or pt[0] >= (width):
        return
    if pt[1] <= 0 or pt[1] >= (height):
        return

    canvas.write_pixel(canv,
            int(pt[0]), int(pt[1]),
            col)


if __name__ == '__main__':
    main()
