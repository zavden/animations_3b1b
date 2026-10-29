# ==============================================================================
# Scene:      FakeAreaManipulation
# Source:     videos/outside_videos/geometry.py (lines 4-150)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl FakeAreaManipulation.py FakeAreaManipulation -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - append_points now adds (handle, anchor) pairs: 2 points instead of 3
#   - old syntax self.play(mob.method, args) -> mob.animate.method(args)
# ==============================================================================

from manim_imports_ext import *

class FakeAreaManipulation(Scene):
    CONFIG = {
        "unit": 0.5
    }

    def construct(self):
        unit = self.unit
        group1, group2 = groups = self.get_diagrams()
        for group in groups:
            group.set_width(10 * unit, stretch=True)
            group.set_height(12 * unit, stretch=True)
            group.move_to(3 * DOWN, DOWN)
            # CHANGE: append_points now adds (handle, anchor) pairs: 2 points instead of 3
            group[2].append_points(2 * [group[2].get_left() + LEFT])
            group[3].append_points(2 * [group[3].get_right() + RIGHT])

        grid = NumberPlane(
            x_range=(-30, 30),
            y_range=(-30, 30),
            faded_line_ratio=0,
        )
        grid.set_stroke(width=1)
        grid.scale(unit)
        grid.shift(3 * DOWN - grid.c2p(0, 0))

        vertex_dots = VGroup(
            Dot(group1.get_top()),
            Dot(group1.get_corner(DR)),
            Dot(group1.get_corner(DL)),
        )

        self.add(grid)
        self.add(group1)
        self.add(vertex_dots)

        # group1.save_state()

        kw = {
            "lag_ratio": 0.1,
            "run_time": 2,
            "rate_func": bezier([0, 0, 1, 1]),
        }
        path_arc_factors = [-1, 1, 0, 0, -1, 1]
        for target in (group2, group1.copy()):
            # CHANGE: old syntax self.play(mob.method, args) -> mob.animate.method(args)
            self.play(group1.animate.space_out_submobjects(1.2))
            self.play(*[
                Transform(
                    sm1, sm2,
                    path_arc=path_arc_factors[i] * 60 * DEGREES,
                    **kw
                )
                for i, sm1, sm2 in zip(it.count(), group1, target)
            ])
            self.wait(2)

        lines = VGroup(
            Line(group1.get_top(), group1.get_corner(DR)),
            Line(group1.get_top(), group1.get_corner(DL)),
        )
        lines.set_stroke(YELLOW, 2)

        frame = self.camera.frame
        frame.save_state()

        self.play(ShowCreation(lines, lag_ratio=0))
        # CHANGE: old syntax self.play(mob.method, args) -> mob.animate.method(args)
        self.play(
            frame.animate.scale(0.15).move_to(group1[1].get_corner(DR)),
            run_time=4,
        )
        self.wait(3)
        self.play(Restore(frame, run_time=2))

        # Another switch
        self.play(*[
            Transform(sm1, sm2, **kw)
            for i, sm1, sm2 in zip(it.count(), group1, group2)
        ])

        # Another zooming
        # CHANGE: old syntax self.play(mob.method, args) -> mob.animate.method(args)
        self.play(
            frame.animate.scale(0.15).move_to(group1[1].get_corner(UL)),
            run_time=4,
        )
        self.wait(2)
        self.play(Restore(frame, run_time=4))

        self.embed()

    def get_diagrams(self):
        unit = self.unit

        tri1 = Polygon(2 * LEFT, ORIGIN, 5 * UP)
        tri2 = tri1.copy()
        tri2.flip()
        tri2.next_to(tri1, RIGHT, buff=0)
        tris = VGroup(tri1, tri2)
        tris.scale(unit)
        tris.move_to(3 * UP, UP)
        tris.set_stroke(width=0)
        tris.set_fill(BLUE_D)
        tris[1].set_color(BLUE_C)

        ell = Polygon(
            ORIGIN,
            4 * RIGHT,
            4 * RIGHT + 2 * UP,
            2 * RIGHT + 2 * UP,
            2 * RIGHT + 5 * UP,
            5 * UP,
        )
        ell.scale(unit)
        ells = VGroup(ell, ell.copy().rotate(PI).shift(2 * unit * UP))
        ells.next_to(tris, DOWN, buff=0)

        ells.set_stroke(width=0)
        ells.set_fill(GREY)
        ells[1].set_fill(GREY_BROWN)

        big_tri = Polygon(ORIGIN, 3 * LEFT, 7 * UP)
        big_tri.set_stroke(width=0)
        big_tri.scale(unit)

        big_tri.move_to(ells.get_corner(DL), DR)
        big_tris = VGroup(big_tri, big_tri.copy().rotate(PI, UP, about_point=ORIGIN))

        big_tris[0].set_fill(RED_E, 1)
        big_tris[1].set_fill(RED_C, 1)
        full_group = VGroup(*tris, *ells, *big_tris)
        full_group.set_height(5, about_edge=UP)

        alt_group = full_group.copy()

        alt_group[0].move_to(alt_group, DL)
        alt_group[1].move_to(alt_group, DR)
        alt_group[4].move_to(alt_group[0].get_corner(UR), DL)
        alt_group[5].move_to(alt_group[1].get_corner(UL), DR)
        alt_group[2].rotate(90 * DEGREES)
        alt_group[2].move_to(alt_group[1].get_corner(DL), DR)
        alt_group[2].rotate(-90 * DEGREES)
        alt_group[2].move_to(alt_group[0].get_corner(DR), DL)
        alt_group[3].move_to(alt_group[1].get_corner(DL), DR)

        full_group.set_opacity(0.75)
        alt_group.set_opacity(0.75)

        return full_group, alt_group
