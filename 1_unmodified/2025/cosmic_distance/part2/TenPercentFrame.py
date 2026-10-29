# ==============================================================================
# Scene:      TenPercentFrame
# Source:     videos/_2025/cosmic_distance/part2.py (lines 1396-1422)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TenPercentFrame.py TenPercentFrame -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TenPercentFrame(InteractiveScene):
    def construct(self):
        # Test
        title = Text("10% match", font_size=60)
        title.to_edge(UP, buff=MED_SMALL_BUFF)

        h_line = Line(LEFT, RIGHT).set_width(FRAME_WIDTH)
        h_line.next_to(title, DOWN)
        v_line = Line(h_line.get_center(), FRAME_HEIGHT * DOWN / 2)
        lines = VGroup(h_line, v_line)
        lines.set_stroke(WHITE, 2)

        self.play(
            ShowCreation(lines, lag_ratio=0),
            Write(title)
        )
        self.wait()

        # Question
        box = SurroundingRectangle(title["10%"])
        box.set_stroke(YELLOW, 2)
        q_mark = Text("?", font_size=72)
        q_mark.next_to(box, LEFT)
        q_mark.match_color(box)

        self.play(ShowCreation(box), Write(q_mark))
        self.wait()
