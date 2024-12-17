#version 330 core

in vec3 frag_position;
in vec3 frag_normal;
in vec2 frag_tex_coord;

out vec4 frag_color;

uniform sampler2D texture_diffuse; // Texture for the gun
uniform float time;                // Time uniform for animation
uniform vec3 light_color;          // Light color for the glow effect

void main() {
    // Compute a pulsating effect using sine wave
    float pulse = 0.5 + 0.5 * sin(time * 2.0); // Range from 0 to 1
    vec3 glow = light_color * pulse;

    // Combine the texture and pulsating glow
    vec3 tex_color = texture(texture_diffuse, frag_tex_coord).rgb;
    vec3 result = tex_color + glow;

    frag_color = vec4(result, 1.0);
}
