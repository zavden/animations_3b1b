# ==============================================================================
# Scene:      QuaternionInterpolationScematic
# Source:     videos/_2018/quat3d.py (lines 814-857)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl QuaternionInterpolationScematic.py QuaternionInterpolationScematic -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class QuaternionInterpolationScematic(Scene):
    def construct(self):
        title = OldTexText("Slice of a hypersphere")
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        self.add(title)

        radius = 3
        circle = Circle(radius=radius)
        circle.set_stroke(GREY_B, 1)
        qs = [circle.point_from_proportion(p) for p in (0.55, 0.35, 0.15)]
        colors = [YELLOW, PINK, RED]
        q_dots = [Dot(q, color=c) for q, c in zip(qs, colors)]
        q_labels = [
            OldTex("q_{}".format(i + 1)).next_to(
                dot, normalize(dot.get_center()), SMALL_BUFF
            ).match_color(dot)
            for i, dot in enumerate(q_dots)
        ]

        q1, q2, q3 = qs
        lines = [
            DashedLine(q1, q2)
            for q1, q2 in zip(qs, qs[1:])
        ]
        for color, line in zip([GREEN, BLUE], lines):
            line.set_stroke(color, 3)
            line.proj = line.copy().apply_function(
                lambda p: radius * normalize(p)
            )
        dot = Dot(qs[0], color=WHITE)

        self.add(circle)
        self.add(dot)
        self.add(*q_dots + q_labels)

        self.wait(2)
        for line, q in zip(lines, qs[1:]):
            self.play(
                ShowCreation(line),
                ShowCreation(line.proj),
                dot.move_to, q,
                run_time=4
            )
            self.wait(2)
