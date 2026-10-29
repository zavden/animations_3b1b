# ==============================================================================
# Scene:      SquareCircleExample
# Source:     videos/_2022/visual_proofs/lies.py (lines 1288-1557)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SquareCircleExample.py SquareCircleExample -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - circle.radius -> circle.get_radius()
# ==============================================================================

from manim_imports_ext import *

class SquareCircleExample(InteractiveScene):
    def construct(self):
        # Setup
        radius = 2.0
        circle = Circle(radius=radius, n_components=32)
        rich_circle = Circle(radius=radius, n_components=2**14)
        circle.set_fill(BLUE_E, 1)
        circle.set_stroke(WHITE, 1)
        approx_curves = [
            self.get_square_approx(rich_circle, 4 * 2**n)
            for n in range(10)
        ]
        square = approx_curves[0].copy()

        self.add(circle)

        # Ask about circumference
        radial_line = Line(ORIGIN, circle.get_right())
        radial_line.set_stroke(WHITE, 1)
        radius_label = OldTex("1")
        radius_label.next_to(radial_line, UP, SMALL_BUFF)

        circum = circle.copy()
        circum.set_stroke(YELLOW, 3).set_fill(opacity=0)
        question = Text("What is the circumference?")
        question.next_to(circle, UP, MED_LARGE_BUFF)

        unwrapped_circum = Line(LEFT, RIGHT)
        unwrapped_circum.set_width(PI * circle.get_width())
        unwrapped_circum.match_style(circum)
        unwrapped_circum.next_to(circle, UP)

        diameter = Line(circle.get_left(), circle.get_right())
        diameter.set_stroke(RED, 2)

        self.play(
            ShowCreation(radial_line),
            Write(radius_label, stroke_color=WHITE)
        )
        self.wait()

        self.play(
            Write(question),
            ShowCreation(circum)
        )
        self.wait()
        self.play(
            question.animate.to_edge(UP),
            Transform(circum, unwrapped_circum),
        )
        self.play(ShowCreation(diameter))
        self.wait()
        self.play(*map(FadeOut, [question, circum, diameter]))

        # Show perimeter length
        points = [square.get_edge_center(np.round(vect)) for vect in compass_directions(8)]
        new_radii = VGroup(*(
            Line(p1, p2).match_style(radial_line)
            for p1, p2 in adjacent_pairs(points)
        ))
        new_radii.save_state()
        new_radii.space_out_submobjects(1.1)

        perimeter_label = OldTexText("Perimeter = $8$")
        perimeter_label.to_edge(UP)

        self.play(ShowCreation(square), run_time=3)
        self.play(square.animate.scale(1.2), rate_func=there_and_back)
        self.wait()
        self.play(
            TransformFromCopy(VGroup(radial_line), new_radii, lag_ratio=0.2, run_time=2),
            FadeIn(perimeter_label),
        )
        self.wait()
        self.play(new_radii.animate.restore())
        self.play(FadeOut(new_radii))
        self.wait()

        # Finer approximations
        for i, curve in enumerate(approx_curves[1:]):
            curve.set_color(YELLOW)
            self.play(
                square.animate.set_stroke(width=1),
                TransformFromCopy(square, curve)
            )
            self.wait()
            if i == 0:
                dots = GlowDot().replicate(2)
                dots.set_color(BLUE)
                sc = square.copy().insert_n_curves(200)
                cc = curve.copy().insert_n_curves(200)
                self.play(VGroup(square, curve).animate.set_stroke(opacity=0.2))
                self.play(
                    MoveAlongPath(dots[0], square),
                    MoveAlongPath(dots[1], curve),
                    ShowCreation(sc),
                    ShowCreation(cc),
                    rate_func=linear,
                    run_time=6,
                )
                self.play(FadeOut(dots), FadeOut(sc), FadeOut(cc), VGroup(square, curve).animate.set_stroke(opacity=1))

            if i == 1:
                curve.set_stroke(width=5)
                print(self.num_plays)
            self.play(FadeOut(square), curve.animate.set_color(RED))
            square = curve

        # Zoom in
        frame = self.camera.frame
        self.wait(note="Prepare for zoom")
        self.play(frame.animate.set_height(0.05).move_to(circle.pfp(1 / 8)), run_time=4)
        self.wait()
        self.play(frame.animate.to_default_state(), run_time=3)

        # Define parametric curve
        frame = self.camera.frame
        t_tracker = ValueTracker(0)
        get_t = t_tracker.get_value
        dot = GlowDot()
        t_axis = UnitInterval()
        t_axis.set_width(6)
        t_axis.next_to(circle, RIGHT, buff=1.5)
        t_axis.add_numbers()
        t_indicator = Triangle(start_angle=-90 * DEGREES)
        t_indicator.set_height(0.1)
        t_indicator.set_fill(RED, 1)
        t_indicator.set_stroke(WHITE, 0)
        t_label = VGroup(OldTex("t = "), DecimalNumber())
        t_label.arrange(RIGHT)
        t_label.next_to(t_axis, UP, buff=LARGE_BUFF)
        VGroup(t_axis, t_label).to_edge(UP)

        t_label[1].add_updater(lambda d: d.set_value(get_t()))
        dot.add_updater(lambda d: d.move_to(square.pfp(get_t())))
        t_indicator.add_updater(lambda m: m.move_to(t_axis.n2p(get_t()), DOWN))

        c_labels = VGroup(*(OldTex(f"c_{n}(t)") for n in range(len(approx_curves))))
        c_labels.add(OldTex("c_\\infty (t)"))
        for label in c_labels:
            label.scale(0.75)
            label.add_updater(lambda m: m.next_to(dot, UR, buff=-SMALL_BUFF))

        self.play(
            Transform(square, approx_curves[0]),
            frame.animate.move_to(4 * RIGHT),
            FadeIn(dot),
            FadeIn(t_label),
            Write(c_labels[0]),
            Write(t_axis),
            Write(t_indicator),
            run_time=1
        )
        square.match_points(approx_curves[0])
        self.wait()
        self.play(t_tracker.animate.set_value(1), run_time=7)
        self.wait()
        t_tracker.set_value(0)

        self.play(
            Transform(square, approx_curves[1]),
            FadeTransform(c_labels[0], c_labels[1]),
        )
        self.play(t_tracker.animate.set_value(1), run_time=7)
        self.wait()
        t_tracker.set_value(0)

        # Show limits
        self.play(t_tracker.animate.set_value(0.2), run_time=3)
        dot_shadows = VGroup()
        self.add(dot_shadows)
        for i in range(2, len(approx_curves)):
            dot_shadow = Dot(radius=0.01, color=YELLOW, opacity=0.5)
            dot_shadow.move_to(dot)
            dot_shadows.add(dot_shadow)
            self.play(
                Transform(square, approx_curves[i]),
                FadeTransform(c_labels[i - 1], c_labels[i]),
                run_time=0.5,
            )
            self.wait(0.5)

        # Write limits
        lim_tex_ex = Tex("\\lim_{n \\to \\infty} c_{n}(" + "{:.1f}".format(get_t()) + ")")
        lim_tex = OldTex("c_\\infty(t)", ":=", "\\lim_{n \\to \\infty} c_{n}(t)")
        for lt in lim_tex_ex, lim_tex:
            lt.next_to(t_axis, DOWN, aligned_edge=LEFT, buff=2.0)
        lim_arrow = Arrow(lim_tex_ex.get_corner(UL), dot.get_center(), buff=0.1, stroke_width=2, color=YELLOW)
        self.play(Write(lim_tex_ex))
        self.play(ShowCreation(lim_arrow))
        self.wait()
        self.play(
            FadeTransform(lim_tex_ex, lim_tex[2]),
            Write(lim_tex[:2]),
        )
        self.wait()
        self.play(FadeOut(dot_shadows), FadeOut(lim_arrow), FadeTransform(c_labels[9], c_labels[-1]))
        self.play(t_tracker.animate.set_value(0), run_time=2)
        self.play(t_tracker.animate.set_value(1), run_time=8)
        self.wait()

        # This is a circle
        text = Text("This is, precisely, a circle", t2s={"precisely": ITALIC})
        text.next_to(lim_tex, DOWN, LARGE_BUFF, aligned_edge=LEFT)
        arrow = Arrow(text, lim_tex[0])
        VGroup(text, arrow).set_color(GREEN)

        self.play(Write(text), ShowCreation(arrow))
        self.wait()
        self.play(FadeOut(text), FadeOut(arrow), lim_tex.animate.shift(UP))

        # Mismatched limits
        t2c = {
            "\\lim_{n \\to \\infty}": YELLOW,
            "\\text{len}": RED,
            "c_n(t)": WHITE,
            "\\Big(": WHITE,
            "\\Big)": WHITE,
        }
        lim_len = Tex("\\lim_{n \\to \\infty}\\Big(\\text{len}\\big(c_n(t)\\big) \\Big) = 8", tex_to_color_map=t2c)
        len_lim = Tex("\\text{len} \\Big( \\lim_{n \\to \\infty} c_n(t) \\Big) = 2\\pi", tex_to_color_map=t2c)
        lims = VGroup(lim_len, len_lim)
        lim_len.next_to(lim_tex, DOWN, LARGE_BUFF, aligned_edge=LEFT)

        top_group = VGroup(t_axis, t_indicator, t_label)

        self.play(Write(lim_len))
        self.wait()
        self.play(
            VGroup(lim_tex, lim_len).animate.next_to(frame.get_corner(UR), DL, MED_LARGE_BUFF),
            FadeOut(top_group, 2 * UR),
        )

        len_lim.next_to(lim_len, DOWN, buff=2.0, aligned_edge=LEFT)
        not_eq = OldTex("\\ne", font_size=96)
        not_eq.rotate(90 * DEGREES)
        not_eq.move_to(VGroup(len_lim, lim_len))
        not_eq.match_x(len_lim)

        self.play(*(
            TransformFromCopy(lim_len.select_parts(tex), len_lim.select_parts(tex))
            for tex in t2c.keys()
        ))
        self.play(Write(not_eq))
        self.wait()
        self.play(Write(len_lim[3:]))
        self.wait()

        # Commentary
        morty = Mortimer()

    def get_square_approx(self, circle, n_samples):
        # CHANGE: Circle no longer has the radius attribute; get_radius() is used
        radius = circle.get_radius()
        points = [
            radius * np.array([math.cos(a), math.sin(a), 0])
            for a in np.linspace(0, TAU, n_samples + 1)
        ]
        result = VMobject()
        result.start_new_path(points[0])
        for p1, p2 in zip(points, points[1:]):
            corners = np.array([
                [p2[0], p1[1], 0],
                [p1[0], p2[1], 0]
            ])
            corner = corners[np.argmax(np.apply_along_axis(np.linalg.norm, 1, corners))]
            result.add_line_to(corner)
            result.add_line_to(p2)

        result.set_stroke(RED, 2)
        return result
