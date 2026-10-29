# ==============================================================================
# Scene:      ConvergenceExample
# Source:     videos/_2017/eoc/chapter10.py (lines 3085-3134)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ConvergenceExample.py ConvergenceExample -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ConvergenceExample(Scene):
    def construct(self):
        max_shown_power = 6
        max_computed_power = 13
        series = OldTex(*list(it.chain(*[
            ["\\frac{1}{%d}"%(3**n), "+"]
            for n in range(1, max_shown_power)
        ])) + ["\\cdots"])
        series_nums = [3**(-n) for n in range(1, max_computed_power)]
        partial_sums = np.cumsum(series_nums)
        braces = self.get_partial_sum_braces(series, partial_sums)

        convergence_words = OldTexText("``Converges'' to $\\frac{1}{2}$")
        convergence_words.next_to(series, UP, LARGE_BUFF)
        convergence_words.set_color(YELLOW)
        rhs = OldTex("= \\frac{1}{2}")
        rhs.next_to(series, RIGHT)
        rhs.set_color(BLUE)

        brace = braces[0]
        self.add(series, brace)
        for i, new_brace in enumerate(braces[1:]):
            self.play(Transform(brace, new_brace))
            if i == 4:
                self.play(FadeIn(convergence_words))
            else:
                self.wait()
        self.play(
            FadeOut(brace),
            Write(rhs)
        )
        self.wait(2)

    def get_partial_sum_braces(self, series, partial_sums):
        braces = [
            Brace(VGroup(*series[:n]))
            for n in range(1, len(series)-1, 2)
        ]
        last_brace = braces[-1]
        braces += [
            braces[-1].copy().stretch_in_place(
                1 + 0.1 + 0.02*(n+1), dim = 0,
            ).move_to(last_brace, LEFT)
            for n in range(len(partial_sums) - len(braces))
        ]
        for brace, partial_sum in zip(braces, partial_sums):
            number = brace.get_text("%.7f"%partial_sum)
            number.set_color(YELLOW)
            brace.add(number)
        return braces
