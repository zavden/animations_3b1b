# ==============================================================================
# Scene:      ExplanationOneTitle
# Source:     videos/_2025/laplace/derivative_supplements.py (lines 552-577)
# Category:   1 · Renders unmodified
# Includes code copied from: _2025/laplace/derivatives.py
#
# Run from this folder:
#     manimgl ExplanationOneTitle.py ExplanationOneTitle -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2025/laplace/derivatives.py -----

tex_to_color = {
    "{t}": BLUE,
    "{s}": YELLOW,
}



# ----- From _2025/laplace/derivative_supplements.py -----

class ExplanationOneTitle(InteractiveScene):
    def construct(self):
        t2c = dict(tex_to_color)
        title = VGroup(
            Text("Explanation #1: Try it for"),
            Tex(R"e^{a{t}}", t2c=t2c)
        )
        title.arrange(RIGHT)
        title[1].shift(SMALL_BUFF * UP)
        title.to_corner(UL)
        alt_formula = Tex(R"c_1 e^{a_1 {t}} + c_2 e^{a_2 {t}} + \cdots + c_n e^{a_n {t}}", t2c=t2c)
        alt_formula[re.compile(r"c_.")].set_color(TEAL_D)
        alt_formula.move_to(title[1], LEFT)
        ponder_words = Text("(Pause and ponder to taste)")
        ponder_words.set_fill(GREY_B)
        ponder_words.move_to(title)
        ponder_words.to_edge(RIGHT, buff=SMALL_BUFF)

        self.add(title)
        self.play(Write(ponder_words))
        self.wait()
        self.play(
            TransformMatchingTex(title[1], alt_formula),
            FadeOut(ponder_words, lag_ratio=0.1),
        )
        self.wait()
