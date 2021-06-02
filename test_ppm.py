import ppm
import canvas
import color
import pprint


def test_header():
    canv = canvas.canvas(5, 3)
    header = "P3\n5 3\n255"
    test_header = ppm.canvas_to_ppm(canv).split('\n')[:3]
    test_header = '\n'.join(test_header)
    assert test_header == header


def test_pixel_data():
    canv = canvas.canvas(5, 3)
    c1 = color.color(1.5, 0, 0)
    c2 = color.color(0, 0.5, 0)
    c3 = color.color(-0.5, 0, 1)

    canvas.write_pixel(canv, 0, 0, c1)
    canvas.write_pixel(canv, 2, 1, c2)
    canvas.write_pixel(canv, 4, 2, c3)

    ppm_data = ppm.canvas_to_ppm(canv)

    ppm_pixels = ppm_data.split('\n')[3:6]
    ppm_pixels = '\n'.join(ppm_pixels)
    print(ppm_pixels)

    assert ppm_pixels == """255 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 128 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 255"""



def test_line_length():
    canv = canvas.canvas(10, 2)
    for i in range(canvas.width(canv)):
        for j in range(canvas.height(canv)):
            canvas.write_pixel(canv, i, j, color.color(1, 0.8, 0.6))

    ppm_data = ppm.canvas_to_ppm(canv)
    ppm_pixels = ppm_data.split('\n')[3:7]
    for line in ppm_pixels:
        print('length:', len(line))
    ppm_pixels = '\n'.join(ppm_pixels)

    assert ppm_pixels == """255 204 153 255 204 153 255 204 153 255 204 153 255 204 153 255 204
153 255 204 153 255 204 153 255 204 153 255 204 153
255 204 153 255 204 153 255 204 153 255 204 153 255 204 153 255 204
153 255 204 153 255 204 153 255 204 153 255 204 153"""



def test_newline_ending():
    canv = canvas.canvas(5, 3)
    ppm_data = ppm.canvas_to_ppm(canv)
    assert ppm_data[-1] == '\n'
