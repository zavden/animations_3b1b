# ==============================================================================
# Scene:      UnfoldCircles
# Source:     videos/_2018/sphere_area.py (lines 502-670)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl UnfoldCircles.py UnfoldCircles -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - GL Tex has no CONFIG (class defaults are not configurable); labels keep GL defaults
# ==============================================================================

from manim_imports_ext import *

class UnfoldCircles(Scene):
    CONFIG = {
        "circle_style": {
            "fill_color": GREY_BROWN,
            "fill_opacity": 0,
            "stroke_color": GREY_BROWN,
            "stroke_width": 2,
        },
        "radius": 1.0,
        "dr": 0.01,
    }

    def construct(self):
        self.show_rectangle_with_formula()
        self.add_four_circles()

    def show_rectangle_with_formula(self):
        # CHANGE: GL Tex has no CONFIG (class defaults are not configurable); labels keep GL defaults
        pass
        R = self.radius
        rect = Rectangle(width=TAU * R, height=2 * R)
        rect.set_fill(BLUE_E, 1)
        rect.set_stroke(width=0)
        p0, p1, p2 = [rect.get_corner(v) for v in (DL, UL, UR)]
        h_line = Line(p0, p1)
        h_line.set_stroke(RED, 3)
        w_line = Line(p1, p2)
        w_line.set_stroke(YELLOW, 3)
        two_R = OldTex("2", "R")
        two_R.next_to(h_line, LEFT)
        two_pi_R = OldTex("2", "\\pi", "R")
        two_pi_R.next_to(w_line, UP)

        pre_area_label = OldTex(
            "2\\cdot", "2", "\\pi", "R", "\\cdot R"
        )
        area_label = OldTex("4", "\\pi", "R^2")
        for label in [area_label, pre_area_label]:
            label.next_to(rect.get_center(), UP, SMALL_BUFF)

        self.rect_group = VGroup(
            rect, h_line, w_line,
            two_R, two_pi_R, area_label
        )
        self.area_label = area_label
        self.rect = rect

        self.add(rect, h_line, w_line, two_R, two_pi_R)
        self.play(
            TransformFromCopy(two_R[0], pre_area_label[0]),
            TransformFromCopy(two_R[1], pre_area_label[-1]),
            TransformFromCopy(two_pi_R, pre_area_label[1:-1]),
        )
        self.wait()
        self.play(
            ReplacementTransform(pre_area_label[:2], area_label[:1]),
            ReplacementTransform(pre_area_label[2], area_label[1]),
            ReplacementTransform(pre_area_label[3:], area_label[2:]),
        )
        self.wait()
        self.play(
            self.rect_group.to_corner, UL,
            {"buff": MED_SMALL_BUFF}
        )

    def add_four_circles(self):
        rect_group = self.rect_group
        radius = self.radius

        radii_lines = VGroup(*[
            Line(radius * UP, ORIGIN).set_stroke(WHITE, 2)
            for x in range(4)
        ])
        radii_lines.arrange_in_grid(buff=1.3)
        radii_lines[2:].shift(RIGHT)
        radii_lines.next_to(rect_group, DOWN, buff=1.3)
        R_labels = VGroup(*[
            OldTex("R").next_to(line, LEFT, SMALL_BUFF)
            for line in radii_lines
        ])

        unwrap_factor_tracker = ValueTracker(0)

        def get_circle(line):
            return always_redraw(
                lambda: self.get_unwrapped_circle(
                    radius=radius, dr=self.dr,
                    unwrap_factor=unwrap_factor_tracker.get_value(),
                    center=line.get_top()
                )
            )

        circles = VGroup(*[get_circle(line) for line in radii_lines])
        circle_copies = circles.copy()
        for mob in circle_copies:
            mob.clear_updaters()

        self.play(
            LaggedStartMap(Write, circle_copies, lag_ratio=0.7),
            LaggedStartMap(Write, R_labels),
            LaggedStartMap(ShowCreation, radii_lines),
        )
        self.remove(circle_copies)
        self.add(circles, radii_lines, R_labels)
        self.wait()
        self.play(
            radii_lines[2:].shift, 2.9 * RIGHT,
            R_labels[2:].shift, 2.9 * RIGHT,
            VGroup(
                radii_lines[:2], R_labels[:2]
            ).to_edge, LEFT, {"buff": 1.0}
        )
        self.play(
            unwrap_factor_tracker.set_value, 1,
            run_time=2
        )
        self.wait()

        # Move triangles
        triangles = circles.copy()
        for triangle in triangles:
            triangle.clear_updaters()
            border = Polygon(*[
                triangle.get_corner(vect)
                for vect in (DL, UL, DR)
            ])
            border.set_stroke(WHITE, 1)
            triangle.add(border)
            triangle.generate_target()
        rect = self.rect
        for i, triangle in enumerate(triangles):
            if i % 2 == 1:
                triangle.target.rotate(PI)
            vect = UP if i < 2 else DOWN
            triangle.target.move_to(rect, vect)

        self.play(FadeIn(triangles))
        self.add(triangles, triangles.copy(), self.area_label)
        self.play(MoveToTarget(triangles[0]))
        self.wait()
        self.play(LaggedStartMap(MoveToTarget, triangles))
        self.wait()

    #
    def get_unwrapped_circle(self, radius, dr, unwrap_factor=0, center=ORIGIN):
        radii = np.arange(0, radius + dr, dr)
        rings = VGroup()
        for r in radii:
            r_factor = 1 + 3 * (r / radius)
            alpha = unwrap_factor**r_factor
            alpha = np.clip(alpha, 0, 0.9999)
            angle = interpolate(TAU, 0, alpha)
            length = TAU * r
            arc_radius = length / angle
            ring = Arc(
                start_angle=-90 * DEGREES,
                angle=angle,
                radius=arc_radius,
                **self.circle_style
            )
            ring.shift(center + (r - arc_radius) * DOWN)
            # ring = AnnularSector(
            #     inner_radius=r1,
            #     outer_radius=r2,
            #     angle=TAU,
            #     start_angle=-TAU / 4,
            #     **self.circle_style
            # )
            rings.add(ring)
        return rings
