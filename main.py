import pyglet
import math
from pyglet import gl
import ctypes
from shader import Shader
import matrix

class Window(pyglet.window.Window):
    def __init__(self, config=None, **kwargs):
        super().__init__(config=config, **kwargs)

        self.vertices = [
            -0.5, -0.5, 0.0,
             0.5, -0.5, 0.0,
             0.5,  0.5, 0.0,
            -0.5,  0.5, 0.0
        ]
        self.vertices = (gl.GLfloat * len(self.vertices))(*self.vertices)

        self.indices = [0, 1, 2, 2, 3, 0]
        self.indices = (gl.GLuint * len(self.indices))(*self.indices)

        self.vao = gl.GLuint()
        gl.glGenVertexArrays(1, ctypes.byref(self.vao))
        gl.glBindVertexArray(self.vao)

        self.vbo = gl.GLuint()
        gl.glGenBuffers(1, ctypes.byref(self.vbo))
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, ctypes.sizeof(self.vertices), self.vertices, gl.GL_STATIC_DRAW)

        self.ebo = gl.GLuint()
        gl.glGenBuffers(1, ctypes.byref(self.ebo))
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, ctypes.sizeof(self.indices), self.indices, gl.GL_STATIC_DRAW)

        gl.glEnableVertexAttribArray(0)
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(0))

        self.shader = Shader("vert.glsl", "frag.glsl")
        self.shader_matrix_location = self.shader.find_uniform(b"matrix")
        self.shader.use()

        self.mv_matrix = matrix.Matrix()
        self.p_matrix = matrix.Matrix()
        self.x = 0

        pyglet.clock.schedule_interval(self.update, 1.0 / 60)

    def on_resize(self, width, height):
        super().on_resize(width, height)
        gl.glViewport(0, 0, width, height)

    def update(self, dt):
        self.x += dt

    def on_draw(self):
        gl.glClearColor(1.0, 0.5, 1.0, 1.0)  # Pink background
        self.clear()

        self.p_matrix.load_identity()
        self.p_matrix.perspective(90, float(self.width) / self.height, 0.1, 100)

        self.mv_matrix.load_identity()
        self.mv_matrix.translate(0, 0, -2)
        self.mv_matrix.rotate_2d(self.x, self.x / 2)

        mvp_matrix = self.mv_matrix * self.p_matrix
        self.shader.uniform_matrix(self.shader_matrix_location, mvp_matrix)

        self.shader.use()
        gl.glBindVertexArray(self.vao)
        gl.glDrawElements(gl.GL_TRIANGLES, 6, gl.GL_UNSIGNED_INT, ctypes.c_void_p(0))

class Game:
    def __init__(self):
        config = gl.Config(major_version=3, minor_version=3, forward_compatible=True, double_buffer=True)
        self.window = Window(config=config, width=800, height=600, caption="minecraft", resizable=True)

    def run(self):
        pyglet.app.run()

if __name__ == "__main__":
    game = Game()
    game.run()
