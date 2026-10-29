# ==============================================================================
# Scene:      TitleCard
# Source:     videos/_2025/laplace/derivative_supplements.py (lines 86-105)
# Category:   1 · Renders unmodified
# Includes code copied from: _2025/laplace/derivatives.py
#
# Run from this folder:
#     manimgl TitleCard.py TitleCard -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2025/laplace/derivatives.py -----

tex_to_color = {
    "{t}": BLUE,
    "{s}": YELLOW,
}



# ----- From _2025/laplace/derivative_supplements.py -----

class TitleCard(InteractiveScene):
    def construct(self):
        # Test
        self.add(FullScreenRectangle().set_fill(GREY_E, 1))
        title = Text("Laplace Transform ", font_size=72)
        tex = Tex(
            R"F({s}) = \int^\infty_0 f({t})e^{\minus{s}{t}} d{t}",
            t2c=tex_to_color,
            font_size=60
        )
        # VGroup(title, tex).arrange(RIGHT, buff=MED_LARGE_BUFF).to_edge(UP)
        title.center().to_edge(UP)

        self.play(Write(title))
        # self.play(LaggedStart(
        #     FadeIn(title, 0.5 * LEFT, lag_ratio=0.01),
        #     FadeIn(tex, lag_ratio=0.1),
        #     lag_ratio=0.2
        # ))
        self.wait()
