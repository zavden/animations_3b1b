# ==============================================================================
# Scene:      WellOfSyene
# Source:     videos/_2025/cosmic_distance/supplements.py (lines 590-620)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl WellOfSyene.py WellOfSyene -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The illustration is looked up in KurtArtwork/ next to this file (before: Grant's folder) and is a placeholder.
#
# Placeholder assets (not Grant's originals):
#   - KurtArtwork/TheWellOfSyene.jpg (stone well with water, placeholder)
# ==============================================================================

from manim_imports_ext import *

class WellOfSyene(InteractiveScene):
    def construct(self):
        # Test
        # CHANGE: the illustration lived in KurtArtwork/ next to Grant's video output; now there is a placeholder in KurtArtwork/ next to this file.
        image_path = Path(__file__).parent / "KurtArtwork" / "TheWellOfSyene.jpg"
        image = TexturedSurface(Square3D(resolution=(101, 101)), image_path)
        image.set_shape(FRAME_WIDTH, FRAME_HEIGHT)
        image.set_shading(0.1, 0.1, 0.1)
        self.add(image)

        # Make waves
        frame = self.frame
        center = np.array([-2.3, 0.84, 0])

        sun_spot = GlowDot([-2.36, 1.26, 0.0])
        sun_spot.set_color(WHITE)
        sun_spot.set_radius(0.7)

        def wave(x, y, z, t):
            dist = get_dist(center, [x, y, z])
            scale = 0.025 * np.exp(-2 * dist * dist)
            nudge1 = scale * math.sin(2 * TAU * x - 5 * TAU * t)
            nudge2 = 3 * scale * math.sin(3 * TAU * y - 5 * TAU * t)
            return (x, y + nudge1, z + nudge2)

        frame.reorient(0, 0, 0, (-1.64, 0.72, 0.0), 2.39)
        self.play(
            Homotopy(wave, image, rate_func=linear),
            frame.animate.to_default_state(),
            GrowFromCenter(sun_spot, time_span=(5.5, 6.5)),
            run_time=12,
        )
