import shapes
import transformation as transform
import matrix
import base


def test_sphere():
    s = shapes.sphere()
    assert matrix.equals(
            s.transform,
            matrix.identity_matrix()
            )

def test_sphere2():
    """Changing sphere's transformation"""
    s = shapes.sphere()
    t = transform.translation(2, 3, 4)
    s.set_transform(t)
    assert matrix.equals(
            s.transform,
            t
            )
