# ==============================================================================
# Scene:      CartesianSlices
# Source:     videos/_2023/gauss_int/integral.py (lines 1008-1209)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CartesianSlices.py CartesianSlices -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class GaussianIntegral(ThreeDScene, InteractiveScene):
    def func(self, x, y):
        return np.exp(-x**2 - y**2)

    def get_axes(
        self,
        x_range=(-3, 3),
        y_range=(-3, 3),
        z_range=(0, 1.5, 0.5),
        width=8,
        height=8,
        depth=3,
        center=0.5 * IN,
        include_plane=False
    ):
        axes = ThreeDAxes(
            x_range, y_range, z_range,
            width=width, height=height, depth=depth
        )
        axes.set_stroke(GREY_C)
        if include_plane:
            plane = NumberPlane(
                x_range, y_range,
                width=width, height=height,
                background_line_style=dict(
                    stroke_color=GREY_C,
                    stroke_width=1,
                ),
            )
            plane.faded_lines.set_stroke(opacity=0.5)
            plane.shift(0.01 * IN)
            axes.plane = plane
            axes.add(plane)

        x, y, z = axis_labels = VGroup(*map(Tex, "xyz"))
        axis_labels.use_winding_fill(False)
        x.next_to(axes.x_axis, RIGHT)
        y.next_to(axes.y_axis, UP)
        z.rotate(90 * DEGREES, RIGHT)
        z.next_to(axes.z_axis, OUT)
        axes.labels = axis_labels
        axes.add(axis_labels)

        axes.shift(center - axes.c2p(0, 0, 0))
        axes.set_flat_stroke(False)
        return axes

    def get_gaussian_graph(
        self,
        axes,
        color=interpolate_color(BLUE_E, BLACK, 0.6),
        opacity=1.0,
        shading=(0.2, 0.2, 0.4),
    ):
        graph = axes.get_graph(self.func)
        graph.set_color(color)
        graph.set_opacity(opacity)
        graph.set_shading(*shading)
        return graph

    def get_dynamic_cylinder(self, axes, r_init=1):
        cylinder = self.get_cylinder(axes, r_init)
        r_tracker = ValueTracker(r_init)
        cylinder.add_updater(lambda m: self.set_cylinder_r(
            m, axes, r_tracker.get_value()
        ))
        return cylinder, r_tracker

    def get_cylinder(
        self, axes, r,
        color=BLUE_E,
        opacity=1
    ):
        cylinder = Cylinder(color=color, opacity=opacity)
        self.set_cylinder_r(cylinder, axes, r)
        return cylinder

    def set_cylinder_r(self, cylinder, axes, r):
        r = max(r, 1e-5)
        cylinder.set_width(2 * r * axes.x_axis.get_unit_size())
        cylinder.set_depth(
            self.func(r, 0) * axes.z_axis.get_unit_size(),
            stretch=True
        )
        cylinder.move_to(axes.c2p(0, 0, 0), IN)
        return cylinder

    def get_thick_cylinder(self, cylinder, delta_r):
        radius = 0.5 * cylinder.get_width()
        outer_cylinder = cylinder.copy()
        factor = (radius + delta_r) / radius
        outer_cylinder.stretch(factor, 0)
        outer_cylinder.stretch(factor, 1)

        annulus = ParametricSurface(
            lambda u, v: (radius + u * delta_r) * np.array([math.cos(v), math.sin(v), 0]),
            u_range=(0, 1),
            v_range=(0, TAU),
        )
        annulus.match_color(cylinder)
        annulus.move_to(cylinder, OUT)

        result = Group(cylinder.copy(), annulus, outer_cylinder)
        result.clear_updaters()
        return result

    def get_x_slice(self, axes, y, x_range=(-3, 3.1, 0.1)):
        xs = np.arange(*x_range)
        ys = np.ones(len(xs)) * y
        points = axes.c2p(xs, ys, self.func(xs, y))
        graph = VMobject().set_points_smoothly(points)
        graph.use_winding_fill(False)
        return graph

    def get_dynamic_slice(
        self,
        axes,
        stroke_color=BLUE,
        stroke_width=2,
        fill_color=BLUE_E,
        fill_opacity=0.5,
    ):
        y_tracker = ValueTracker(0)
        get_y = y_tracker.get_value

        z_unit = axes.z_axis.get_unit_size()
        x_slice = self.get_x_slice(axes, 0)
        x_slice.set_stroke(stroke_color, stroke_width)
        x_slice.set_fill(fill_color, fill_opacity)
        x_slice.add_updater(
            lambda m: m.set_depth(self.func(0, get_y()) * z_unit, stretch=True)
        )
        x_slice.add_updater(lambda m: m.move_to(axes.c2p(0, get_y(), 0), IN))

        return x_slice, y_tracker


class CartesianSlices(GaussianIntegral):
    def construct(self):
        # Setup
        frame = self.frame
        axes = self.get_axes()

        graph = self.get_gaussian_graph(axes)
        graph_mesh = SurfaceMesh(graph, resolution=(21, 21))
        graph_mesh.set_stroke(WHITE, 0.5, opacity=0.25)
        graph_mesh.set_flat_stroke(False)

        self.add(axes, graph, graph_mesh)

        # Dynamic slice
        x_slice, y_tracker = self.get_dynamic_slice(axes)
        y_unit = axes.y_axis.get_unit_size()
        graph.add_updater(lambda m: m.set_clip_plane(UP, -y_tracker.get_value() * y_unit))

        x_max = axes.x_range[1]
        y_tracker.set_value(x_max)
        self.add(x_slice)
        self.play(
            y_tracker.animate.set_value(-x_max),
            run_time=5,
            rate_func=linear,
        )
        self.wait()

        # Show many slices
        def get_x_slices(dx=0.25):
            original_y_value = y_tracker.get_value()
            x_slices = VGroup()
            x_min, x_max = axes.x_range[:2]
            for y in np.arange(x_max, x_min, -dx):
                y_tracker.set_value(y)
                x_slice.update()
                x_slices.add(x_slice.copy().clear_updaters())
            x_slices.use_winding_fill(False)
            x_slices.deactivate_depth_test()
            x_slices.set_stroke(BLUE, 2, 0.5)
            x_slices.set_flat_stroke(False)
            y_tracker.set_value(original_y_value)
            return x_slices

        x_slices = get_x_slices(dx=0.25)
        self.add(x_slice, x_slices, graph, graph_mesh)
        self.play(
            FadeOut(graph, time_span=(0, 1)),
            FadeOut(x_slice, time_span=(0, 1)),
            FadeIn(x_slices, 0.1 * OUT, lag_ratio=0.1),
            axes.labels[2].animate.set_opacity(0),
            frame.animate.reorient(-80),
            run_time=4
        )
        self.play(
            frame.animate.reorient(-100),
            run_time=3,
        )
        self.wait()
        y_tracker.set_value(-x_max)
        self.add(x_slice, x_slices, graph, graph_mesh)
        self.play(
            FadeOut(x_slices, 0.1 * IN, time_span=(0, 2.5)),
            FadeIn(graph, time_span=(0, 2.5)),
            VFadeIn(x_slice),
            frame.animate.reorient(-15).set_height(6),
            y_tracker.animate.set_value(0),
            run_time=5,
        )

        # Discuss area of each slice
        tex_kw = dict(
            font_size=42,
            t2c={"x": BLUE, "y": YELLOW}
        )
        get_y = y_tracker.get_value
        x_slice_label = Tex("0.00 e^{-x^2}", **tex_kw)
        coef = x_slice_label.make_number_changeable("0.00")
        coef.set_color(YELLOW)
        coef.add_updater(lambda m: m.set_value(math.exp(-get_y()**2)).rotate(90 * DEGREES, RIGHT))

        x_term = x_slice_label[1:]
        brace = Brace(coef, UP, MED_SMALL_BUFF)
        y_term = Tex("e^{-y^2}", **tex_kw)
        y_term.next_to(brace, UP, SMALL_BUFF)

        y0_label = Tex("y = 0", **tex_kw)
        y0_label.rotate(90 * DEGREES, RIGHT)
        y0_label.next_to(x_slice.pfp(0.35), OUT + LEFT)

        x_slice_label.add(brace, y_term)
        x_slice_label.rotate(90 * DEGREES, RIGHT)
        x_slice_label.add_updater(lambda m: m.next_to(x_slice.pfp(0.6), OUT + RIGHT))

        x_slice_label.save_state()
        y_term.next_to(x_term, LEFT, SMALL_BUFF, aligned_edge=DOWN)
        brace.scale(0, about_edge=IN)
        coef.scale(0, about_edge=IN)
        swap = Swap(x_term, y_term)
        swap.begin()
        swap.update(1)

        func_label = Tex(R"e^{-(x^2 + y^2)}", **tex_kw)
        func_label.rotate(90 * DEGREES, RIGHT)
        func_label.next_to(x_slice_label, OUT, MED_LARGE_BUFF)

        fx0 = Tex(R"e^{-(x^2 + 0^2)} = e^{-x^2}", **tex_kw)
        fx0.rotate(90 * DEGREES, RIGHT)
        fx0.next_to(func_label, IN, MED_LARGE_BUFF, aligned_edge=LEFT)
        fx0["0"].set_color(YELLOW)

        self.always_depth_test = False
        self.play(
            *(
                VShowPassingFlash(mob, time_width=1.5, run_time=3)
                for mob in [
                    x_slice.copy().set_stroke(YELLOW, 8).set_fill(opacity=0).shift(0.02 * OUT),
                    Line(*axes.x_axis.get_start_and_end()).set_stroke(YELLOW, 8).insert_n_curves(40),
                ]
            ),
            Write(y0_label)
        )
        self.wait()

        self.play(FadeIn(func_label))
        self.wait()
        self.play(TransformMatchingTex(func_label.copy(), fx0, lag_ratio=0.025))
        self.wait()
        self.play(FadeOut(fx0, RIGHT, rate_func=running_start))

        self.play(TransformMatchingShapes(func_label.copy(), x_slice_label))
        self.wait()
        self.play(Swap(x_term, y_term, path_arc=0.5 * PI))
        self.play(
            Restore(x_slice_label),
            FadeOut(func_label, OUT),
        )
        self.wait()

        # Note the area
        def get_area_label():
            area_label = TexText(R"Area = $0.00 \cdot C$", font_size=30)
            area_label["C"].set_color(RED)
            num = area_label.make_number_changeable("0.00")
            num.set_value(coef.get_value())
            area_label.rotate(90 * DEGREES, RIGHT)
            area_label.move_to(interpolate(x_slice.get_zenith(), x_slice.get_nadir(), 0.66))
            area_label.shift(0.1 * DOWN)
            return area_label

        self.play(FadeIn(get_area_label(), run_time=3, rate_func=there_and_back_with_pause))

        # Move the slice
        y0_slice_copy = x_slice.copy()
        y0_slice_copy.clear_updaters()
        y0_slice_copy.set_fill(opacity=0)
        self.play(FadeOut(y0_label))
        for value in [-0.5, -0.75, -1]:
            self.play(y_tracker.animate.set_value(value), run_time=3)
            slice_copy = y0_slice_copy.copy().set_opacity(0)
            area_label = get_area_label()
            self.play(FadeIn(area_label))
            self.play(slice_copy.animate.match_y(x_slice).set_stroke(YELLOW, 3, 1))
            self.wait(0.25)
            self.play(slice_copy.animate.match_depth(x_slice, stretch=True, about_edge=IN).set_opacity(0))
            self.wait()
            self.play(FadeOut(area_label))

        # Go back to finer slices
        x_slices = get_x_slices(dx=0.1)
        y_tracker.set_value(-1)

        self.add(x_slices, graph, graph_mesh)
        self.play(
            FadeIn(x_slices, 0.1 * OUT, lag_ratio=0.1, run_time=4),
            FadeOut(graph),
            FadeOut(x_slice, time_span=(3, 4)),
            FadeOut(x_slice_label, time_span=(3, 4)),
            frame.animate.reorient(-83, 72, 0).set_height(8).center().set_anim_args(run_time=5)
        )

        # Ambient rotation
        t0 = self.time
        theta0 = frame.get_theta()
        frame.clear_updaters()
        frame.add_updater(lambda m: m.set_theta(
            theta0 + -0.2 * math.sin(0.1 * (self.time - t0))
        ))
        self.wait(10)

        # Show slice width
        mid_index = len(x_slices) // 2 - 3
        line = Line(x_slices[mid_index].get_zenith(), x_slices[mid_index + 1].get_zenith())
        brace = Brace(Line().set_width(line.get_length()), UP)
        brace.stretch(0.5, 1)
        brace.add(brace.get_tex("dy", buff=SMALL_BUFF).scale(0.75, about_edge=DOWN))
        brace.rotate(90 * DEGREES, RIGHT)
        brace.rotate(90 * DEGREES, IN)
        brace.next_to(line, OUT, buff=0)
        brace.use_winding_fill(False)
        self.play(FadeIn(brace))
        self.wait(60)
