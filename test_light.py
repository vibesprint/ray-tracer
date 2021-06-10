import light
import color
import base

def test_point_light():
    position = base.point(0, 0, 0)
    intensity = color.color(1, 1, 1)
    lht = light.point_light(position, intensity)
    assert base.equals(lht.position, position)
    assert base.equals(lht.intensity, intensity)
