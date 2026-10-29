# ==============================================================================
# Scene:      LayersOfLightbulbs
# Source:     videos/_2017/cba.py (lines 355-389)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LayersOfLightbulbs.py LayersOfLightbulbs -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LayersOfLightbulbs(Scene):
    CONFIG = {
        "random_seed": 1,
    }

    def construct(self):
        layers = VGroup()
        for x in range(6):
            n_dots = 5 + (x % 2)
            dots = VGroup(*[Dot() for x in range(n_dots)])
            dots.scale(2)
            dots.arrange(RIGHT, buff=MED_LARGE_BUFF)
            dots.set_stroke(WHITE, 2)
            for dot in dots:
                dot.set_fill(YELLOW, np.random.random())
            layers.add(dots)

        layers.arrange(UP, buff=LARGE_BUFF)

        lines = VGroup()
        for l1, l2 in zip(layers, layers[1:]):
            for d1, d2 in it.product(l1, l2):
                color = interpolate_color(
                    YELLOW, GREEN, np.random.random()
                )
                line = Line(
                    d1.get_center(),
                    d2.get_center(),
                    buff=(d1.get_width() / 2),
                    color=color,
                    stroke_width=2 * np.random.random(),
                )
                lines.add(line)

        self.add(layers, lines)
