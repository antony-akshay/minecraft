import ctypes
import pyglet.gl as gl

class ShaderError(Exception):
    def __init__(self, message):
        super().__init__(message)

def create_shader(target, source_path):
    with open(source_path, "rb") as source_file:
        source = source_file.read()

    source_length = ctypes.c_int(len(source) + 1)
    source_buffer = ctypes.create_string_buffer(source)

    buffer_pointer = ctypes.cast(
        ctypes.pointer(ctypes.pointer(source_buffer)),
        ctypes.POINTER(ctypes.POINTER(ctypes.c_char))
    )

    gl.glShaderSource(target, 1, buffer_pointer, ctypes.byref(source_length))
    gl.glCompileShader(target)

    status = ctypes.c_int()
    gl.glGetShaderiv(target, gl.GL_COMPILE_STATUS, ctypes.byref(status))

    if not status.value:
        log_length = ctypes.c_int()
        gl.glGetShaderiv(target, gl.GL_INFO_LOG_LENGTH, ctypes.byref(log_length))
        log_buffer = ctypes.create_string_buffer(log_length.value)
        gl.glGetShaderInfoLog(target, log_length, None, log_buffer)
        raise ShaderError(f"Shader compile error: {log_buffer.value.decode()}")

class Shader:
    def __init__(self, vert_path, frag_path):
        self.program = gl.glCreateProgram()

        self.vert_shader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        create_shader(self.vert_shader, vert_path)
        gl.glAttachShader(self.program, self.vert_shader)

        self.frag_shader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        create_shader(self.frag_shader, frag_path)
        gl.glAttachShader(self.program, self.frag_shader)

        gl.glLinkProgram(self.program)

        status = ctypes.c_int()
        gl.glGetProgramiv(self.program, gl.GL_LINK_STATUS, ctypes.byref(status))
        if not status.value:
            log_length = ctypes.c_int()
            gl.glGetProgramiv(self.program, gl.GL_INFO_LOG_LENGTH, ctypes.byref(log_length))
            log_buffer = ctypes.create_string_buffer(log_length.value)
            gl.glGetProgramInfoLog(self.program, log_length, None, log_buffer)
            raise ShaderError(f"Program link error: {log_buffer.value.decode()}")

        gl.glDeleteShader(self.vert_shader)
        gl.glDeleteShader(self.frag_shader)

    def use(self):
        gl.glUseProgram(self.program)

    def find_uniform(self, name):
        return gl.glGetUniformLocation(self.program, ctypes.create_string_buffer(name))

    def uniform_matrix(self, location, matrix):
        flat_matrix = sum(matrix.data, [])
        gl.glUniformMatrix4fv(location, 1, gl.GL_FALSE, (gl.GLfloat * 16)(*flat_matrix))

    def __del__(self):
        try:
            gl.glDeleteProgram(self.program)
        except Exception:
            pass
