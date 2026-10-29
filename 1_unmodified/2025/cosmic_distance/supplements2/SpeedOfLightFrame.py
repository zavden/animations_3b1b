# ==============================================================================
# Scene:      SpeedOfLightFrame
# Source:     videos/_2025/cosmic_distance/supplements2.py (lines 347-375)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SpeedOfLightFrame.py SpeedOfLightFrame -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SpeedOfLightFrame(InteractiveScene):
    def construct(self):
        # Test
        # title = Text("Real-time\ndepiction\nof the\nspeed of\nlight", alignment="LEFT", font_size=60)
        title = Text("The speed\nof light in\nreal time", alignment="LEFT", font_size=60)
        title.to_edge(LEFT, buff=0.25)

        h_lines = Line(LEFT, RIGHT).set_width(11).replicate(2)
        h_lines.arrange(DOWN, buff=FRAME_HEIGHT / 3)
        h_lines.to_edge(RIGHT, buff=0)
        v_line = Line(UP, DOWN).set_height(FRAME_HEIGHT)
        v_line.move_to(h_lines, LEFT)

        lines = VGroup(v_line, h_lines)
        lines.set_stroke(WHITE, 2)

        self.add(title)
        self.add(lines)


    def old(self):
        h_line = Line(LEFT, RIGHT).set_width(FRAME_WIDTH)
        h_line.next_to(title, DOWN)
        h_line2 = h_line.copy()
        h_line2.set_y(-1)
        VGroup(h_line, h_line2).set_stroke(WHITE, 2)

        self.add(title, h_line, h_line2)
        self.wait()
