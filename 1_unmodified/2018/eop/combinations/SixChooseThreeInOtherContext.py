# ==============================================================================
# Scene:      SixChooseThreeInOtherContext
# Source:     videos/_2018/eop/combinations.py (lines 537-599)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SixChooseThreeInOtherContext.py SixChooseThreeInOtherContext -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SixChooseThreeInOtherContext(Scene):
    def construct(self):
        self.add_dots()
        self.count_paths_to_three_three()

    def add_dots(self):
        n = 4
        dots = VGroup(*[Dot() for x in range(n**2)])
        dots.arrange_in_grid(n, n, buff = LARGE_BUFF)
        dots.next_to(ORIGIN, LEFT)
        self.add(dots)

        self.dots = dots
        self.dot_to_dot_distance = get_norm(
            dots[1].get_center() - dots[0].get_center()
        )

    def count_paths_to_three_three(self):
        dots = self.dots
        d = self.dot_to_dot_distance
        lower_left = dots.get_corner(DOWN+LEFT)
        lower_left += dots[0].radius*(UP+RIGHT)

        right = Vector(d*RIGHT, color = PINK)
        up = Vector(d*UP, color = BLUE)

        last_rights = None
        last_ups = None
        last_line = None
        for indices in it.combinations(list(range(6)), 3):
            bools = [i in indices for i in range(6)]
            arrows = VGroup(*[
                right.deepcopy() if b else up.deepcopy()
                for b in bools
            ])
            last_point = np.array(lower_left)
            ups, rights = VGroup(), VGroup()
            for arrow, b in zip(arrows, bools):
                arrow.shift(last_point - arrow.get_start())
                last_point = arrow.get_end()
                group = rights if b else ups
                group.add(arrow)

            line = VGroup(*[arrow.tip.copy() for arrow in arrows])
            line.arrange(RIGHT, buff = 0.5*SMALL_BUFF)
            if last_line is None:
                line.shift(FRAME_X_RADIUS*RIGHT/2)
                line.to_edge(UP)
                self.play(
                    ShowCreation(arrows),
                    ShowCreation(line)
                )
            else:
                line.next_to(last_line, DOWN, SMALL_BUFF)
                self.play(
                    FadeIn(line),
                    ReplacementTransform(last_rights, rights),
                    ReplacementTransform(last_ups, ups),
                )
            last_rights = rights
            last_ups = ups
            last_line = line
        self.wait()
