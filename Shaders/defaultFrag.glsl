#version 330 core

in vec3 frag_position;  // Interpolated world-space position
in vec3 frag_normal;    // Interpolated world-space normal
in vec2 frag_tex_coord; // Interpolated texture coordinates

out vec4 frag_color;    // Output color

uniform sampler2D texture_diffuse; // Diffuse texture
uniform vec3 light_position;       // Light position in world space
uniform vec3 light_color;          // Light color
uniform vec3 view_position;        // Camera position in world space

void main() {
    // Ambient lighting
    vec3 ambient = 0.1 * light_color;

    // Diffuse lighting
    vec3 light_dir = normalize(light_position - frag_position);
    float diff = max(dot(frag_normal, light_dir), 0.0);
    vec3 diffuse = diff * light_color;

    // Specular lighting
    vec3 view_dir = normalize(view_position - frag_position);
    vec3 reflect_dir = reflect(-light_dir, frag_normal);
    float spec = pow(max(dot(view_dir, reflect_dir), 0.0), 32.0);
    vec3 specular = 0.5 * spec * light_color;

    // Combine results
    vec3 result = (ambient + diffuse + specular) * texture(texture_diffuse, frag_tex_coord).rgb;
    frag_color = vec4(result, 1.0);
}