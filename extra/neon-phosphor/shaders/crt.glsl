// Phosphor CRT: slight tube curvature, neon bloom, scanlines, vignette.
// Static (no iTime), so custom-shader-animation can stay off.

const float CURVATURE = 0.03;  // 0.0 = flat glass
const float BLOOM     = 0.35;  // neon glow strength
const float SCANLINE  = 0.14;  // 0.0 = no scanlines
const float VIGNETTE  = 0.9;

void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 uv = fragCoord / iResolution.xy;

    // Barrel distortion
    vec2 cc = uv - 0.5;
    float dist = dot(cc, cc);
    uv += cc * dist * CURVATURE;
    if (uv.x < 0.0 || uv.x > 1.0 || uv.y < 0.0 || uv.y > 1.0) {
        fragColor = vec4(0.0);  // transparent outside the curved glass
        return;
    }

    // Ghostty passes premultiplied alpha; keep it so background-opacity works.
    vec4 base = texture(iChannel0, uv);
    vec3 col = base.rgb;

    // Bloom: cheap 5x5 box blur added back on top
    vec2 px = 1.5 / iResolution.xy;
    vec4 glow = vec4(0.0);
    for (int x = -2; x <= 2; x++) {
        for (int y = -2; y <= 2; y++) {
            glow += texture(iChannel0, uv + vec2(x, y) * px);
        }
    }
    col += (glow.rgb / 25.0) * BLOOM;
    float alpha = base.a;  // glow brightens colour only; never adds opacity

    // Scanlines (2px period)
    col *= (1.0 - SCANLINE) + SCANLINE * sin(fragCoord.y * 3.14159);

    // Vignette
    col *= 1.0 - dist * VIGNETTE;

    fragColor = vec4(col, alpha);
}
