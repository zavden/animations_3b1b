# ==============================================================================
# Scene:      NameIntro
# Source:     videos/_2019/clacks/question.py (lines 387-424)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NameIntro.py NameIntro -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NameIntro(Scene):
    def construct(self):
        name = OldTexText("3Blue", "1Brown", arg_separator="")
        blue, brown = name
        name.scale(2.5)
        for part in name:
            part.save_state()
        brown.to_edge(RIGHT, buff=0)
        flash_time = 0.75

        self.add(blue, brown)
        self.play(
            VFadeIn(blue),
            VFadeIn(brown),
            Restore(brown, rate_func=linear),
        )
        self.play(
            Flash(blue.get_right(), run_time=flash_time),
            ApplyMethod(
                blue.to_edge, LEFT, {"buff": 0},
                rate_func=linear,
            ),
        )
        self.play(
            Flash(blue.get_left(), run_time=flash_time),
            Restore(blue, rate_func=linear),
        )
        self.play(
            Flash(blue.get_right(), run_time=flash_time),
            ApplyMethod(
                brown.to_edge, RIGHT, {"buff": 0},
                rate_func=linear,
            )
        )
        self.play(
            Flash(brown.get_right(), run_time=flash_time),
            Restore(brown, rate_func=linear)
        )
