# ==============================================================================
# Scene:      ViewRect
# Source:     videos/_2021/some1_winners.py (lines 675-703)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ViewRect.py ViewRect -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ViewRect(Scene):
    views = 596

    def construct(self):
        rect = Rectangle(3.5, 1)
        rect.set_height(0.25)
        rect.set_stroke(RED, 3)

        number = Integer(self.views, font_size=96)
        number.set_fill(RED)
        number.next_to(rect, DOWN, LARGE_BUFF)
        number.shift(3 * RIGHT)

        arrow = Arrow(rect, number)
        arrow.set_color(RED)

        self.play(
            ShowCreation(rect)
        )

        number.set_value(0)
        self.play(
            ShowCreation(arrow),
            # FadeInFromPoint(number, arrow.get_start())
            ChangeDecimalToValue(number, self.views, run_time=2),
            VFadeIn(number),
            UpdateFromFunc(number, lambda m: m.set_fill(RED))
        )
        self.wait()
