# ==============================================================================
# Scene:      Recap
# Source:     videos/_2022/puzzles/subsets.py (lines 3515-3602)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Recap.py Recap -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - tex_to_color_map with a regex key fails (dict(**...) requires str): it is removed and colored with set_color_by_tex(re.compile(...), TEAL)
# ==============================================================================

from manim_imports_ext import *

class Recap(InteractiveScene):
    def construct(self):
        # Step labels
        steps = VGroup(*(Text(f"{n}.") for n in range(1, 5)))
        VGroup(*reversed(steps)).arrange_to_fit_height(6, DOWN)
        steps.set_y(0)
        steps.to_edge(LEFT)

        # Question
        set_part = "$\\{1,\\dots,2000\\}$"
        kw = dict(font_size=40)
        question = OldTexText(
            f"Find the number of subsets of {set_part} whose sum is divisible by 5",
            tex_to_color_map={set_part: BLUE},
            **kw
        )
        question.set_width(FRAME_WIDTH - 1.5)
        question.next_to(steps[0], buff=MED_SMALL_BUFF)
        question.shift(0.025 * DOWN)
        self.play(Write(question), Write(steps[0]))
        self.wait()

        # Polynomial
        factored_tex = "(1 + x)(1 + x^2)(1 + x^3)\\cdots\\big(1 + x^{2{,}000}\\big)"
        rhs_tex = "\\sum_{n = 0}^\\infty c_n x^n"
        poly = Tex(
            f"f(x) &= {factored_tex} = {rhs_tex}",
            isolate=[factored_tex, rhs_tex, "c_n", "="],
            **kw,
        )
        poly.next_to(steps[1], RIGHT)
        poly.shift((steps[1].get_y() - poly[0].get_y()) * UP)

        cn_part = poly.select_part("c_n")
        cn_rect = SurroundingRectangle(cn_part, buff=0.05)
        cn_rect.round_corners()
        cn_rect.set_stroke(TEAL, 2)
        cn_label = OldTexText("How many subsets sum to $n$", font_size=30)
        cn_label.set_color(TEAL)
        cn_label.next_to(cn_rect, UP, MED_LARGE_BUFF, aligned_edge=LEFT)
        cn_arrow = Arrow(cn_rect.get_top(), cn_label[0][:5], color=TEAL, buff=0.1)

        self.play(FadeIn(poly, lag_ratio=0.1), Write(steps[1]))
        self.wait()
        self.play(
            ShowCreation(cn_rect),
            ShowCreation(cn_arrow),
        )
        self.play(FadeIn(cn_label, 0.25 * UP))
        self.wait()

        # Evaluation
        evaluation = Tex(
            "c_{0} + c_{5} + c_{10} + c_{15} + \\cdots = "
            "\\frac{1}{5}\\Big(f(\\zeta^0) + f(\\zeta^1) + f(\\zeta^2) + f(\\zeta^3) + f(\\zeta^4) \\Big)",
            # CHANGE: tex_to_color_map no longer admits regex keys (dict(**...) requires str); the color of c_{..} is set afterwards
            tex_to_color_map={"\\zeta": YELLOW},
            isolate=[re.compile(r"f(.+?)")],
            **kw
        )
        evaluation.set_color_by_tex(re.compile(r"c_{.+?}"), TEAL)
        evaluation.next_to(steps[2], RIGHT)

        self.play(Write(evaluation), Write(steps[2]))
        self.wait()

        # f(zeta)
        rhs = "\\Big(" + "".join(f"(1 + \\zeta^{n})" for n in range(1, 6)) + "\\Big)^{400}"
        fz = Tex(
            f"f(\\zeta) = {rhs}",
            tex_to_color_map={"\\zeta": YELLOW},
            isolate=["f(\\zeta)", "=", rhs],
            **kw,
        )
        fz.next_to(steps[3], RIGHT)

        self.play(
            TransformFromCopy(
                evaluation.select_part("f(\\zeta^1)"),
                fz.select_part("f(\\zeta)"),
            ),
            Write(fz.select_part("=")),
            Write(steps[3]),
        )
        self.wait()
        self.play(Write(fz.select_part(rhs)))
        self.wait()
