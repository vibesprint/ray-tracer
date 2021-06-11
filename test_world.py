import world
import color
import light
import material
import base
import shapes
import ray
import transformation as transform

def test_world():
    wld = world.world()
    assert len(wld.objects) == 0
    assert wld.light_source is None


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


def test_default_world():
    lght = light.point_light(base.point(-10, 10, -10), color.color(1, 1, 1))
    s1 = shapes.sphere()
    s1.material.color = color.color(0.8, 1.0, 0.6)
    s1.material.diffuse = 0.7
    s1.material.specular = 0.2

    s2 = shapes.sphere()
    s2.set_transform(transform.scale(0.5,  0.5, 0.5))

    wrld = default_world()

    assert wrld.light_source == lght
    assert s1 in wrld.objects
    assert s2 in wrld.objects


def test_intersect_world():
    w = default_world()
    r = ray.ray(base.point(0, 0, -5), base.vector(0, 0, 1))
    xs = world.intersect_world(w, r)
    assert xs.count == 4
    assert xs[0].t == 4
    assert xs[1].t == 4.5
    assert xs[2].t == 5.5
    assert xs[3].t == 6
