import ctypes
import pyglet.gl as gl

class ShaderError(Exception):
    def __init__(self, message):
        super().__init__(message)

def create_shader(target, source_path):
    # Read shader source
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

    # Check for shader compilation errors
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

        # Create and compile vertex shader
        self.vert_shader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        create_shader(self.vert_shader, vert_path)
        gl.glAttachShader(self.program, self.vert_shader)

        # Create and compile fragment shader
        self.frag_shader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        create_shader(self.frag_shader, frag_path)
        gl.glAttachShader(self.program, self.frag_shader)

        # Link program
        gl.glLinkProgram(self.program)

        # Check for linking errors
        status = ctypes.c_int()
        gl.glGetProgramiv(self.program, gl.GL_LINK_STATUS, ctypes.byref(status))
        if not status.value:
            log_length = ctypes.c_int()
            gl.glGetProgramiv(self.program, gl.GL_INFO_LOG_LENGTH, ctypes.byref(log_length))

            log_buffer = ctypes.create_string_buffer(log_length.value)
            gl.glGetProgramInfoLog(self.program, log_length, None, log_buffer)

            raise ShaderError(f"Program link error: {log_buffer.value.decode()}")

        # Clean up shaders
        gl.glDeleteShader(self.vert_shader)
        gl.glDeleteShader(self.frag_shader)

    def use(self):
        gl.glUseProgram(self.program)

    def __del__(self):
        try:
            gl.glDeleteProgram(self.program)
        except Exception:
            pass
