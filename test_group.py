import group
import matrix
import shapes
import ray
import base
import transformation as transform


def test_group():
    grp = group.group()
    assert len(grp) == 0
    assert matrix.equals(grp.transform, matrix.identity_matrix())


def default_shape():

    class TestShape(shapes.Shape):
        def local_intersect(self, ray_):
            self.saved_ray = ray_

        def local_normal_at(self, local_pt):
            return base.vector(local_pt[0], local_pt[1], local_pt[2])

    return TestShape()



def test_group_add_child():
    grp = group.group()
    shape = default_shape()
    grp.add_child(grp)

    assert len(grp) > 0
    assert shape in grp
    assert grp.parent is grp


def test_group_local_intersect():
    g = group.group()
    r = ray.ray(base.point(0, 0, 0), base.vector(0, 0, 1))
    xs = g.local_intersect(r)
    assert xs.count == 0

def test_group_local_intersect2():
    g = group.group()
    s1 = shapes.sphere()
    s2 = shapes.sphere()
    s2.transform = transform.translation(0, 0, -3)
    s3 = shapes.sphere()
    s3.transform = transform.translation(5, 0, 0)
    g.add_child(s1)
    g.add_child(s2)
    g.add_child(s3)
    r = ray.ray(base.point(0, 0, -5), base.vector(0, 0, 1))
    xs = g.local_intersect(r)

    assert xs.count == 4
    xs[0].object == s2
    xs[1].object == s2
    xs[2].object == s1
    xs[3].object == s1


def test_group_intersect():
    g = group.group()
    g.transform = transform.scale(2, 2, 2)
    s = shapes.sphere()
    s.transform = transform.translation(5, 0, 0)
    g.add_child(s)
    r = ray.ray(base.point(10, 0, -10), base.vector(0, 0, 1))
    xs = ray.intersect(g, r)
    assert xs.count == 2
