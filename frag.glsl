#version 330 core

in vec3 local_position;
out vec4 fragment_colour;

void main() {
    fragment_colour = vec4(local_position * 0.5 + 0.5, 1.0); // smooth color from position
}
