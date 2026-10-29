# ==============================================================================
# Scene:      DimensionForNaturalNumbers
# Source:     videos/_2017/fractal_dimension.py (lines 548-568)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DimensionForNaturalNumbers.py DimensionForNaturalNumbers -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DimensionForNaturalNumbers(Scene):
    def construct(self):
        labels = VGroup(*[
            OldTexText("%d-dimensional"%d)
            for d in (1, 2, 3)
        ])
        for label, vect in zip(labels, [LEFT, ORIGIN, RIGHT]):
            label.to_edge(vect)
        labels.shift(2*DOWN)

        line = Line(DOWN+LEFT, 3*UP+RIGHT, color = BLUE)
        line.next_to(labels[0], UP)

        self.play(
            Write(labels[0]),
            ShowCreation(line)
        )
        self.wait()
        for label in labels[1:]:
            self.play(Write(label))
            self.wait()
