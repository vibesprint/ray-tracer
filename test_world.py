import world
import color
import light
import material
import base
import shapes
import ray
import transformation as transform
import utils

import math

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


def test_shade_hit3():
    w = world.world()
    w.light_source = light.point_light(base.point(0, 0, -10), color.color(1, 1, 1))
    s1 = shapes.sphere()
    w.add_objs(s1)

    s2 = shapes.sphere()
    s2.transform = transform.translation(0, 0, 10)
    w.add_objs(s2)

    r = ray.ray(base.point(0, 0, 5), base.vector(0, 0, 1))
    i = ray.intersection(4, s2)
    comps = world.prepare_computations(i, r)
    c = world.shade_hit(w, comps)
    assert color.equals(c, color.color(0.1, 0.1, 0.1))

def test_prepare_computations4():
    r = ray.ray(base.point(0, 0, -5), base.vector(0, 0, 1))
    shape = shapes.sphere()
    shape.transform = transform.translation(0, 0, 1)
    i = ray.intersection(5, shape)
    comps = world.prepare_computations(i, r)

    EPSILON = 0.00001
    assert comps.over_point[2] < -world.EPSILON/2
    assert comps.point[2] > comps.over_point[2]


def test_prepare_computations5():
    r = ray.ray(base.point(0, 1, -1), base.vector(0, -math.sqrt(2)/2, math.sqrt(2)/2))
    shape = shapes.plane()
    i = ray.intersection(math.sqrt(2), shape)
    comps = world.prepare_computations(i, r)
    assert base.equals(comps.reflectv, base.vector(0, math.sqrt(2)/2, math.sqrt(2)/2))


def test_reflected_color():
    w = default_world()
    r = ray.ray(base.point(0, 0, 0), base.vector(0, 0, 1))
    shape = w.objects[1]
    shape.material.ambient = 1
    i = ray.intersection(1, shape)
    comps = world.prepare_computations(i, r)
    col = world.reflected_color(w, comps)
    assert color.equals(col, color.color(0, 0, 0))


def test_reflected_color2():
    w = default_world()
    shape = shapes.plane()
    shape.material.reflective = 0.5
    shape.transform = transform.translation(0, -1, 0)
    w.add_objs(shape)
    r = ray.ray(base.point(0, 0, -3), base.vector(0, -math.sqrt(2)/2, math.sqrt(2)/2))
    i = ray.intersection(math.sqrt(2), shape)
    comps = world.prepare_computations(i, r)
    col = world.reflected_color(w, comps)
    assert color.equals(
            col,
            color.color(0.190332, 0.237915, 0.1427491)
            )


def test_shade_hit4():
    w = default_world()
    shape = shapes.plane()
    shape.material.reflective = 0.5
    shape.transform = transform.translation(0, -1, 0)
    w.add_objs(shape)
    r = ray.ray(base.point(0, 0, -3), base.vector(0, -math.sqrt(2)/2, math.sqrt(2)/2))
    i = ray.intersection(math.sqrt(2), shape)
    comps = world.prepare_computations(i, r)
    col = world.shade_hit(w, comps)
    assert color.equals(
            col,
            color.color(0.876757, 0.9243403, 0.8291742)
            )


def test_halting():
    """color_at should halt for mutually reflective surfaces and avoid infinite recursion"""
    w = world.world()
    w.light_source = light.point_light(base.point(0, 0, 0), color.color(1, 1, 1))
    lower = shapes.plane()
    lower.material.reflective = 1
    lower.transform = transform.translation(0, -1, 0)

    upper = shapes.plane()
    upper.material.reflective = 1
    upper.transform = transform.translation(0, 1, 0)

    w.add_objs(lower, upper)
    r = ray.ray(base.point(0, 0, 0), base.vector(0, 1, 0))

    world.color_at(w, r) # This should terminate, otherwise python would raise exception due to recursion limit


def test_reflected_color3():
    w = default_world()
    shape = shapes.plane()
    shape.material.reflective = 0.5
    shape.transform = transform.translation(0, -1, 0)
    w.add_objs(shape)
    r = ray.ray(base.point(0, 0, 0), base.vector(0, -math.sqrt(2)/2, math.sqrt(2)/2))
    i = ray.intersection(math.sqrt(2), shape)
    comps = world.prepare_computations(i, r)
    col = world.reflected_color(w, comps, 0)
    assert color.equals(col, color.color(0, 0, 0))


def refraction_test(idx, n1, n2):
    A = shapes.glass_sphere()
    A.transform = transform.scale(2, 2, 2)
    A.material.refractive_index = 1.5

    B = shapes.glass_sphere()
    B.transform = transform.translation(0, 0, -0.25)
    B.material.refractive_index = 2.0

    C = shapes.glass_sphere()
    C.transform = transform.translation(0, 0, 0.25)
    C.material.refractive_index = 2.5

    r = ray.ray(base.point(0, 0, -4), base.vector(0, 0, 1))
    xs = ray.intersections(
            ray.intersection(2, A),
            ray.intersection(2.75, B),
            ray.intersection(3.25, C),
            ray.intersection(4.75, B),
            ray.intersection(5.25, C),
            ray.intersection(6, A)
            )
    comps = world.prepare_computations(xs[idx], r, xs)
    assert utils.fequals(comps.n1, n1)
    assert utils.fequals(comps.n2, n2)

def test_prepare_computations6():
    refraction_test(0, 1, 1.5)
    refraction_test(1, 1.5, 2)
    refraction_test(2, 2, 2.5)
    refraction_test(3, 2.5, 2.5)
    refraction_test(4, 2.5, 1.5)
    refraction_test(5, 1.5, 1.0)

def test_prepare_computations7():
    r = ray.ray(base.point(0, 0, -5), base.vector(0, 0, 1))
    shape = shapes.glass_sphere()
    shape.transform = transform.translation(0, 0, 1)
    i = ray.intersection(5, shape)
    xs = ray.intersections(i)
    comps = world.prepare_computations(i, r, xs)
    EPSILON = 1e-5
    assert comps.under_point[2] > EPSILON/2
    assert comps.point[2] < comps.under_point[2]

def test_refracted_color():
    w = default_world()
    shape = w.objects[0]
    r = ray.ray(base.point(0, 0, -5), base.vector(0, 0, 1))
    xs = ray.intersections(
            ray.intersection(4, shape),
            ray.intersection(4, shape)
            )
    comps = world.prepare_computations(xs[0], r, xs)
    col = world.refracted_color(w, comps)
    assert color.equals(
            col,
            color.color(0, 0, 0)
            )


def test_refracted_color2():
    w = default_world()
    shape = w.objects[0]
    shape.material.transparency = 1.0
    shape.material.refractive_index = 1.5
    r = ray.ray(base.point(0, 0, -5), base.vector(0, 0, 1))
    xs = ray.intersections(
            ray.intersection(4, shape),
            ray.intersection(4, shape)
            )
    comps = world.prepare_computations(xs[0], r, xs)
    col = world.refracted_color(w, comps, 0)
    assert color.equals(
            col,
            color.color(0, 0, 0)
            )


def test_refracted_color3():
    """total internal reflection"""
    w = default_world()
    shape = w.objects[0]
    shape.material.transparency = 1.
    shape.material.refractive_index = 1.5
    r = ray.ray(base.point(0, 0, math.sqrt(2)/2), base.vector(0, 1, 0))
    xs = ray.intersections(
            ray.intersection(-math.sqrt(2)/2, shape),
            ray.intersection(math.sqrt(2)/2, shape)
            )
    comps = world.prepare_computations(xs[1], r, xs)
    col = world.refracted_color(w, comps)
    assert color.equals(
            col,
            color.color(0, 0, 0)
            )


import patterns

def default_pattern():
    class TestPattern(patterns.Pattern):
        def pattern_at(self, local_pt):
            return color.color(local_pt[0], local_pt[1], local_pt[2])

    return TestPattern()

def _test_refracted_color3():
    w = default_world()
    A = w.objects[0]
    A.material.ambient = 1.0
    A.material.patttern = default_pattern()

    B = w.objects[1]
    B.material.transparency = 1.0
    B.material.refractive_index = 1.5

    r = ray.ray(base.point(0, 0, 0.1), base.vector(0, 1, 0))
    xs = ray.intersections(
            ray.intersection(-0.9899, A),
            ray.intersection(-0.4899, B),
            ray.intersection(0.4899, B),
            ray.intersection(0.9899, A)
            )
    comps = world.prepare_computations(xs[2], r, xs)
    col = world.refracted_color(w, comps, 5)
    assert color.equals(
            col,
            color.color(0., 0.99888, 0.04725)
            )


def test_shade_hit5():
    """shade_hit() with a transparent material"""
    w = default_world()
    floor = shapes.plane()
    floor.transform = transform.translation(0, -1, 0)
    floor.material.transparency = 0.5
    floor.material.refractive_index = 1.5
    w.add_objs(floor)

    ball = shapes.sphere()
    ball.material.color = color.color(1, 0, 0)
    ball.material.ambient = 0.5
    ball.transform = transform.translation(0, -3.5, -.5)
    w.add_objs(ball)

    r = ray.ray(base.point(0, 0, -3), base.vector(0, -math.sqrt(2)/2, math.sqrt(2)/2))
    xs = ray.intersections(
            ray.intersection(math.sqrt(2), floor)
            )
    comps = world.prepare_computations(xs[0], r, xs)
    col = world.shade_hit(w, comps, 5)
    assert color.equals(
            col,
            color.color(0.93642, 0.68642, 0.68642)
            )

def test_schlick():
    shape = shapes.glass_sphere()
    r = ray.ray(base.point(0, 0, math.sqrt(2)/2), base.vector(0, 1, 0))
    xs = ray.intersections(
            ray.intersection(-math.sqrt(2)/2, shape),
            ray.intersection(math.sqrt(2)/2, shape)
            )
    comps = world.prepare_computations(xs[1], r, xs)
    reflectance = world.schlick(comps)
    assert utils.fequals(reflectance, 1.)


def test_schlick2():
    """schlick approximation with a perpendicular viewing angle"""
    shape = shapes.glass_sphere()
    r = ray.ray(base.point(0, 0, 0), base.vector(0, 1, 0))
    xs = ray.intersections(
            ray.intersection(-1, shape),
            ray.intersection(1, shape)
            )
    comps = world.prepare_computations(xs[1], r, xs)
    reflectance = world.schlick(comps)
    assert utils.fequals(reflectance, 0.04)


def test_schlick3():
    """schlick approximation with small angle and n2 >  n1"""
    shape = shapes.glass_sphere()
    r = ray.ray(base.point(0, 0.99, -2), base.vector(0, 0, 1))
    xs = ray.intersections(
            ray.intersection(1.8589, shape)
            )
    comps = world.prepare_computations(xs[0], r, xs)
    reflectance = world.schlick(comps)
    assert utils.fequals(reflectance, 0.48873)


def test_shade_hit6():
    w = default_world()
    r = ray.ray(base.point(0, 0, -3), base.vector(0, -math.sqrt(2)/2, math.sqrt(2)/2))
    floor = shapes.plane()
    floor.transform = transform.translation(0, -1, 0)
    floor.material.reflective = 0.5
    floor.material.transparency = .5
    floor.material.refractive_index = 1.5

    ball = shapes.sphere()
    ball.material.color = color.color(1, 0, 0)
    ball.material.ambient = 0.5
    ball.transform = transform.translation(0, -3.5, -0.5)

    w.add_objs(floor, ball)
    xs = ray.intersections(
            ray.intersection(math.sqrt(2), floor)
            )
    comps = world.prepare_computations(xs[0], r, xs)
    col = world.shade_hit(w, comps)
    assert color.equals(
            col,
            color.color(0.93391, 0.69643, 0.69243)
            )
