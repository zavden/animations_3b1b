# ==============================================================================
# Scene:      GeneralWordForMeasurement
# Source:     videos/_2017/fractal_dimension.py (lines 730-761)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GeneralWordForMeasurement.py GeneralWordForMeasurement -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GeneralWordForMeasurement(Scene):
    def construct(self):
        measure = OldTexText("``Measure''")
        measure.to_edge(UP)
        mass = OldTexText("Mass")
        mass.move_to(measure)

        words = VGroup(*list(map(TexText, [
            "Length", "Area", "Volume"
        ])))
        words.arrange(RIGHT, buff = 2*LARGE_BUFF)
        words.next_to(measure, DOWN, buff = 2*LARGE_BUFF)
        colors = color_gradient([BLUE_B, BLUE_D], len(words))
        for word, color in zip(words, colors):
            word.set_color(color)
        lines = VGroup(*[
            Line(
                measure.get_bottom(), word.get_top(),
                color = word.get_color(),
                buff = MED_SMALL_BUFF
            )
            for word in words
        ])

        for word in words:
            self.play(FadeIn(word))
        self.play(ShowCreation(lines, run_time = 2))
        self.wait()
        self.play(Write(measure))
        self.wait(2)
        self.play(Transform(measure, mass))
        self.wait(2)
