# ==============================================================================
# Scene:      ProblemsWhereComplexNumbersArise
# Source:     videos/_2018/quaternions.py (lines 1766-1806)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ProblemsWhereComplexNumbersArise.py ProblemsWhereComplexNumbersArise -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - iterate over a copy: Cairo iterated split() (a new list) while GL iterates the live submobjects list, so adding the dots inside the loop made it visit the dots too
# ==============================================================================

from manim_imports_ext import *

class ProblemsWhereComplexNumbersArise(Scene):
    def construct(self):
        text = "Problems where complex numbers are surprisingly useful"
        title = OldTexText(*text.split(" "))
        title.to_edge(UP)
        title.set_color(BLUE)
        underline = Line(LEFT, RIGHT)
        underline.set_width(title.get_width() + 0.5)
        underline.next_to(title, DOWN)

        problems = VGroup(
            OldTexText(
                "Integer solutions to\\\\ $a^2 + b^2 = c^2$",
                alignment=""
            ),
            OldTexText(
                "Understanding\\\\",
                "$1 - \\frac{1}{3} + \\frac{1}{5} - \\frac{1}{7} + \\cdots" +
                "=\\frac{\\pi}{4}$",
                alignment="",
            ),
            OldTexText("Frequency analysis")
        )
        problems.arrange(
            DOWN, buff=LARGE_BUFF, aligned_edge=LEFT
        )
        # CHANGE: iterate over a copy: Cairo iterated split() (a new list) while GL iterates the live submobjects list, so adding the dots inside the loop made it visit the dots too
        for problem in list(problems):
            problems.add(Dot().next_to(problem[0], LEFT))
        problems.next_to(underline, DOWN, buff=MED_LARGE_BUFF)
        problems.to_edge(LEFT)
        v_dots = OldTex("\\vdots")
        v_dots.scale(2)
        v_dots.next_to(problems, DOWN, aligned_edge=LEFT)

        self.add(problems, v_dots)
        self.play(
            ShowCreation(underline),
            LaggedStartMap(FadeInFromDown, title, lag_ratio=0.5),
            run_time=3
        )
        self.wait()
