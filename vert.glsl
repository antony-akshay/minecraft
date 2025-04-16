#version 330 core

layout(location = 0) in vec3 vertex_position;

uniform mat4 matrix;
out vec3 local_position;

void main() {
    local_position = vertex_position;
    gl_Position = matrix * vec4(vertex_position, 1.0);
}
