# ==============================================================================
# Scene:      BackAndForth
# Source:     videos/_2017/highD.py (lines 513-565)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BackAndForth.py BackAndForth -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BackAndForth(Scene):
    def construct(self):
        analytic = OldTexText("Analytic")
        analytic.shift(FRAME_X_RADIUS*LEFT/2)
        analytic.to_edge(UP, buff = MED_SMALL_BUFF)
        geometric = OldTexText("Geometric")
        geometric.shift(FRAME_X_RADIUS*RIGHT/2)
        geometric.to_edge(UP, buff = MED_SMALL_BUFF)
        h_line = Line(LEFT, RIGHT).scale(FRAME_X_RADIUS)
        h_line.to_edge(UP, LARGE_BUFF)
        v_line = Line(UP, DOWN).scale(FRAME_Y_RADIUS)
        self.add(analytic, geometric, h_line, v_line)

        pair = OldTex("(", "x", ",", "y", ")")
        pair.shift(FRAME_X_RADIUS*LEFT/2 + FRAME_Y_RADIUS*UP/3)
        triplet = OldTex("(", "x", ",", "y", ",", "z", ")")
        triplet.shift(FRAME_X_RADIUS*LEFT/2 + FRAME_Y_RADIUS*DOWN/2)
        for mob in pair, triplet:
            arrow = DoubleArrow(LEFT, RIGHT)
            arrow.move_to(mob)
            arrow.shift(2*RIGHT)
            mob.arrow = arrow
        circle_eq = OldTex("x", "^2", "+", "y", "^2", "=", "1")
        circle_eq.move_to(pair)
        sphere_eq = OldTex("x", "^2", "+", "y", "^2", "+", "z", "^2", "=", "1")
        sphere_eq.move_to(triplet)

        plane = NumberPlane(x_unit_size = 2, y_unit_size = 2)
        circle = Circle(radius = 2, color = YELLOW)
        plane_group = VGroup(plane, circle)
        plane_group.scale(0.4)
        plane_group.next_to(h_line, DOWN, SMALL_BUFF)
        plane_group.shift(FRAME_X_RADIUS*RIGHT/2)


        self.play(Write(pair))
        # self.play(ShowCreation(pair.arrow))
        self.play(ShowCreation(plane, run_time = 3))
        self.play(Write(triplet))
        # self.play(ShowCreation(triplet.arrow))
        self.wait(3)
        for tup, eq, to_draw in (pair, circle_eq, circle), (triplet, sphere_eq, VMobject()):
            for mob in tup, eq:
                mob.xyz = VGroup(*[sm for sm in map(mob.get_part_by_tex, "xyz") if sm is not None])
            self.play(
                ReplacementTransform(tup.xyz, eq.xyz),
                FadeOut(VGroup(*[sm for sm in tup if sm not in tup.xyz])),
            )
            self.play(
                Write(VGroup(*[sm for sm in eq if sm not in eq.xyz])),
                ShowCreation(to_draw)
            )
        self.wait(3)
