# ==============================================================================
# Scene:      ProblemSolvingTakeaways
# Source:     videos/_2017/putnam.py (lines 1296-1324)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ProblemSolvingTakeaways.py ProblemSolvingTakeaways -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ProblemSolvingTakeaways(Scene):
    def construct(self):
        title = OldTexText("Problem solving takeaways")
        underline = Line(LEFT, RIGHT)
        underline.set_width(title.get_width()*1.1)
        underline.next_to(title, DOWN)
        group = VGroup(title, underline)
        group.to_corner(UP+LEFT)

        points = VGroup(*[
            OldTexText(string, alignment = "")
            for string in [
                "Ask a simpler version \\\\ of the question",
                "Try reframing the question \\\\ around new constructs",
            ]
        ])
        points[0].set_color(BLUE)
        points[1].set_color(YELLOW)
        points.arrange(
            DOWN, buff = LARGE_BUFF,
            aligned_edge = LEFT
        )
        points.next_to(group, DOWN, LARGE_BUFF)

        self.play(Write(title), ShowCreation(underline))
        self.wait()
        for point in points:
            self.play(Write(point))
            self.wait(3)
