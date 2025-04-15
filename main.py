import pyglet
from pyglet import gl
import ctypes
from shader import Shader  # Make sure shader.py exists with a Shader class

class Window(pyglet.window.Window):
    def __init__(self, config=None, **kwargs):
        super().__init__(config=config, **kwargs)
        
        # Rectangle vertices (4 corners)
        self.vertices = [
            -0.5, -0.5, 0.0,  # Bottom Left
             0.5, -0.5, 0.0,  # Bottom Right
             0.5,  0.5, 0.0,  # Top Right
            -0.5,  0.5, 0.0   # Top Left
        ]
        self.vertices = (gl.GLfloat * len(self.vertices))(*self.vertices)

        # Indices for 2 triangles (forming a rectangle)
        self.indices = [
            0, 1, 2,  # First Triangle
            2, 3, 0   # Second Triangle
        ]
        self.indices = (gl.GLuint * len(self.indices))(*self.indices)

        # Vertex Array Object
        self.vao = gl.GLuint()
        gl.glGenVertexArrays(1, ctypes.byref(self.vao))
        gl.glBindVertexArray(self.vao)

        # Vertex Buffer Object
        self.vbo = gl.GLuint()
        gl.glGenBuffers(1, ctypes.byref(self.vbo))
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, ctypes.sizeof(self.vertices), self.vertices, gl.GL_STATIC_DRAW)

        # Element Buffer Object
        self.ebo = gl.GLuint()
        gl.glGenBuffers(1, ctypes.byref(self.ebo))
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, ctypes.sizeof(self.indices), self.indices, gl.GL_STATIC_DRAW)

        # Vertex Attribute Pointer
        gl.glEnableVertexAttribArray(0)
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 3 * ctypes.sizeof(gl.GLfloat), ctypes.c_void_p(0))

        # Load shader
        self.shader = Shader("vert.glsl", "frag.glsl")

    def on_draw(self):
        self.clear()
        gl.glUseProgram(self.shader.program)
        gl.glBindVertexArray(self.vao)
        gl.glDrawElements(gl.GL_TRIANGLES, 6, gl.GL_UNSIGNED_INT, ctypes.c_void_p(0))

class Game:
    def __init__(self):
        config = gl.Config(double_buffer=True)
        self.window = Window(config=config, width=800, height=600, caption="minecraft", resizable=True)

    def run(self):
        pyglet.app.run()

if __name__ == "__main__":
    game = Game()
    game.run()
