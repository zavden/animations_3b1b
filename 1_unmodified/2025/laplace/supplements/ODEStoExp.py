# ==============================================================================
# Scene:      ODEStoExp
# Source:     videos/_2025/laplace/supplements.py (lines 661-695)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ODEStoExp.py ODEStoExp -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ODEStoExp(InteractiveScene):
    def construct(self):
        # Test
        odes, exp = words = VGroup(
            Text("Differential\nEquations"),
            Tex("e^{st}", t2c={"s": YELLOW}, font_size=72),
        )
        exp.match_height(odes)
        words.arrange(RIGHT, buff=3.0)
        words.to_edge(UP, buff=1.25)

        top_arrow, low_arrow = arrows = VGroup(
            Arrow(odes.get_corner(UR), exp.get_corner(UL), path_arc=-60 * DEG, thickness=5),
            Arrow(exp.get_corner(DL), odes.get_corner(DR), path_arc=-60 * DEG, thickness=5),
        )
        arrows.set_fill(TEAL)

        top_words = Tex(R"Explain", font_size=36).next_to(top_arrow, UP, SMALL_BUFF)
        low_words = Tex(R"Solves", font_size=36).next_to(low_arrow, DOWN, SMALL_BUFF)

        exp.shift(0.25 * UP + 0.05 * LEFT)

        self.add(words)
        self.wait()
        self.play(
            Write(top_arrow),
            Write(top_words),
        )
        self.wait()
        self.play(
            # Write(low_arrow),
            TransformFromCopy(top_arrow, low_arrow, path_arc=-PI),
            Write(low_words),
        )
        self.wait()
