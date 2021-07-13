import ruamel.yaml as yaml
import world
import camera
import shapes
import color
import transformation as transform
import light
import camera
import material
import base
import matrix

from copy import deepcopy

class ParseResult:
    def __init__(self):
        self.scene = world.world()
        self.camera = None
        self.errors = []
        self.ignored_items = 0
        self.definitions = dict()
        self.definitions_dict = dict()
        self.warnings = []
        self.light_added = False


def load_scene(file):
    parsed_file = yaml.safe_load(file)
    return make_scene(parsed_file)


def make_scene(parsed_file):
    parse_res = ParseResult()

    for entry in parsed_file:
        parse_entry(entry, parse_res)

    return parse_res


def parse_entry(entry, parse_res):
    if 'add' in entry:
        parse_add(entry, parse_res)
    elif 'define' in entry:
        parse_define(entry, parse_res)
    else:
        parse_res.errors.append('unable to parse entry: %s' % (str(entry),))
        parse_res.ignored_items += 1

def parse_add(entry, parse_res):
    item = entry['add']

    handlers = {
            'camera': add_camera,
            'cube': add_cube,
            'sphere': add_sphere,
            'light': add_light,
            'plane': add_plane
            }

    if item not in handlers:
        parse_res.errors.append('unknown item to add: %s' % (item, ))
        parse_res.ignored_items += 1
        return

    handlers[item](entry, parse_res)


def parse_define(entry, parse_res):
    if type(entry['value']) is dict:
        define_material(entry, parse_res)

    elif type(entry['value']) is list:
        define_transform(entry, parse_res)

    else:
        parse_res.errors.append(f"unknown value for a definition: {entry['value']}")



def define_material(entry, parse_res):
    if 'extend' in entry:
        value_dict = deepcopy(parse_res.definitions_dict[entry['extend']])
        extension = entry['value']

    else:
        value_dict = deepcopy(entry['value'])
        extension = dict()

    value_dict.update(extension)


    value, err = parse_material(value_dict, parse_res)
    if err is not None:
        parse_res.errors.append(f"unable to parse material value: {entry['value']}")
    else:
        name = entry['define']
        parse_res.definitions[name] = value
        parse_res.definitions_dict[name] = value_dict

def define_transform(entry, parse_res):
    value, err = parse_transform(entry['value'], parse_res)
    if err is not None:
        parse_res.errors.append(f"unable to parse transform value: {entry['value']}")

    else:
        if 'extend' in entry:
            ext = parse_res.definitions[entry['extend']]
        else:
            ext = matrix.identity_matrix()

        value = transform.compose(ext, value)

        name = entry['define']
        parse_res.definitions[name] = value
        parse_res.definitions_dict[name] = entry['value']




def add_camera(entry, parse_res):
    width = entry['width']
    height = entry['height']
    fov = entry['field-of-view']
    frm = base.point(*entry['from'])
    to = base.point(*entry['to'])
    up = base.vector(*entry['up'])

    view = transform.view_transform(frm, to, up)

    cam = camera.camera(width, height, fov)
    cam.transform = view
    parse_res.camera = cam


def add_light(entry, parse_res):
    if parse_res.light_added:
        parse_res.warnings.append(f"skipping the adding of second light source")
    at = base.point(*entry['at'])
    intensity = color.color(*entry['intensity'])
    parse_res.scene.light_source = light.point_light(at, intensity)
    parse_res.light_added = True


def add_material_transform(shape, entry, parse_res):
    plane = shape
    mtrl, err = parse_material(entry['material'], parse_res)
    if err is not None:
        parse_res.warnings.append(f"error while parsing material for {entry['add']}: {entry['material']}")
    else:
        plane.material = mtrl

    trnsf, err = parse_transform(entry['transform'], parse_res)
    if err is not None:
        parse_res.warnings.append(f"unable to parse transform of a {entry['add']}: {entry['transform']}")
    else:
        plane.transform = trnsf



def add_obj(obj, entry, parse_res):
    add_material_transform(obj, entry, parse_res)
    parse_res.scene.add_objs(obj)


def add_sphere(entry, parse_res):
    sphere = shapes.sphere()
    add_obj(sphere, entry, parse_res)

def add_plane(entry, parse_res):
    plane = shapes.plane()
    add_obj(plane, entry, parse_res)

def add_cube(entry, parse_res):
    cube = shapes.cube()
    add_obj(cube, entry, parse_res)



def parse_material(entry, parse_res):
    if type(entry) is str:
        if not entry in parse_res.definitions:
            return None, f"no definition for material '{entry}'"

        return parse_res.definitions[entry], None

    assert type(entry) is dict
    mat = material.material()
    default = {
            'color': color.color(1, 1, 1),
            'ambient': .1,
            'diffuse': .9,
            'specular': .9,
            'shininess': 200,
            'pattern': None,
            'reflective': 0.0,
            'refractive_index': 1.,
            'transparency': 0.
            }

    default.update(entry)

    if type(default['color']) is not color.color:
        default['color'] = color.color(*entry['color'])

    mat.color = default['color']
    mat.ambient = default['ambient']
    mat.diffuse = default['diffuse']
    mat.specular = default['specular']
    mat.shininess = default['shininess']
    mat.pattern = default['pattern']
    mat.reflective = default['reflective']
    mat.refractive_index = default['refractive_index']
    mat.transparency = default['transparency']

    return mat, None


def parse_transform(entry, parse_res):
    transforms = []

    for t in entry:
        if type(t) is str:
            if t not in parse_res.definitions:
                parse_res.warnings.append(f"no transform definition for '{t}'")
            transforms.append(parse_res.definitions[t])
            continue

        transform_type = t[0]
        if transform_type == 'translate':
            transforms.append(transform.translation(t[1], t[2], t[3]))
        elif transform_type == 'rotate-x':
            transforms.append(transform.rotation_x(t[1]))
        elif transform_type == 'rotate-y':
            transforms.append(transform.rotation_y(t[1]))
        elif transform_type == 'rotate-z':
            transforms.append(transform.rotation_z(t[1]))
        elif transform_type == 'scale':
            transforms.append(transform.scale(t[1], t[2], t[3]))
        else:
            parse_res.warnings.append(f"unknown transform type '{transform_type}'")

    transforms.reverse()
    return transform.compose(*transforms), None
