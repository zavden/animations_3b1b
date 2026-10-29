# ==============================================================================
# Scene:      QuickGeometryProof
# Source:     videos/_2018/dandelin.py (lines 1161-1227)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl QuickGeometryProof.py QuickGeometryProof -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class QuickGeometryProof(Scene):
    def construct(self):
        radius = 2
        circle = Circle(color=BLUE, radius=radius)
        circle.shift(0.5 * DOWN)
        angle = 60 * DEGREES
        O = circle.get_center()
        p1 = circle.point_from_proportion(angle / TAU)
        p2 = circle.point_from_proportion(1 - angle / TAU)
        Q = O + (radius / np.cos(angle)) * RIGHT

        O_p1 = Line(O, p1)
        O_p2 = Line(O, p2)
        p1_Q = Line(p1, Q, color=MAROON_B)
        p2_Q = Line(p2, Q, color=MAROON_B)
        O_Q = DashedLine(O, Q)

        elbow = VGroup(Line(RIGHT, UR), Line(UR, UP))
        elbow.set_stroke(WHITE, 1)
        elbow.scale(0.2, about_point=ORIGIN)

        ticks = VGroup(Line(DOWN, UP), Line(DOWN, UP))
        ticks.scale(0.1)
        ticks.arrange(RIGHT, buff=SMALL_BUFF)

        equation = OldTex(
            "\\Delta OP_1Q \\cong \\Delta OP_2Q",
            tex_to_color_map={
                "O": BLUE,
                "P_1": MAROON_B,
                "P_2": MAROON_B,
                "Q": YELLOW,
            }
        )
        equation.to_edge(UP)
        self.add(*equation)

        self.add(circle)
        self.add(
            OldTex("O").next_to(O, LEFT),
            OldTex("P_1").next_to(p1, UP).set_color(MAROON_B),
            OldTex("P_2").next_to(p2, DOWN).set_color(MAROON_B),
            OldTex("Q").next_to(Q, RIGHT).set_color(YELLOW),
        )
        self.add(O_p1, O_p2, p1_Q, p2_Q, O_Q)
        self.add(
            Dot(O, color=BLUE),
            Dot(p1, color=MAROON_B),
            Dot(p2, color=MAROON_B),
            Dot(Q, color=YELLOW)
        )
        self.add(
            elbow.copy().rotate(angle + PI, about_point=ORIGIN).shift(p1),
            elbow.copy().rotate(-angle + PI / 2, about_point=ORIGIN).shift(p2),
        )
        self.add(
            ticks.copy().rotate(angle).move_to(O_p1),
            ticks.copy().rotate(-angle).move_to(O_p2),
        )

        everything = VGroup(*self.mobjects)

        self.play(LaggedStartMap(
            GrowFromCenter, everything,
            lag_ratio=0.25,
            run_time=4
        ))
