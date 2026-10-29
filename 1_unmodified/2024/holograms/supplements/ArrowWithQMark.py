# ==============================================================================
# Scene:      ArrowWithQMark
# Source:     videos/_2024/holograms/supplements.py (lines 607-618)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ArrowWithQMark.py ArrowWithQMark -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ArrowWithQMark(InteractiveScene):
    def construct(self):
        arrow = Arrow(3 * LEFT, 3 * RIGHT, path_arc=-PI / 2)
        q_marks = Tex(R"???", font_size=72)
        q_marks.next_to(arrow, UP)

        self.play(
            Write(arrow),
            Write(q_marks),
            run_time=2
        )
        self.wait()
