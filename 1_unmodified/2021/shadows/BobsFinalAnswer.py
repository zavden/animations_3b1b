# ==============================================================================
# Scene:      BobsFinalAnswer
# Source:     videos/_2021/shadows.py (lines 5393-5434)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BobsFinalAnswer.py BobsFinalAnswer -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_overline(mob):
    overline = Underline(mob).next_to(mob, UP, buff=0.05)
    overline.set_stroke(WHITE, 2)
    return overline


class BobsFinalAnswer(Scene):
    def construct(self):
        answer = OldTex(
            "S(\\text{Cube})", "=",
            "\\frac{1}{2}", "\\cdot", "{\\frac{1}{2}}",
            "(\\text{Surface area})", "=",
            "\\frac{1}{4} \\big(6s^2\\big)", "=",
            "\\frac{3}{2} s^2",
            tex_to_color_map={
                "\\text{Cube}": BLUE,
                "{\\frac{1}{2}}": RED,
            }
        )
        answer.add_to_back(get_overline(answer[:3]))
        equals = answer.get_parts_by_tex("=")
        eq_indices = list(map(answer.index_of_part, equals))

        eq1 = answer[:eq_indices[1]].deepcopy()
        eq2 = answer[:eq_indices[2]].deepcopy()
        eq3 = answer.deepcopy()
        for eq in eq1, eq2, eq3:
            eq.to_edge(RIGHT)
            eq.shift(1.25 * UP)

        self.play(FadeIn(eq1, DOWN))
        self.wait()
        for m1, m2 in (eq1, eq2), (eq2, eq3):
            self.play(
                FadeIn(m2[len(m1):]),
                m1.animate.move_to(m2, LEFT),
            )
            self.remove(m1)
            self.add(m2)
            self.wait()

        rect = SurroundingRectangle(eq3[-1])
        rect.set_stroke(YELLOW, 2)
        self.play(
            ShowCreation(rect),
            FlashAround(eq3[-1], stroke_width=5, time_width=1.5, run_time=1.5)
        )
        self.wait()
