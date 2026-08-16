import base
import group
import shapes


def parse_obj_file(string):
    lines = string.split('\n')
    lines = map(str.strip, lines)

    parse_res = ParseResult()

    for line in lines:
        parse_line(line, parse_res)

    return parse_res


class ParseResult:
    def __init__(self):
        self.ignored_lines = 0
        self.vertices = OneBasedList()
        self.errors = []
        self.default_group = group.group()
        self.cur_group = self.default_group
        self.name_to_group = dict()
        self.normals = OneBasedList()

    def get_group(self, gname):
        return self.name_to_group[gname]


class OneBasedList:
    def __init__(self):
        self.lst= []

    def append(self, *vertices):
        self.lst.extend(vertices)

    def __getitem__(self, idx):
        return self.lst[idx - 1]

    def __len__(self):
        return len(self.lst)

    def __iter__(self):
        return iter(self.lst)



def parse_line(line, parse_res):
    if line == "":
        return

    line = line.split()

    action = line[0]

    if action not in HANDLERS:
        parse_res.ignored_lines += 1
        parse_res.errors.append("invalid token: %s" % (action,))
        return

    return HANDLERS[action](line, parse_res)


def parse_vertex(tokens, parse_res):
    point = [float(tok) for tok in tokens[1:]]
    pt = base.point(*point)
    parse_res.vertices.append(pt)

def parse_face(tokens, parse_res):
    if '/' in tokens[1]:
        parse_face_with_normals(tokens, parse_res)
        return

    indices = [int(tok) for tok in tokens[1:]]
    for i in range(1, len(indices)-1):
        tri = shapes.triangle(parse_res.vertices[indices[0]],
                parse_res.vertices[indices[i]],
                parse_res.vertices[indices[i+1]]
                )
        parse_res.cur_group.add_child(tri)


def parse_face_with_normals(tokens, parse_res):
    vertex_idx, err = parse_vertex_indices(tokens[1:])

    if err is not None:
        parse_res.errors.append(err)
        return

    normal_idx, err = parse_normal_indices(tokens[1:])
    if err is not None:
        parse_res.errors.append(err)
        return

    for i in range(1, len(vertex_idx)-1):
        tri = shapes.smooth_triangle(
                parse_res.vertices[vertex_idx[0]],
                parse_res.vertices[vertex_idx[i]],
                parse_res.vertices[vertex_idx[i+1]],
                parse_res.normals[normal_idx[0]],
                parse_res.normals[normal_idx[i]],
                parse_res.normals[normal_idx[i+1]]
                )

        parse_res.cur_group.add_child(tri)


def parse_vertex_indices(tokens):
    indices = []
    try:
        for tok in tokens:
            idx = int(tok[0:tok.find('/')])
            indices.append(idx)
    except Exception as err:
        return None, err

    return indices, None

def parse_normal_indices(tokens):
    indices = []

    try:
        for tok in tokens:
            idx = int(tok[tok.rfind('/')+1:])
            indices.append(idx)
    except Exception as ex:
        return None, ex

    return indices, None


def parse_group(tokens, parse_res):
    gname = tokens[1]
    grp = group.group()
    parse_res.name_to_group[gname] = grp
    parse_res.cur_group = grp


def parse_normal(tokens, parse_res):
    coords = [float(tok) for tok in tokens[1:]]
    parse_res.normals.append(base.vector(*coords))


HANDLERS = {'v': parse_vertex,
            'f': parse_face,
            'g': parse_group,
            'vn': parse_normal,
            }



def obj_to_group(parse_res):
    grp = group.group()
    grp.add_child(parse_res.default_group)
    for gname in parse_res.name_to_group:
        grp.add_child(parse_res.name_to_group[gname])

    return grp
