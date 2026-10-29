# ==============================================================================
# Scene:      AbstractGraphOfLossFunction
# Source:     videos/_2026/cross_entropy/language_models.py (lines 553-755)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AbstractGraphOfLossFunction.py AbstractGraphOfLossFunction -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
import numpy as np

class AbstractGraphOfLossFunction(InteractiveScene):
    xy_init = (1.5, -3.75)
    # xy_init = (1.9, 3.75)

    def construct(self):
        # Set up graph
        frame = self.frame
        x_range = (-4, 4)
        axes = ThreeDAxes(x_range, x_range, (0, 5))
        plane = NumberPlane(x_range, x_range)
        plane.move_to(axes.get_origin())
        plane.background_lines.set_stroke(BLUE_D, 1, 0.5)
        plane.faded_lines.set_stroke(BLUE_E, 1, 0.2)

        def func(x, y):
            return 0.1 * (x * x + y * y) + np.sin(x) + 1.5

        graph = axes.get_graph(func)
        graph.set_color(RED, 0.5)
        graph.always_sort_to_camera(self.camera)

        mesh = SurfaceMesh(graph)
        mesh.set_stroke(WHITE, 1, 0.1)
        mesh.deactivate_depth_test()

        # Add graph indicators
        network = self.get_network()
        network.set_width(1)
        network.move_to(plane.c2p(*self.xy_init))

        line_kw = dict(
            dash_length=0.025,
            stroke_color=RED,
            stroke_width=1
        )

        def point_to_graph(point):
            x, y = plane.p2c(point)
            return axes.c2p(x, y, func(x, y))

        def get_v_line():
            in_point = network.get_center()
            return DashedLine(
                in_point, point_to_graph(in_point),
                **line_kw
            )

        v_line = always_redraw(get_v_line)
        graph_dot = Group(TrueDot().make_3d(), GlowDot())
        graph_dot.set_color(RED)
        graph_dot.f_always.move_to(v_line.get_end)

        # Add loss indicator
        loss_label = Text("Loss")
        loss_label.set_color(RED)
        loss_label.rotate(90 * DEG, RIGHT)
        loss_label.next_to(axes.z_axis, OUT, SMALL_BUFF)
        h_line = always_redraw(lambda: DashedLine(
            v_line.get_end(), axes.z_axis.n2p(axes.z_axis.p2n(v_line.get_end())),
            **line_kw
        ))

        loss_tracker = ValueTracker(4.78)
        get_loss = loss_tracker.get_value

        def get_loss_dec():
            loss = get_loss()
            dec = DecimalNumber(loss, fill_color=RED)
            dec.rotate(90 * DEG, RIGHT)
            dec.next_to(axes.z_axis.n2p(loss), LEFT, buff=0.2)
            return dec

        loss_dec = always_redraw(get_loss_dec)

        # Just show z_axis
        loss_slider = ArrowTip()
        loss_slider.rotate(PI).set_width(0.25)
        loss_slider.rotate(90 * DEG, RIGHT)
        loss_slider.set_color(RED)
        loss_slider.add_updater(lambda m: m.move_to(axes.z_axis.n2p(get_loss()), LEFT))

        loss_func_label = Text("Loss(model)")
        loss_func_label["Loss"].set_color(RED)
        loss_func_label.rotate(90 * DEG, RIGHT)
        loss_func_label.always.next_to(loss_slider, RIGHT)

        brace_lines = DashedLine(ORIGIN, RIGHT).get_grid(2, 1, buff=LARGE_BUFF)
        brace = Brace(brace_lines, LEFT, buff=SMALL_BUFF)
        brace_group = VGroup(brace, brace_lines)
        brace_group.rotate(90 * DEG, RIGHT)
        brace_group.next_to(axes.z_axis, LEFT, buff=0, aligned_edge=IN)

        words = VGroup(Text("Good"), Text("Bad"))
        words.rotate(90 * DEG, RIGHT)
        for word in words:
            word.always.next_to(brace, LEFT)

        frame.reorient(0, 90, 0, (-1.69, 0.68, 1.97), 8.00).set_field_of_view(1 * DEG)
        self.add(axes.z_axis, loss_dec, loss_slider, loss_func_label)

        self.play(
            loss_tracker.animate.set_value(0.43),
            FadeIn(brace_group),
            FadeIn(words[0]),
            run_time=2
        )
        self.wait()
        self.play(LaggedStart(
            brace_group.animate.stretch(2, 2).next_to(axes.z_axis.n2p(5), IN + LEFT, buff=0),
            VFadeOut(words[0]),
            VFadeIn(words[1]),
            loss_tracker.animate.set_value(axes.z_axis.p2n(v_line.get_end())),
            run_time=2
        ))
        self.wait()

        # Transition
        self.play(
            frame.animate.reorient(-28, 70, 0, (0.39, 0.18, 1.18), 10.55).set_field_of_view(45 * DEG),
            FadeOut(loss_func_label[4:]),
            ReplacementTransform(loss_func_label[:4], loss_label),
            FadeOut(loss_slider),
            FadeOut(brace_group),
            FadeOut(words[1]),
            Write(plane),
            ShowCreation(graph),
            Write(mesh),
            run_time=2
        )
        frame.add_ambient_rotation(1 * DEG)
        self.play(
            FadeIn(network, scale=3),
            ShowCreation(v_line, suspend_mobject_updating=True),
            ShowCreation(h_line, suspend_mobject_updating=True),
            FadeIn(graph_dot),
        )
        loss_tracker.add_updater(lambda m: m.set_value(axes.z_axis.p2n(v_line.get_end())))
        self.add(loss_tracker)

        # Iterations of gradient descent
        n_steps = 15
        learning_rate = 0.5
        epsilon = 1e-2

        for n in range(n_steps):
            point = network.get_center()
            x, y = plane.p2c(point)
            del_x = (func(x + epsilon, y) - func(x, y)) / epsilon
            del_y = (func(x, y + epsilon) - func(x, y)) / epsilon
            new_point = plane.c2p(
                x - learning_rate * del_x,
                y - learning_rate * del_y,
            )
            arrow = Arrow(point, new_point, thickness=5, buff=0)
            arrow.set_fill(YELLOW)
            arrow.scale(2, about_point=arrow.get_start())
            anims = [
                network.animate.move_to(new_point), VFadeInThenOut(arrow, run_time=2)
            ]
            self.play(*anims)
        self.wait()

    def get_network(self, layer_sizes=[3, 5, 5, 3]):
        layers = VGroup(
            Dot().get_grid(size, 1, buff=0.1)
            for size in layer_sizes
        )
        layers.arrange(RIGHT, buff=0.3)
        for layer in layers:
            for dot in layer:
                dot.set_stroke(WHITE, 1)
                dot.set_fill(WHITE, random.random())

        lines = VGroup()
        for l1, l2 in zip(layers, layers[1:]):
            lines.add(VGroup(
                Line(
                    n1.get_center(), n2.get_center(),
                    buff=n1.get_width() / 2,
                    stroke_width=random.random(),
                    stroke_color=random.choice([RED, BLUE])
                )
                for n1, n2 in it.product(l1, l2)
            ))

        return VGroup(layers, lines)

    def insert(self):
        # To be placed before transition
        self.remove(loss_dec)
        frame.reorient(22, 80, 0, (0.39, 0.18, 1.18), 10.55)
        graph.save_state()
        mesh.save_state()
        graph.stretch(0, 2).move_to(plane).set_opacity(0),
        mesh.stretch(0, 2).move_to(plane).set_opacity(0),
        self.play(
            frame.animate.reorient(-28, 70, 0, (0.39, 0.18, 1.18), 10.55),
            Restore(graph),
            Restore(mesh),
            run_time=2
        )
        frame.add_ambient_rotation(2 * DEG)
        self.wait(3)
