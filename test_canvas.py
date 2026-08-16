import canvas
import color



def test_canvas():
    canv = canvas.canvas(10, 20)
    assert canvas.width(canv) == 10
    assert canvas.height(canv) == 20
    for row in canv:
        for col in row:
            assert color.equals(
                    col,
                    color.color(0, 0, 0)
                    )


def test_write_pixel():
    canv = canvas.canvas(10, 20)
    red = color.color(1, 0, 0)
    canvas.write_pixel(canv, 2, 3, red)
    assert color.equals(
            canvas.pixel_at(canv, 2, 3),
            red
            )
