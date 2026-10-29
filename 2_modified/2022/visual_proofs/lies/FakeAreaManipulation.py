# ==============================================================================
# Scene:      FakeAreaManipulation
# Source:     videos/_2022/visual_proofs/lies.py (lines 874-1063)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl FakeAreaManipulation.py FakeAreaManipulation -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - append_points(3 * [p]) -> append_points(2 * [p]): the curves are quadratic (handle + anchor)
# ==============================================================================

from manim_imports_ext import *

class FakeAreaManipulation(InteractiveScene):
    CONFIG = {
        "unit": 0.5
    }

    def construct(self):
        # Setup
        unit = self.unit
        group1, group2 = groups = self.get_diagrams()
        for group in groups:
            group.set_width(10 * unit, stretch=True)
            group.set_height(12 * unit, stretch=True)
            group.move_to(3 * DOWN, DOWN)
            # CHANGE: append_points are now quadratic: 2 points (handle and anchor) instead of 3
            group[2].append_points(2 * [group[2].get_left() + LEFT])
            # CHANGE: append_points are now quadratic: 2 points (handle and anchor) instead of 3
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
        self.add(*group1)
        self.add(vertex_dots)

        self.disable_interaction(grid, vertex_dots)
        targets = [group1.copy(), group2.copy()]

        self.wait(note="Manually manipulate")

        # Animate swap
        kw = {
            "lag_ratio": 0.1,
            "run_time": 2,
            "rate_func": bezier([0, 0, 1, 1]),
        }
        path_arc_factors = [-1, 1, 0, 0, -1, 1]
        for target in targets:
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

        # Zoom
        lines = VGroup(
            Line(grid.c2p(0, 12), grid.c2p(-5, 0)),
            Line(grid.c2p(0, 12), grid.c2p(5, 0)),
        )
        lines.set_stroke(YELLOW, 2)
        self.disable_interaction(lines)

        frame = self.camera.frame
        frame.save_state()

        self.play(ShowCreation(lines, lag_ratio=0))
        self.play(
            frame.animate.scale(0.15).move_to(group1[0].get_corner(UR)),
            run_time=4,
        )
        self.wait(3)
        self.play(frame.animate.restore(), run_time=2)

        # Another switch
        self.wait(note="Hold for next swap")
        self.play(*(
            Transform(sm1, sm2, **kw)
            for sm1, sm2 in zip(group1, targets[0])
        ))
        self.wait()

        # Another zooming
        self.play(
            frame.animate.scale(0.15).move_to(group1[4].get_corner(UR)),
            run_time=4,
        )
        self.wait(2)
        self.play(frame.animate.restore(), run_time=2)

        # Show slopes
        tris = VGroup(group1[0], group1[4])
        lil_lines = VGroup(*(Line(tri.get_corner(DL), tri.get_corner(UR)) for tri in tris))
        lil_lines[0].set_stroke(PINK, 3)
        lil_lines[1].set_stroke(WHITE, 3)

        slope_labels = VGroup(
            OldTexText("Slope =", " $5 / 2$"),
            OldTexText("Slope =", " $7 / 3$"),
        )
        for line, label in zip(lil_lines, slope_labels):
            label.next_to(line.pfp(0.5), UL, buff=0.7)
            arrow = Arrow(label.get_bottom(), line.pfp(0.5))
            label.add(arrow)

        self.play(
            FadeOut(lines[0]),
            ShowCreation(lil_lines),
        )
        for line, label in zip(lil_lines, slope_labels):
            p1, p2 = line.get_start_and_end()
            corner = [p2[0], p1[1], 0]
            x_line = Line(p1, corner).set_stroke(line.get_color(), 2)
            y_line = Line(corner, p2).set_stroke(line.get_color(), 2)
            self.play(
                FadeIn(label[:2]),
                ShowCreation(label[2]),
            )
            self.play(
                TransformFromCopy(line, y_line),
                FlashAround(label[1][0]),
            )
            self.play(
                TransformFromCopy(line, x_line),
                FlashAround(label[1][2]),
            )
            self.wait()

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
