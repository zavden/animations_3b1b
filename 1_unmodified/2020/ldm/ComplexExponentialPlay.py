# ==============================================================================
# Scene:      ComplexExponentialPlay
# Source:     videos/_2020/ldm.py (lines 1010-1205)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ComplexExponentialPlay.py ComplexExponentialPlay -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ComplexExponentialPlay(Scene):
    def setup(self):
        self.transform_alpha = 0

    def construct(self):
        # Plane
        plane = ComplexPlane(
            x_min=-2 * FRAME_WIDTH,
            x_max=2 * FRAME_WIDTH,
            y_min=-2 * FRAME_HEIGHT,
            y_max=2 * FRAME_HEIGHT,
        )
        plane.add_coordinates()
        self.add(plane)

        # R Dot
        r_dot = Dot(color=YELLOW)

        def update_r_dot(dot, point_tracker=self.mouse_drag_point):
            point = point_tracker.get_location()
            if abs(point[0]) < 0.1:
                point[0] = 0
            if abs(point[1]) < 0.1:
                point[1] = 0
            dot.move_to(point)

        r_dot.add_updater(update_r_dot)
        self.mouse_drag_point.move_to(plane.n2p(1))

        # Transformed sample dots
        def func(z, dot=r_dot, plane=plane):
            r = plane.p2n(dot.get_center())
            result = np.exp(r * z)
            if abs(result) > 20:
                result *= 20 / abs(result)
            return result

        sample_dots = VGroup()
        dot_template = Dot(radius=0.05)
        dot_template.set_opacity(0.8)
        spacing = 0.05
        for x in np.arange(-7, 7, spacing):
            dot = dot_template.copy()
            dot.set_color(TEAL)
            dot.z = x
            dot.move_to(plane.n2p(dot.z))
            sample_dots.add(dot)
        for y in np.arange(-6, 6, spacing):
            dot = dot_template.copy()
            dot.set_color(MAROON)
            dot.z = complex(0, y)
            dot.move_to(plane.n2p(dot.z))
            sample_dots.add(dot)

        special_values = [1, complex(0, 1), -1, complex(0, -1)]
        special_dots = VGroup(*[
            list(filter(lambda d: abs(d.z - x) < 0.01, sample_dots))[0]
            for x in special_values
        ])
        for dot in special_dots:
            dot.set_fill(opacity=1)
            dot.scale(1.2)
            dot.set_stroke(WHITE, 2)

        sample_dots.save_state()

        def update_sample(sample, f=func, plane=plane, scene=self):
            sample.restore()
            sample.apply_function_to_submobject_positions(
                lambda p: interpolate(
                    p,
                    plane.n2p(f(plane.p2n(p))),
                    scene.transform_alpha,
                )
            )
            return sample

        sample_dots.add_updater(update_sample)

        # Sample lines
        x_line = Line(plane.n2p(plane.x_min), plane.n2p(plane.x_max))
        y_line = Line(plane.n2p(plane.y_min), plane.n2p(plane.y_max))
        y_line.rotate(90 * DEGREES)
        x_line.set_color(GREEN)
        y_line.set_color(PINK)
        axis_lines = VGroup(x_line, y_line)
        for line in axis_lines:
            line.insert_n_curves(50)
        axis_lines.save_state()

        def update_axis_liens(lines=axis_lines, f=func, plane=plane, scene=self):
            lines.restore()
            lines.apply_function(
                lambda p: interpolate(
                    p,
                    plane.n2p(f(plane.p2n(p))),
                    scene.transform_alpha,
                )
            )
            lines.make_smooth()

        axis_lines.add_updater(update_axis_liens)

        # Labels
        labels = VGroup(
            OldTex("f(1)"),
            OldTex("f(i)"),
            OldTex("f(-1)"),
            OldTex("f(-i)"),
        )
        for label, dot in zip(labels, special_dots):
            label.set_height(0.3)
            label.match_color(dot)
            label.set_stroke(BLACK, 3, background=True)
            label.add_background_rectangle(opacity=0.5)

        def update_labels(labels, dots=special_dots, scene=self):
            for label, dot in zip(labels, dots):
                label.next_to(dot, UR, 0.5 * SMALL_BUFF)
                label.set_opacity(self.transform_alpha)

        labels.add_updater(update_labels)

        # Titles
        title = OldTex(
            "f(x) =", "\\text{exp}(r\\cdot x)",
            tex_to_color_map={"r": YELLOW}
        )
        title.to_corner(UL)
        title.set_stroke(BLACK, 5, background=True)
        brace = Brace(title[1:], UP, buff=SMALL_BUFF)
        e_pow = OldTex("e^{rx}", tex_to_color_map={"r": YELLOW})
        e_pow.add_background_rectangle()
        e_pow.next_to(brace, UP, buff=SMALL_BUFF)
        title.add(brace, e_pow)

        r_eq = VGroup(
            OldTex("r=", tex_to_color_map={"r": YELLOW}),
            DecimalNumber(1)
        )
        r_eq.arrange(RIGHT, aligned_edge=DOWN)
        r_eq.next_to(title, DOWN, aligned_edge=LEFT)
        r_eq[0].set_stroke(BLACK, 5, background=True)
        r_eq[1].set_color(YELLOW)
        r_eq[1].add_updater(lambda m: m.set_value(plane.p2n(r_dot.get_center())))

        self.add(title)
        self.add(r_eq)

        # self.add(axis_lines)
        self.add(sample_dots)
        self.add(r_dot)
        self.add(labels)

        # Animations
        def update_transform_alpha(mob, alpha, scene=self):
            scene.transform_alpha = alpha

        frame = self.camera.frame
        frame.set_height(10)
        r_dot.clear_updaters()
        r_dot.move_to(plane.n2p(1))

        self.play(
            UpdateFromAlphaFunc(
                VectorizedPoint(),
                update_transform_alpha,
            )
        )
        self.play(r_dot.move_to, plane.n2p(2))
        self.wait()
        self.play(r_dot.move_to, plane.n2p(PI))
        self.wait()
        self.play(r_dot.move_to, plane.n2p(np.log(2)))
        self.wait()
        self.play(r_dot.move_to, plane.n2p(complex(0, np.log(2))), path_arc=90 * DEGREES, run_time=2)
        self.wait()
        self.play(r_dot.move_to, plane.n2p(complex(0, PI / 2)))
        self.wait()
        self.play(r_dot.move_to, plane.n2p(np.log(2)), run_time=2)
        self.wait()
        self.play(frame.set_height, 14)
        self.play(r_dot.move_to, plane.n2p(complex(np.log(2), PI)), run_time=3)
        self.wait()
        self.play(r_dot.move_to, plane.n2p(complex(np.log(2), TAU)), run_time=3)
        self.wait()

        self.embed()

    def on_mouse_scroll(self, point, offset):
        frame = self.camera.frame
        if self.zoom_on_scroll:
            factor = 1 + np.arctan(10 * offset[1])
            frame.scale(factor, about_point=ORIGIN)
        else:
            self.transform_alpha = clip(self.transform_alpha + 5 * offset[1], 0, 1)
