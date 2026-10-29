# ==============================================================================
# Scene:      UnwrappedCircleLogic
# Source:     videos/_2018/sphere_area.py (lines 2453-2602)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl UnwrappedCircleLogic.py UnwrappedCircleLogic -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - GL Tex has no CONFIG (class defaults are not configurable); labels keep GL defaults
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


class UnwrappedCircleLogic(UnfoldCircles):
    CONFIG = {
        "radius": 1.25,
        "dr": 0.01,
    }

    def construct(self):
        radius = self.radius
        dr = self.dr

        # CHANGE: GL Tex has no CONFIG (class defaults are not configurable); labels keep GL defaults
        pass
        unwrap_factor_tracker = ValueTracker(0)
        center_tracker = VectorizedPoint()
        highligt_prop_tracker = ValueTracker(0.5)

        def get_highlight_prop():
            return highligt_prop_tracker.get_value()

        def get_r():
            return radius * get_highlight_prop()

        center_tracker.move_to(4.5 * LEFT)

        def get_unwrapped_circle():
            result = self.get_unwrapped_circle(
                radius=radius, dr=dr,
                unwrap_factor=unwrap_factor_tracker.get_value(),
                center=center_tracker.get_center()
            )
            self.get_submob_from_prop(
                result, get_highlight_prop()
            ).set_stroke(YELLOW, 2)
            return result

        unwrapped_circle = always_redraw(get_unwrapped_circle)
        circle = unwrapped_circle.copy()
        circle.clear_updaters()
        R_line = Line(circle.get_center(), circle.get_bottom())
        R_line.set_stroke(WHITE, 2)
        R_label = OldTex("R")
        R_label.next_to(R_line, LEFT)
        circle_group = VGroup(circle, R_line, R_label)

        tri_R_line = always_redraw(
            lambda: Line(
                ORIGIN, radius * DOWN
            ).shift(center_tracker.get_center())
        )

        # Unwrap
        self.play(FadeInFromDown(circle_group))
        self.add(circle_group, unwrapped_circle, tri_R_line, R_label)
        circle_group.set_stroke(opacity=0.5)
        self.play(
            unwrap_factor_tracker.set_value, 1,
            run_time=2
        )
        self.play(
            center_tracker.move_to,
            circle.get_right() + (radius + MED_SMALL_BUFF) * RIGHT,
            circle_group.set_stroke, {"opacity": 1},
        )
        self.wait()

        # Change radius
        r_line = always_redraw(
            lambda: Line(
                ORIGIN, get_r() * DOWN,
                stroke_width=2,
                stroke_color=WHITE,
            ).shift(circle.get_center())
        )
        r_label = OldTex("r")
        r_label.add_updater(
            lambda m: m.next_to(r_line, LEFT, SMALL_BUFF)
        )
        two_pi_r_label = OldTex("2\\pi r")
        two_pi_r_label.add_updater(
            lambda m: m.next_to(
                self.get_submob_from_prop(
                    unwrapped_circle,
                    get_highlight_prop(),
                ), DOWN, SMALL_BUFF
            )
        )

        circle.add_updater(
            lambda m: m.match_style(unwrapped_circle)
        )

        self.play(
            ReplacementTransform(R_line, r_line),
            ReplacementTransform(R_label, r_label),
            FadeInFromDown(
                two_pi_r_label.copy().clear_updaters(),
                remover=True
            )
        )
        self.add(two_pi_r_label)
        for prop in [0.2, 0.8, 0.5]:
            self.play(
                highligt_prop_tracker.set_value, prop,
                run_time=2
            )

        # Show line
        line = Line(*[
            unwrapped_circle.get_corner(vect)
            for vect in (UL, DR)
        ])
        line.set_color(PINK)
        line.set_fill(BLACK, 1)
        line_word = OldTexText("Line")
        line_word.next_to(ORIGIN, UP, SMALL_BUFF)
        line_word.rotate(line.get_angle(), about_point=ORIGIN)
        line_word.shift(line.get_center())

        curve = line.copy()
        curve.get_points()[1] = unwrapped_circle.get_corner(DL)
        not_line = OldTexText("Not line")
        not_line.rotate(line.get_angle() / 2)
        not_line.move_to(line_word)
        not_line.shift(0.3 * DOWN)

        self.play(
            ShowCreation(line),
            Write(line_word),
        )
        self.wait()
        self.play(highligt_prop_tracker.set_value, 1)
        self.wait()

        # Bend
        line.save_state()
        line_word.save_state()
        self.play(
            Transform(line, curve),
            Transform(line_word, not_line),
        )
        self.wait()
        self.play(
            Restore(line),
            Restore(line_word),
            # FadeIn(two_pi_r_label),
        )
        self.wait()

    def get_submob_from_prop(self, mob, prop):
        n = len(mob.submobjects)
        return mob[min(int(prop * n), n - 1)]
