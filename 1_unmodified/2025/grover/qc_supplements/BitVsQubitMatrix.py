# ==============================================================================
# Scene:      BitVsQubitMatrix
# Source:     videos/_2025/grover/qc_supplements.py (lines 483-514)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BitVsQubitMatrix.py BitVsQubitMatrix -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BitVsQubitMatrix(InteractiveScene):
    def construct(self):
        # Set up frame
        boxes = Rectangle(5, 3).get_grid(2, 2, buff=0)
        boxes.to_edge(DOWN, buff=MED_LARGE_BUFF)
        boxes.shift(RIGHT)
        boxes.set_stroke(WHITE, 1)

        top_titles = VGroup(
            Text("Bit", font_size=72),
            Text("Qubit", font_size=72),
        )
        for title, box in zip(top_titles, boxes):
            title.next_to(box, UP)
            title.align_to(top_titles[0], UP)

        side_titles = VGroup(
            Text("State", font_size=48),
            Text("What you\nobserve", font_size=48),
        )
        for title, box in zip(side_titles, boxes[::2]):
            title.next_to(box, LEFT)
        side_titles[0].match_x(side_titles[1])

        for i in [0, 2, 3]:
            content = Text(R"0 or 1", font_size=72)
            content.move_to(boxes[i])
            boxes[i].add(content)

        self.add(boxes)
        self.add(top_titles)
        self.add(side_titles)
