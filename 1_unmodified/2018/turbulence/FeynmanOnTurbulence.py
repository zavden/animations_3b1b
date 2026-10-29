# ==============================================================================
# Scene:      FeynmanOnTurbulence
# Source:     videos/_2018/turbulence.py (lines 953-976)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FeynmanOnTurbulence.py FeynmanOnTurbulence -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FeynmanOnTurbulence(Scene):
    def construct(self):
        feynman = ImageMobject("Feynman_Woods", height=4)
        name = OldTexText("Richard Feynman")
        name.next_to(feynman, DOWN)
        quote = OldTexText(
            "``", "Turbulence", "is the most\\\\"
            "important", "unsolved problem\\\\",
            "of classical physics.''",
            tex_to_color_map={
                "Turbulence": BLUE,
                "unsolved problem\\\\": YELLOW,
            },
        )
        quote[0].shift(SMALL_BUFF * RIGHT)
        quote.next_to(feynman, RIGHT)
        Group(feynman, name, quote).center()

        self.play(
            FadeIn(feynman, UP),
            FadeIn(name, DOWN),
            Write(quote, run_time=4)
        )
        self.wait()
