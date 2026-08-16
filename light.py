import color
import base

class point_light:
    def __init__(self, position, intensity):
        self.intensity = intensity
        self.position = position

    def __eq__(self, other):
        return color.equals(self.intensity, other.intensity) and \
                base.equals(self.position, other.position)


def reflect(vect, normal):
    return base.sub(
            vect,
            base.scalar_mul(
                normal,
                2 * base.dot(vect, normal)
                )
            )



def lightning(material, obj, light, point, eyev, normalv, in_shadow=False):
    if material.pattern is not None:
        col = material.pattern.pattern_at_shape(obj, point)
    else:
        col = material.color

    effective_color = color.hadamard_mul(col, light.intensity)
    lightv = base.normalize( base.sub(light.position, point) )
    ambient = color.scalar_mul(effective_color, material.ambient)

    if in_shadow:
        return ambient

    diffuse = None
    specular = None

    light_dot_normal = base.dot(lightv, normalv)

    if light_dot_normal < 0:
        diffuse = color.color(0, 0, 0)
        specular = color.color(0, 0, 0)

    else:
        diffuse = color.scalar_mul(effective_color, material.diffuse * light_dot_normal)

        reflectv = reflect(base.negate(lightv), normalv)
        reflect_dot_eye = base.dot(reflectv, eyev)

        if reflect_dot_eye < 0:
            specular = color.color(0, 0, 0)
        else:
            factor = reflect_dot_eye ** material.shininess
            specular = color.scalar_mul(light.intensity, material.specular * factor)

    return color.add(ambient, color.add(diffuse, specular))
