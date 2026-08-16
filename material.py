import color
import base

class material:
    def __init__(self):
        self.color = color.color(1, 1, 1)
        self.ambient = 0.1
        self.diffuse = 0.9
        self.specular = 0.9
        self.shininess = 200.0
        self.pattern = None
        self.reflective = 0.0
        self.refractive_index = 1
        self.transparency = 0


    def __eq__(self, other):
        return base.equals(self.color, other.color) and \
                self.ambient == other.ambient and \
                self.diffuse == other.diffuse and \
                self.specular == other.specular and \
                self.shininess == other.shininess
