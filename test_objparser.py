import objparser as parser
import base

def test_parse_obj_file():
    gibberish = """There was a young lady named Bright
who travelled much faster than light.
She set out one day
in a relative way,
and came back the previous night."""

    res = parser.parse_obj_file(gibberish)
    assert res.ignored_lines == 5



def test_parse_obj_file2():
    file = """v -1 1 0
v -1.00000 0.5000 0.00000
v 1 0 0
v 1 1 0"""

    result = parser.parse_obj_file(file)
    assert len(result.vertices) == 4
    assert base.equals(result.vertices[1], base.point(-1, 1, 0))
    assert base.equals(result.vertices[2], base.point(-1, .5, 0))
    assert base.equals(result.vertices[3], base.point(1, 0, 0))
    assert base.equals(result.vertices[4], base.point(1, 1, 0))


def test_parse_obj_file3():
    file = """
v -1 1 0
v -1 0 0
v 1 0 0
v 1 1 0

f 1 2 3
f 1 3 4
"""
    result = parser.parse_obj_file(file)
    g = result.default_group
    t1 = g[0]
    t2 = g[1]

    assert base.equals(result.vertices[1], t1.p1)
    assert base.equals(result.vertices[2], t1.p2)
    assert base.equals(result.vertices[3], t1.p3)
    assert base.equals(result.vertices[1], t2.p1)
    assert base.equals(result.vertices[3], t2.p2)
    assert base.equals(result.vertices[4], t2.p3)


def test_obj_parse_file4():
    file = """
v -1 1 0
v -1 0 0
v 1 0 0
v 1 1 0
v 0 2 0

f 1 2 3 4 5
"""

    result = parser.parse_obj_file(file)
    g = result.default_group
    t1 = g[0]
    t2 = g[1]
    t3 = g[2]

    assert base.equals(t1.p1, result.vertices[1])
    assert base.equals(t1.p2, result.vertices[2])
    assert base.equals(t1.p3, result.vertices[3])
    assert base.equals(t2.p1, result.vertices[1])
    assert base.equals(t2.p2, result.vertices[3])
    assert base.equals(t2.p3, result.vertices[4])
    assert base.equals(t3.p1, result.vertices[1])
    assert base.equals(t3.p2, result.vertices[4])
    assert base.equals(t3.p3, result.vertices[5])


def test_parse_obj_file5():
    file = """
v -1 1 0
v -1 0 0
v 1 0 0
v 1 1 0

g FirstGroup
f 1 2 3
g SecondGroup
f 1 3 4
"""

    result = parser.parse_obj_file(file)
    g1 = result.get_group("FirstGroup")
    g2 = result.get_group("SecondGroup")
    t1 = g1[0]
    t2 = g2[0]

    assert base.equals(t1.p1, result.vertices[1])
    assert base.equals(t1.p2, result.vertices[2])
    assert base.equals(t1.p3, result.vertices[3])
    assert base.equals(t2.p1, result.vertices[1])
    assert base.equals(t2.p2, result.vertices[3])
    assert base.equals(t2.p3, result.vertices[4])


def test_parse_obj_file6():
    file = """
v -1 1 0
v -1 0 0
v 1 0 0
v 1 1 0

g FirstGroup
f 1 2 3
g SecondGroup
f 1 3 4
"""

    result = parser.parse_obj_file(file)
    g = parser.obj_to_group(result)
    assert result.get_group('FirstGroup') in g
    assert result.get_group('SecondGroup') in g
