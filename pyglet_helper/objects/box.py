"""
pyglet_helper.box contains an object for drawing a box to the screen

"""
try:
    import pyglet.gl
except Exception as error_msg:
    print("Pyglet import error: "+str(error_msg))
from pyglet_helper.objects import Rectangular
from pyglet_helper.util import Rgb, Vector


class Box(Rectangular):
    """
     A box object.
    """
    def __init__(self, width=1.0, height=1.0, length=1.0, color=Rgb(),
                 pos=Vector([0, 0, 0])):
        """

        :param width: The box's width.
        :type width: float
        :param height: The box's height.
        :type height: float
        :param length: The box's length.
        :type length: float
        :param color: The object's color.
        :type color: pyglet_helper.util.Rgb
        :param pos: The object's position.
        :type pos: pyglet_helper.util.Vector
        """
        super(Box, self).__init__(width=width, height=height, color=color,
                                  length=length, pos=pos)
        self.initialized = False
        self.skip_right_face = False


    def init_model(self, scene):
        """ Add the Vertexes and Normals to the compile list.

        :param scene: The view to render the model to.
        :type scene: pyglet_helper.objects.View
        """
        # Note that this model is also used by arrow!
        scene.box_model.gl_compile_begin()
        pyglet.gl.glEnable(pyglet.gl.GL_CULL_FACE)
        pyglet.gl.glBegin(pyglet.gl.GL_TRIANGLES)
        self.generate_model()
        pyglet.gl.glEnd()
        pyglet.gl.glDisable(pyglet.gl.GL_CULL_FACE)
        scene.box_model.gl_compile_end()
        self.initialized = True

    def render(self, scene):
        """Render the box in the view

        :param scene: The view to render the model into
        :type scene: pyglet_helper.objects.View
        """
        if not scene.box_model.compiled:
            self.init_model(scene)
        self.color.gl_set(self.opacity)
        pyglet.gl.glPushMatrix()
        self.apply_transform(scene)
        scene.box_model.gl_render()
        pyglet.gl.glPopMatrix()

    def generate_model(self):
        """ Generate the vertices and normals.
        """
        corner = 0.5
        vertices = [
            [[+corner, +corner, +corner], [+corner, -corner, +corner],
             [+corner, -corner, -corner], [+corner, +corner, -corner]],
            # Right face
            [[-corner, +corner, -corner], [-corner, -corner, -corner],
             [-corner, -corner, +corner], [-corner, +corner, +corner]],
            # Left face
            [[-corner, -corner, +corner], [-corner, -corner, -corner],
             [+corner, -corner, -corner], [+corner, -corner, +corner]],
            # Bottom face
            [[-corner, +corner, -corner], [-corner, +corner, +corner],
             [+corner, +corner, +corner], [+corner, +corner, -corner]],
            # Top face
            [[+corner, +corner, +corner], [-corner, +corner, +corner],
             [-corner, -corner, +corner], [+corner, -corner, +corner]],
            # Front face
            [[-corner, -corner, -corner], [-corner, +corner, -corner],
             [+corner, +corner, -corner], [+corner, -corner, -corner]]
            # Back face
        ]
        normals = [[+1, 0, 0], [-1, 0, 0], [0, -1, 0],
                   [0, +1, 0], [0, 0, +1], [0, 0, -1]]
        # Draw inside (reverse winding and normals)
        for face in range(self.skip_right_face, 6):
            pyglet.gl.glNormal3f(-normals[face][0], -normals[face][1],
                                 -normals[face][2])
            for vertex in range(0, 3):
                pyglet.gl.glVertex3f(pyglet.gl.GLfloat(vertices[face][3 - vertex][0]),
                           pyglet.gl.GLfloat(vertices[face][3 - vertex][1]),
                           pyglet.gl.GLfloat(vertices[face][3 - vertex][2]))
            for vertex in (0, 2, 3):
                pyglet.gl.glVertex3f(pyglet.gl.GLfloat(vertices[face][3 - vertex][0]),
                           pyglet.gl.GLfloat(vertices[face][3 - vertex][1]),
                           pyglet.gl.GLfloat(vertices[face][3 - vertex][2]))
        # Draw outside
        for face in range(self.skip_right_face, 6):
            pyglet.gl.glNormal3f(pyglet.gl.GLfloat(normals[face][0]),
                                 pyglet.gl.GLfloat(normals[face][1]),
                       pyglet.gl.GLfloat(normals[face][2]))
            for vertex in range(0, 3):
                pyglet.gl.glVertex3f(pyglet.gl.GLfloat(vertices[face][vertex][0]),
                           pyglet.gl.GLfloat(vertices[face][vertex][1]),
                           pyglet.gl.GLfloat(vertices[face][vertex][2]))
            for vertex in (0, 2, 3):
                pyglet.gl.glVertex3f(pyglet.gl.GLfloat(vertices[face][vertex][0]),
                           pyglet.gl.GLfloat(vertices[face][vertex][1]),
                           pyglet.gl.GLfloat(vertices[face][vertex][2]))