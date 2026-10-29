# ==============================================================================
# Scene:      ExamplePixels
# Source:     videos/_2021/newton_fractal.py (lines 458-494)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ExamplePixels.py ExamplePixels -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/data/sphere_pixel_values.npy (synthetic data: 5x5 BGR patch over a shaded sphere; generator _lib/assets/generated/2021/newton_fractal/make_newton_fractal_assets.py)
# ==============================================================================

from manim_imports_ext import *

class ExamplePixels(Scene):
    def construct(self):
        pixels = Square().get_grid(5, 5, buff=0)
        pixels.set_height(2)
        pixels.to_corner(UL)
        pixels.set_stroke(WHITE, 1)
        pixels.set_fill(BLACK, 1)
        self.add(pixels)

        y, x = 1066, 1360

        endpoint = np.array([x, -y, 0], dtype=np.float)
        endpoint *= FRAME_HEIGHT / 2160
        endpoint += np.array([-FRAME_WIDTH / 2, FRAME_HEIGHT / 2, 0])
        lines = VGroup(
            Line(pixels.get_corner(UR), endpoint),
            Line(pixels.get_corner(DL), endpoint),
        )
        lines.set_stroke(WHITE, 2)
        self.add(lines)

        def match_values(pixels, values):
            for pixel, value in zip(pixels, it.chain(*values)):
                value = value[::-1]
                pixel.set_fill(rgb_to_color(value / 255))

        values = np.load(
            os.path.join(get_directories()["data"], "sphere_pixel_values.npy")
        )
        match_values(pixels, values[0])
        # for value in values[60::60]:
        for value in values[1:]:
            # pixels.generate_target()
            # match_values(pixels.target, value)
            # self.play(MoveToTarget(pixels))
            match_values(pixels, value)
            self.wait(1 / 60)
