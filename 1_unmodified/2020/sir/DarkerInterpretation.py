# ==============================================================================
# Scene:      DarkerInterpretation
# Source:     videos/_2020/sir.py (lines 2370-2389)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DarkerInterpretation.py DarkerInterpretation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DarkerInterpretation(Scene):
    def construct(self):
        qz = OldTexText("Quarantine zone")
        qz.set_color(RED)
        qz.set_width(2)
        line = Line(qz.get_left(), qz.get_right())

        new_words = OldTexText("Deceased")
        new_words.replace(qz, dim_to_match=1)
        new_words.set_color(RED)

        self.add(qz)
        self.wait()
        self.play(ShowCreation(line))
        self.play(
            FadeOut(qz),
            FadeOut(line),
            FadeIn(new_words)
        )
        self.wait()
