#version 330

layout(location = 0) in vec3 vertex_postition;

out vec3 local_position;

void main(void){
    local_position = vertex_postition;
    gl_Position = vec4(vertex_postition, 1.0);
}
