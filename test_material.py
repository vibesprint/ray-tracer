import material
import color
import base


def test_material():
    m = material.material()
    assert base.equals(m.color, color.color(1, 1, 1))
    assert m.ambient == 0.1
    assert m.diffuse == 0.9
    assert m.specular == 0.9
    assert m.shininess == 200.0
