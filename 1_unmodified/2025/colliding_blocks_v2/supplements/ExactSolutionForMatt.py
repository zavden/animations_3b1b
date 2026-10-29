# ==============================================================================
# Scene:      ExactSolutionForMatt
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 1016-1091)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExactSolutionForMatt.py ExactSolutionForMatt -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ExactSolutionForMatt(InteractiveScene):
    def construct(self):
        # Answer
        kw = dict(
            t2c={
                R"\theta": YELLOW,
                R"m_1": BLUE,
                R"m_2": BLUE,
                R"\pi": WHITE
            }
        )
        equations = VGroup(
            Tex(R"\#\text{Collisions} = {\pi \over \text{arctan}\left(\sqrt{m_2 / m_1}\right)}", **kw),
            Tex(R"\#\text{Collisions} \approx {\pi \over \sqrt{m_2 / m_1}}", **kw),
            Tex(R"\#\text{Collisions} \approx \pi \cdot \sqrt{m_1 / m_2}", **kw),
        )
        for eq in equations[:2]:
            eq[R"\pi"].scale(2, about_edge=DOWN)
        equations[2][R"\pi"].scale(1.5, about_edge=DOWN).shift(0.05 * RIGHT)

        rect = SurroundingRectangle(equations[0][len("#Collisions="):])
        rect.set_stroke(YELLOW, 2)
        words = VGroup(
            Text("If fractional, round down").set_color(YELLOW),
            TexText("If whole...").set_color(GREEN),
        )
        for word in words:
            word.next_to(rect, UP)

        minus_1 = Tex(R"-1", font_size=60)
        minus_1.next_to(equations[0][R"\over"], RIGHT)

        self.play(FadeIn(equations[0], lag_ratio=0.25))
        self.wait()
        self.play(ShowCreation(rect), FadeIn(words[0], 0.25 * UP))
        self.wait()
        self.play(
            rect.animate.set_color(GREEN),
            FadeTransformPieces(words[0], words[1], run_time=1),
        )
        self.play(Write(minus_1))
        self.wait()
        self.play(LaggedStart(FadeOut(rect), FadeOut(words[1]), FadeOut(minus_1)))

        # Pi creature
        randy = Randolph()
        pi = equations[0][R"\pi"][0][0]
        randy.scale(pi.get_height() / randy.body.get_height())
        randy.shift(pi.get_center() - randy.body.get_center())

        self.play(
            FadeOut(pi),
            FadeIn(randy)
        )
        self.play(randy.change("hooray", DOWN))
        self.play(Blink(randy))
        self.play(FadeOut(randy), FadeIn(pi))

        # Cross out arctan
        exmark = Cross(equations[0][R"\text{arctan}"])
        self.play(ShowCreation(exmark))
        self.wait()
        self.play(
            FadeOut(exmark),
            TransformMatchingTex(equations[0], equations[1]),
        )
        self.wait()
        self.play(
            TransformMatchingTex(
                equations[1],
                equations[2],
                matched_keys=["m_1", "m_2", R"\sqrt"],
                path_arc=45 * DEG
            )
        )
        self.wait()
