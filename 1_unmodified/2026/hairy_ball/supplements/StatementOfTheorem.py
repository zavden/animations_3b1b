# ==============================================================================
# Scene:      StatementOfTheorem
# Source:     videos/_2026/hairy_ball/supplements.py (lines 130-158)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl StatementOfTheorem.py StatementOfTheorem -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class StatementOfTheorem(InteractiveScene):
    def construct(self):
        # Add text
        title = Text("Hairy Ball Theorem", font_size=72)
        title.to_corner(UL)
        underline = Underline(title)

        self.add(title, underline)

        statement = Text("""
            Any continuous vector field
            on a sphere must have at least
            one null vector.
        """, alignment="LEFT")
        statement.next_to(underline, DOWN, buff=MED_LARGE_BUFF)
        statement.to_edge(LEFT)

        self.play(Write(statement, run_time=3, lag_ratio=1e-1))
        self.wait()

        statement.set_backstroke(BLACK, 5)

        # Highlight text
        for text, color in [("continuous", BLUE), ("one null vector", YELLOW)]:
            self.play(
                FlashUnder(statement[text], time_width=1.5, run_time=2, color=color),
                statement[text].animate.set_fill(color)
            )
            self.wait()
