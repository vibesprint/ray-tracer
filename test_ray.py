import ray
import base


def test_ray():
    position = base.point(1, 2, 3)
    direction = base.vector(4, 5, 6)
    r = ray.ray(position, direction)

    assert base.equals(
            r.origin,
            position
            )

    assert base.equals(
            r.direction,
            direction
            )


def test_position():
    r = ray.ray(
            base.point(2, 3, 4),
            base.vector(1, 0, 0)
            )

    assert base.equals(
            ray.position(r, 0),
            base.point(2, 3, 4)
            )

    assert base.equals(
            ray.position(r, 1),
            base.point(3, 3, 4)
            )

    assert base.equals(
            ray.position(r, -1),
            base.point(1, 3, 4)
            )

    assert base.equals(
            ray.position(r, 2.5),
            base.point(4.5, 3, 4)
            )
