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


def test_prepare_computations():
    r = ray.ray(base.point(0, 0, -5), base.vector(0, 0, 1))
    sphere = shapes.sphere()
    i = ray.intersection(4, sphere)
    comps = world.prepare_computations(i, r)
    assert comps.t == i.t
    assert comps.object == i.object
    assert base.equals(comps.point, base.point(0, 0, -1))
    assert base.equals(comps.eyev, base.vector(0, 0, -1))
    assert base.equals(comps.normalv, base.vector(0, 0, -1))

def test_prepare_computations2():
    """The hit, when an intersection occur on the outside"""
    r = ray.ray(base.point(0, 0, -5), base.vector(0, 0, 1))
    sphere = shapes.sphere()
    i = ray.intersection(4, sphere)
    comps = world.prepare_computations(i, r)
    assert comps.inside == False


def test_prepare_computations3():
    """The hit, when the intersection occurs on the inside"""
    r = ray.ray(base.point(0, 0, 0), base.vector(0, 0, 1))
    sphere = shapes.sphere()
    i = ray.intersection(1, sphere)
    comps = world.prepare_computations(i, r)
    assert base.equals(comps.point,
            base.point(0, 0, 1))
    assert base.equals(comps.eyev,
            base.vector(0, 0, -1))
    assert comps.inside == True
    assert base.equals(comps.normalv,
            base.vector(0, 0, -1))


def test_shade_hit():
    w = default_world()
    r = ray.ray(base.point(0, 0, -5), base.vector(0, 0, 1))
    shape = w.objects[0]
    i = ray.intersection(4, shape)
    comps = world.prepare_computations(i, r)
    c = world.shade_hit(w, comps)
    assert color.equals(c,
            color.color(0.38066, 0.47583, 0.2855))

def test_shade_hit2():
    """Shading an intersection from inside"""
    w = default_world()
    w.light_source = light.point_light(base.point(0, 0.25, 0), color.color(1, 1, 1))
    r = ray.ray(base.point(0, 0, 0), base.vector(0, 0, 1))
    shape = w.objects[1]
    i = ray.intersection(0.5, shape)
    comps = world.prepare_computations(i, r)
    c = world.shade_hit(w, comps)
    assert color.equals(
            c,
            color.color(0.90498, 0.90498, 0.90498)
            )


def test_color_at():
    w = default_world()
    r = ray.ray(base.point(0, 0, -5), base.vector(0, 1, 0))
    c = world.color_at(w, r)
    assert color.equals(
            c,
            color.color(0, 0, 0)
            )

def test_color_at2():
    """Color when a ray hits"""
    w = default_world()
    r = ray.ray(base.point(0, 0, -5), base.vector(0, 0, 1))
    c = world.color_at(w, r)
    assert color.equals(
            c,
            color.color(0.38066, 0.47583, 0.2855)
            )

def test_color_at3():
    """Color with an intersection behind the ray"""
    w = default_world()
    outer = w.objects[0]
    outer.material.ambient = 1
    inner = w.objects[1]
    inner.material.ambient = 1
    r = ray.ray(base.point(0, 0, 0.75), base.vector(0, 0, -1))
    c = world.color_at(w, r)
    assert color.equals(
            c,
            inner.material.color
            )


def test_is_shadowed():
    w = default_world()
    p = base.point(0, 10, 10)
    assert world.is_shadowed(w, p) == False

    p = base.point(10, -10, 10)
    assert world.is_shadowed(w, p) == True

    p = base.point(-20, 20, -20)
    assert world.is_shadowed(w, p) == False

    p = base.point(-2, 2, -2)
    assert world.is_shadowed(w, p) == False
