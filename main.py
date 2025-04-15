import ctypes
import pyglet

pyglet.options["shadow_window"] = False
pyglet.options["debug_gl"] = False

import pyglet.gl as gl

# Vertex and index data
vertex_positions = [
    -0.5,  0.5,  # top-left
    -0.5, -0.5,  # bottom-left
     0.5, -0.5,  # bottom-right
     0.5,  0.5   # top-right
]

indices = [
    0, 1, 2,
    0, 2, 3
]

# Vertex and fragment shader sources
vertex_shader_source = b"""
#version 330 core
layout(location = 0) in vec2 position;

void main()
{
    gl_Position = vec4(position, 0.0, 1.0);
}
"""

fragment_shader_source = b"""
#version 330 core
out vec4 FragColor;

void main()
{
    FragColor = vec4(1.0, 1.0, 1.0, 1.0); // White color
}
"""

# Helper to compile shader
def compile_shader(source, shader_type):
    shader = gl.glCreateShader(shader_type)

    source_buffer = ctypes.create_string_buffer(source)
    buffer_pointer = ctypes.cast(
        ctypes.pointer(ctypes.pointer(source_buffer)),
        ctypes.POINTER(ctypes.POINTER(gl.GLchar))
    )

    gl.glShaderSource(shader, 1, buffer_pointer, None)
    gl.glCompileShader(shader)

    # Check for compile errors
    success = gl.GLint()
    gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS, ctypes.byref(success))
    if not success.value:
        log = ctypes.create_string_buffer(512)
        gl.glGetShaderInfoLog(shader, 512, None, log)
        raise RuntimeError(f"Shader compile failed: {log.value.decode()}")

    return shader

# Helper to link shader program
def create_shader(vertex_src, fragment_src):
    vertex_shader = compile_shader(vertex_src, gl.GL_VERTEX_SHADER)
    fragment_shader = compile_shader(fragment_src, gl.GL_FRAGMENT_SHADER)

    program = gl.glCreateProgram()
    gl.glAttachShader(program, vertex_shader)
    gl.glAttachShader(program, fragment_shader)
    gl.glLinkProgram(program)

    # Check for link errors
    success = gl.GLint()
    gl.glGetProgramiv(program, gl.GL_LINK_STATUS, ctypes.byref(success))
    if not success:
        log = ctypes.create_string_buffer(512)
        gl.glGetProgramInfoLog(program, 512, None, log)
        raise RuntimeError(f"Program link failed: {log.value.decode()}")

    # Clean up shaders (they're linked now)
    gl.glDeleteShader(vertex_shader)
    gl.glDeleteShader(fragment_shader)

    return program

class Window(pyglet.window.Window):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.shader = create_shader(vertex_shader_source, fragment_shader_source)
        gl.glUseProgram(self.shader)

        # Create and bind VAO
        self.vao = gl.GLuint()
        gl.glGenVertexArrays(1, ctypes.byref(self.vao))
        gl.glBindVertexArray(self.vao)

        # Create VBO
        self.vbo = gl.GLuint()
        gl.glGenBuffers(1, ctypes.byref(self.vbo))
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)

        array_type = gl.GLfloat * len(vertex_positions)
        gl.glBufferData(gl.GL_ARRAY_BUFFER,
                        ctypes.sizeof(array_type),
                        array_type(*vertex_positions),
                        gl.GL_STATIC_DRAW)

        # Define vertex layout
        gl.glVertexAttribPointer(0, 2, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(0)

        # Create IBO
        self.ibo = gl.GLuint()
        gl.glGenBuffers(1, ctypes.byref(self.ibo))
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ibo)

        index_type = gl.GLuint * len(indices)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER,
                        ctypes.sizeof(index_type),
                        index_type(*indices),
                        gl.GL_STATIC_DRAW)

    def on_draw(self):
        gl.glClearColor(1.0, 0.5, 1.0, 1.0)  # Pink background
        self.clear()

        gl.glUseProgram(self.shader)
        gl.glBindVertexArray(self.vao)
        gl.glDrawElements(gl.GL_TRIANGLES, len(indices), gl.GL_UNSIGNED_INT, None)

    def on_resize(self, width, height):
        gl.glViewport(0, 0, width, height)
        print(f"Resized: {width}x{height}")

class Game:
    def __init__(self):
        self.config = gl.Config(major_version=3, forward_compatible=True, double_buffer=True)
        self.window = Window(config=self.config, width=800, height=600, caption="minecraft", resizable=True, vsync=False)

    def run(self):
        pyglet.app.run()

if __name__ == "__main__":
    game = Game()
    game.run()
