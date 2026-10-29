# ==============================================================================
# Scene:      ContrastDumbTrickAndLT
# Source:     videos/_2025/laplace/prequel_equations.py (lines 1560-1584)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ContrastDumbTrickAndLT.py ContrastDumbTrickAndLT -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ContrastDumbTrickAndLT(InteractiveScene):
    def construct(self):
        # Test
        kw = dict(font_size=60)
        titles = VGroup(
            Text("Dumb trick", **kw),
            Text("Laplace Transform", **kw),
        )
        underlines = VGroup()
        for x, title in zip([-1, 1], titles):
            title.set_x(x * FRAME_WIDTH / 4)
            title.to_edge(UP, buff=MED_SMALL_BUFF)
            underlines.add(Underline(title))
        underlines[0].scale(1.25)
        underlines[1].shift(SMALL_BUFF * UP)

        v_line = Line(UP, DOWN).set_height(FRAME_HEIGHT)

        self.play(
            LaggedStartMap(FadeIn, titles[::-1], lag_ratio=0.5),
            LaggedStartMap(ShowCreation, underlines[::-1], lag_ratio=0.5),
            ShowCreation(v_line, time_span=(0.5, 2.0)),
            run_time=2
        )
        self.wait()
