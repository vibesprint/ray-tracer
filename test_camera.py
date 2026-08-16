import camera
import matrix
import base
import color
import canvas
import light
import shapes
import world
import transformation as transform
import utils


import math


def test_camera():
    c = camera.camera(160, 120, math.pi/2)
    assert c.hsize == 160
    assert c.vsize == 120
    assert c.field_of_view == math.pi/2
    assert matrix.equals(
            c.transform,
            matrix.identity_matrix()
            )


def test_camera2():
    """Pixel size for horizontal canvas"""
    c = camera.camera(200, 125, math.pi/2)
    assert utils.fequals(c.pixel_size, 0.01)

def test_camera3():
    """Pixel size for vertical canvas"""
    c = camera.camera(125, 200, math.pi/2)
    assert utils.fequals(c.pixel_size, 0.01)


def test_ray_for_pixel():
    """Ray through the center of the canvas"""
    c = camera.camera(201, 101, math.pi/2)
    r = camera.ray_for_pixel(c, 100, 50)
    assert base.equals(r.origin, base.point(0, 0, 0))
    assert base.equals(r.direction, base.vector(0, 0, -1))

def test_ray_for_pixel2():
    """Ray through the corner of the canvas"""
    c = camera.camera(201, 101, math.pi/2)
    r = camera.ray_for_pixel(c, 0, 0)
    assert base.equals(r.origin, base.point(0, 0, 0))
    assert base.equals(r.direction, base.vector(0.66519, 0.33259, -0.66851))

def test_ray_for_pixel3():
    """Ray when camera is transformed"""
    c = camera.camera(201, 101, math.pi/2)
    c.transform = transform.compose(
            transform.rotation_y(math.pi/4),
            transform.translation(0, -2, 5)
            )
    r = camera.ray_for_pixel(c, 100, 50)
    assert base.equals(r.origin, base.point(0, 2, -5))
    assert base.equals(r.direction,
            base.vector(math.sqrt(2)/2, 0, -math.sqrt(2)/2)
            )


def default_world():
    lght = light.point_light(base.point(-10, 10, -10), color.color(1, 1, 1))
    s1 = shapes.sphere()
    s1.material.color = color.color(0.8, 1.0, 0.6)
    s1.material.diffuse = 0.7
    s1.material.specular = 0.2

    s2 = shapes.sphere()
    s2.set_transform(transform.scale(0.5, 0.5, 0.5))

    wrld = world.world()
    wrld.add_objs(s1, s2)
    wrld.light_source = lght
    return wrld


def test_render():
    w = default_world()
    c = camera.camera(11, 11, math.pi/2)
    frm = base.point(0, 0, -5)
    to = base.point(0, 0, 0)
    up = base.vector(0, 1, 0)
    c.transform = transform.view_transform(frm, to, up)
    img = camera.render(c, w)
    assert color.equals(
            canvas.pixel_at(img, 5, 5),
            color.color(0.38066, 0.47583, 0.2855)
            )
