# ==============================================================================
# Scene:      SmallAngleApproximationTex
# Source:     videos/_2019/diffyq/part1/wordy_scenes.py (lines 5-35)
# Category:   1 · Renders unmodified
# Includes code copied from: _2019/diffyq/part1/shared_constructs.py
#
# Run from this folder:
#     manimgl SmallAngleApproximationTex.py SmallAngleApproximationTex -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2019/diffyq/part1/shared_constructs.py -----

Lg_formula_config = {
    "tex_to_color_map": {
        "\\theta_0": WHITE,
        "{L}": BLUE,
        "{g}": YELLOW,
    },
}



# ----- From _2019/diffyq/part1/wordy_scenes.py -----

class SmallAngleApproximationTex(Scene):
    def construct(self):
        approx = OldTex(
            "\\sin", "(", "\\theta", ") \\approx \\theta",
            tex_to_color_map={"\\theta": RED},
            arg_separator="",
        )

        implies = OldTex("\\Downarrow")
        period = OldTex(
            "\\text{Period}", "\\approx",
            "2\\pi \\sqrt{\\,{L} / {g}}",
            **Lg_formula_config,
        )
        group = VGroup(approx, implies, period)
        group.arrange(DOWN)

        approx_brace = Brace(approx, UP, buff=SMALL_BUFF)
        approx_words = OldTexText(
            "For small $\\theta$",
            tex_to_color_map={"$\\theta$": RED},
        )
        approx_words.scale(0.75)
        approx_words.next_to(approx_brace, UP, SMALL_BUFF)

        self.add(approx, approx_brace, approx_words)
        self.play(
            Write(implies),
            FadeIn(period, LEFT)
        )
        self.wait()
