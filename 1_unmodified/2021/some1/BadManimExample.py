# ==============================================================================
# Scene:      BadManimExample
# Source:     videos/_2021/some1.py (lines 1164-1185)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BadManimExample.py BadManimExample -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BadManimExample(Scene):
    def construct(self):
        words = OldTexText(
            "Does any of this ",
            "need to be ",
            "animated?\\\\",
            "Much less programatically?"
        )
        words[-1].shift(MED_SMALL_BUFF * DOWN)
        words.set_width(FRAME_WIDTH - 2)

        self.play(Write(words[0]), run_time=1)
        self.play(FadeIn(words[1], scale=10, shift=0.25 * UP))
        self.play(TransformMatchingShapes(words[0].copy(), words[2], path_arc=PI / 2))
        self.wait()
        self.play(Transform(
            VGroup(*words[0], *words[1], *words[2]).copy(),
            words[3],
            lag_ratio=0.03,
            run_time=1
        ))
        self.wait()
