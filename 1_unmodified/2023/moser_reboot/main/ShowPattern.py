# ==============================================================================
# Scene:      ShowPattern
# Source:     videos/_2023/moser_reboot/main.py (lines 52-123)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowPattern.py ShowPattern -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def moser(n):
    return choose(n, 4) + choose(n, 2) + 1


class ShowPattern(InteractiveScene):
    def construct(self):
        # Show expression
        N = 11
        values = [moser(n) for n in range(1, N + 1)]
        expression = Tex(
            R",".join(map(str, values)) + R"\dots"
        )
        expression.set_width(FRAME_WIDTH - 3)
        expression.to_edge(UP)

        n = 0
        parts = VGroup()
        for value in values:
            new_n = n + len(str(value))
            parts.add(expression[n:new_n])
            self.play(FadeIn(expression[max(n - 1, 0):new_n], 0.25 * UP, run_time=0.5))
            self.wait(0.5)
            n = new_n + 1

        self.play(Write(expression[-3:]))
        self.wait()

        # Ask about expression
        brace1 = Brace(expression, DOWN)
        brace2 = Brace(expression["1,2,4,8,16"], DOWN)
        brace3 = Brace(expression["256"], DOWN)
        question = brace1.get_text("What is this pattern?")
        coincidence = brace2.get_text("Coincidence?")
        what = brace3.get_text("And what's with this?")

        VGroup(question, coincidence, what).set_color(BLUE)

        self.play(
            GrowFromCenter(brace1),
            FadeIn(question, 0.5 * DOWN),
        )
        self.wait()
        self.play(
            ReplacementTransform(brace1, brace2),
            FadeTransform(question, coincidence),
        )
        self.wait()
        self.play(
            ReplacementTransform(brace2, brace3),
            FadeTransform(coincidence, what),
        )
        self.wait()
        self.play(FadeOut(brace3), FadeOut(what))

        # Ask about the function
        fn = Tex(R"f(n) = \, ???", font_size=60)
        fn.next_to(expression, DOWN, buff=1.5)

        self.play(Write(fn))

        last_rect = VGroup()
        last_term = VGroup()
        for n, part in zip(it.count(1), parts):
            rect = SurroundingRectangle(part, buff=SMALL_BUFF)
            rect.set_stroke(YELLOW, 2)
            term = Tex(fR"f({n})", font_size=48)
            term.set_color(YELLOW)
            term.next_to(rect, DOWN)
            self.play(
                FadeIn(term), FadeIn(rect),
                FadeOut(last_term), FadeOut(last_rect),
                run_time=0.5
            )
            self.wait(0.5)
            last_term = term
            last_rect = rect
