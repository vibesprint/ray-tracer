import color
import canvas
import ppm

import random

def main():
    canv = canvas.canvas(1280, 720)
    for i in range(canvas.width(canv)):
        col = random_color()
        for j in range(canvas.height(canv)):
            canvas.write_pixel(canv, i, j, col)

    print("[+] Canvas generated")
    print("[+] Generating ppm string ...")
    ppm_data = ppm.canvas_to_ppm(canv)
    print("[+] PPM data generated")
    write_ppm("random_img.ppm", ppm_data)

def random_color():
    return color.color(
            random.random(),
            random.random(),
            random.random()
            )

def write_ppm(filename, ppm_data):
    print(f"[+] Writing ppm data to file {filename}")
    try:
        open(filename, 'w').write(ppm_data)
    except Exception as ex:
        print(f"[-] Error occured: {ex}")
        return
    print("[+] PPM file successfully generated")


if __name__ == '__main__':
    main()
