#version 330 core

layout(location = 0) in vec3 in_position;  // Vertex position
layout(location = 1) in vec3 in_normal;    // Vertex normal
layout(location = 2) in vec2 in_tex_coord; // Texture coordinates

out vec3 frag_position;  // Position in world space (for lighting calculations)
out vec3 frag_normal;    // Normal in world space
out vec2 frag_tex_coord; // Texture coordinates passed to fragment shader

uniform mat4 model;      // Model transformation matrix
uniform mat4 view;       // View (camera) transformation matrix
uniform mat4 projection; // Projection matrix

void main() {
    frag_position = vec3(model * vec4(in_position, 1.0));
    frag_normal = mat3(transpose(inverse(model))) * in_normal; // Correct normal for transformations
    frag_tex_coord = in_tex_coord;

    gl_Position = projection * view * vec4(frag_position, 1.0);
}