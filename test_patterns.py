import color
import patterns
import base
import shapes
import transformation as transform
import base

def black_white():
    return color.color(0, 0, 0), color.color(1, 1, 1)


def test_stripe_pattern():
    black, white = black_white()
    pat = patterns.stripe_pattern(white, black)
    assert color.equals(pat.a, white)
    assert color.equals(pat.b, black)


def test_stripe_at():
    """A stripe pattern is constant is y"""
    black, white = black_white()
    pat = patterns.stripe_pattern(white, black)

    assert color.equals(
            pat.stripe_at(base.point(0, 0, 0)),
            white
            )

    assert color.equals(
            pat.stripe_at(base.point(0, 1, 0)),
            white
            )

    assert color.equals(
            pat.stripe_at(base.point(0, 2, 0)),
            white
            )

def test_stripe_at2():
    """Stripe pattern is constant in z"""
    black, white = black_white()
    pat = patterns.stripe_pattern(white, black)

    assert color.equals(
            pat.stripe_at(base.point(0, 0, 0)),
            white
            )

    assert color.equals(
            pat.stripe_at(base.point(0, 0, 1)),
            white
            )

    assert color.equals(
            pat.stripe_at(base.point(0, 0, 2)),
            white
            )


def test_stripe_at3():
    """Stripe pattern alternates in x"""
    black, white = black_white()
    pat = patterns.stripe_pattern(white, black)

    assert color.equals(
            pat.stripe_at(base.point(0, 0, 0)),
            white
            )

    assert color.equals(
            pat.stripe_at(base.point(0.9, 0, 0)),
            white
            )

    assert color.equals(
            pat.stripe_at(base.point(1, 0, 0)),
            black
            )

    assert color.equals(
            pat.stripe_at(base.point(-0.1, 0, 0)),
            black
            )

    assert color.equals(
            pat.stripe_at(base.point(-1, 0, 0)),
            black
            )

    assert color.equals(
            pat.stripe_at(base.point(-1.1, 0, 0)),
            white
            )



def default_pattern():
    class TestPattern(patterns.Pattern):
        def pattern_at(self, local_pt):
            return color.color(local_pt[0], local_pt[1], local_pt[2])

    return TestPattern()

import matrix

def test_pattern():
    """default transformation"""
    pat = default_pattern()
    assert matrix.equals(pat.transform, matrix.identity_matrix())

def test_pattern2():
    """transformation can be assigned"""
    pat = default_pattern()
    pat.transform = transform.translation(1, 2, 3)
    assert matrix.equals(pat.transform, transform.translation(1, 2, 3))

def test_pattern_at_shape():
    """A pattern with an object transformation"""
    shape = shapes.sphere()
    shape.transform = transform.scale(2, 2, 2)
    pat = default_pattern()
    c = pat.pattern_at_shape(shape, base.point(2, 3, 4))
    assert color.equals(c, color.color(1, 1.5, 2))

def test_pattern_at_shape2():
    """A pattern with a pattern transformation"""
    shape = shapes.sphere()
    pat = default_pattern()
    pat.transform = transform.scale(2, 2, 2)
    c = pat.pattern_at_shape(shape, base.point(2, 3, 4))
    assert color.equals(c, color.color(1, 1.5, 2))

def test_pattern_at_shape3():
    """Both object and pattern transformation"""
    shape = shapes.sphere()
    pat = default_pattern()
    pat.transform = transform.translation(0.5, 1, 1.5)
    shape.transform = transform.scale(2, 2, 2)
    c = pat.pattern_at_shape(shape, base.point(2.5, 3, 3.5))
    assert color.equals(c, color.color(0.75, 0.5, 0.25))

def test_gradient_pattern():
    black, white = black_white()
    pat = patterns.gradient_pattern(white, black)
    assert color.equals(
            pat.pattern_at(base.point(0, 0, 0)),
            white
            )

    assert color.equals(
            pat.pattern_at(base.point(0.25, 0, 0)),
            color.color(0.75, 0.75, 0.75)
            )

    assert color.equals(
            pat.pattern_at(base.point(0.5, 0, 0)),
            color.color(0.5, 0.5, 0.5)
            )

    assert color.equals(
            pat.pattern_at(base.point(0.75, 0, 0)),
            color.color(0.25, 0.25, 0.25)
            )


def test_ring_pattern():
    black, white = black_white()
    pat = patterns.ring_pattern(white, black)
    assert color.equals(
            pat.pattern_at(base.point(0, 0, 0)),
            white
            )

    assert color.equals(
            pat.pattern_at(base.point(1, 0, 0)),
            black
            )

    assert color.equals(
            pat.pattern_at(base.point(0, 0, 1)),
            black
            )

    assert color.equals(
            pat.pattern_at(base.point(0.708, 0.708, 0.708)),
            black
            )


def test_checkers_pattern():
    """Checkers should repeat in x"""
    black, white = black_white()
    pat = patterns.checkers_pattern(white, black)
    assert color.equals(
            pat.pattern_at(base.point(0, 0, 0)),
            white
            )

    assert color.equals(
            pat.pattern_at(base.point(0.99, 0, 0)),
            white
            )

    assert color.equals(
            pat.pattern_at(base.point(1.01, 0, 0)),
            black
            )


def test_checkers_pattern2():
    """Checkres should repeat in y"""
    black, white = black_white()
    pat = patterns.checkers_pattern(white, black)
    assert color.equals(
            pat.pattern_at(base.point(0, 0, 0)),
            white
            )

    assert color.equals(
            pat.pattern_at(base.point(0, 0.99, 0)),
            white
            )

    assert color.equals(
            pat.pattern_at(base.point(0, 1.01, 0)),
            black
            )

def test_checkers_pattern3():
    """Checkers should repeat in z"""
    black, white = black_white()
    pat = patterns.checkers_pattern(white, black)
    assert color.equals(
            pat.pattern_at(base.point(0, 0, 0)),
            white
            )

    assert color.equals(
            pat.pattern_at(base.point(0, 0, 0.99)),
            white
            )

    assert color.equals(
            pat.pattern_at(base.point(0, 0, 1.01)),
            black
            )
