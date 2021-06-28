import light
import color
import base
import material

import math

def test_point_light():
    position = base.point(0, 0, 0)
    intensity = color.color(1, 1, 1)
    lht = light.point_light(position, intensity)
    assert base.equals(lht.position, position)
    assert base.equals(lht.intensity, intensity)


def lightning_test_setup():
    m = material.material()
    position = base.point(0, 0, 0)
    return m, position


def test_lightning():
    """Eye between the light and the surface"""
    m, position = lightning_test_setup()
    eyev = base.vector(0, 0, -1)
    normalv = base.vector(0, 0, -1)
    lght = light.point_light(base.point(0, 0, -10), color.color(1, 1, 1))
    result = light.lightning(m, lght, position, eyev, normalv)
    print(f"[+] Result {result}")
    assert base.equals(result, color.color(1.9, 1.9, 1.9))

def test_lightning2():
    """Eye between light and the surface, eye offset 45 degrees"""
    m, position = lightning_test_setup()
    const = math.sqrt(2) / 2
    eyev = base.vector(0, const, -const)
    normalv = base.vector(0, 0, -1)
    lght = light.point_light(base.point(0, 0, -10), color.color(1, 1, 1))
    result = light.lightning(m, lght, position, eyev, normalv)
    print(f"[+] Result 2: {result}")
    assert base.equals(result, color.color(1, 1, 1))

def test_lightning3():
    """light offset 45 degrees"""
    m, position = lightning_test_setup()
    eyev = base.vector(0, 0, -1)
    normalv = base.vector(0, 0, -1)
    lght = light.point_light(base.point(0, 10, -10), color.color(1, 1, 1))
    result = light.lightning(m, lght, position, eyev, normalv)
    assert base.equals(result, color.color(0.7364, 0.7364, 0.7364))

def test_lightning4():
    """eye in the path of reflection vector"""
    m, position = lightning_test_setup()
    const = math.sqrt(2) / 2
    eyev = base.vector(0, -const, -const)
    normalv = base.vector(0, 0, -1)
    lght = light.point_light(base.point(0, 10, -10), color.color(1, 1, 1))
    result = light.lightning(m, lght, position, eyev, normalv)
    assert base.equals(result, color.color(1.6364, 1.6364, 1.6364))

def test_lightning5():
    m, position = lightning_test_setup()
    eyev = base.vector(0, 0, -1)
    normalv = base.vector(0, 0, -1)
    lght = light.point_light(base.point(0, 0, 10), color.color(1, 1, 1))
    result = light.lightning(m, lght, position, eyev, normalv)
    assert base.equals(result, color.color(0.1, 0.1, 0.1))


def test_lightning6():
    m, position = lightning_test_setup()
    eyev = base.vector(0, 0, -1)
    normalv = base.vector(0, 0, -1)
    lght = light.point_light(
            base.point(0, 0, -10),
            color.color(1, 1, 1)
            )
    in_shadow = True
    result = light.lightning(m, lght, position, eyev, normalv, in_shadow)
    assert color.equals(result, color.color(0.1, 0.1, 0.1))
