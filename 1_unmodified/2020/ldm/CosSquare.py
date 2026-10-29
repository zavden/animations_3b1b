# ==============================================================================
# Scene:      CosSquare
# Source:     videos/_2020/ldm.py (lines 454-457)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CosSquare.py CosSquare -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SineWave(Scene):
    def construct(self):
        w_axes = self.get_wave_axes()
        square, circle, c_axes = self.get_edge_group()

        self.add(w_axes)
        self.add(square, circle, c_axes)

        theta_tracker = ValueTracker(0)
        c_dot = Dot(color=YELLOW)
        c_line = Line(DOWN, UP, color=GREEN)
        w_dot = Dot(color=YELLOW)
        w_line = Line(DOWN, UP, color=GREEN)

        def update_c_dot(dot, axes=c_axes, tracker=theta_tracker):
            theta = tracker.get_value()
            dot.move_to(axes.c2p(
                np.cos(theta),
                np.sin(theta),
            ))

        def update_c_line(line, axes=c_axes, tracker=theta_tracker):
            theta = tracker.get_value()
            x = np.cos(theta)
            y = np.sin(theta)
            if y == 0:
                y = 1e-6
            line.put_start_and_end_on(
                axes.c2p(x, 0),
                axes.c2p(x, y),
            )

        def update_w_dot(dot, axes=w_axes, tracker=theta_tracker):
            theta = tracker.get_value()
            dot.move_to(axes.c2p(theta, np.sin(theta)))

        def update_w_line(line, axes=w_axes, tracker=theta_tracker):
            theta = tracker.get_value()
            x = theta
            y = np.sin(theta)
            if y == 0:
                y = 1e-6
            line.put_start_and_end_on(
                axes.c2p(x, 0),
                axes.c2p(x, y),
            )

        def get_partial_circle(circle=circle, tracker=theta_tracker):
            result = circle.copy()
            theta = tracker.get_value()
            result.pointwise_become_partial(
                circle, 0, clip(theta / TAU, 0, 1),
            )
            result.set_stroke(RED, width=3)
            return result

        def get_partial_wave(axes=w_axes, tracker=theta_tracker):
            theta = tracker.get_value()
            graph = axes.get_graph(np.sin, x_min=0, x_max=theta, step_size=0.025)
            graph.set_stroke(BLUE, 3)
            return graph

        def get_h_line(axes=w_axes, tracker=theta_tracker):
            theta = tracker.get_value()
            return Line(
                axes.c2p(0, 0),
                axes.c2p(theta, 0),
                stroke_color=RED
            )

        c_dot.add_updater(update_c_dot)
        c_line.add_updater(update_c_line)
        w_dot.add_updater(update_w_dot)
        w_line.add_updater(update_w_line)
        partial_circle = always_redraw(get_partial_circle)
        partial_wave = always_redraw(get_partial_wave)
        h_line = always_redraw(get_h_line)

        self.add(partial_circle)
        self.add(partial_wave)
        self.add(h_line)
        self.add(c_line, c_dot)
        self.add(w_line, w_dot)

        sin_label = OldTex(
            "\\sin\\left(\\theta\\right)",
            tex_to_color_map={"\\theta": RED}
        )
        sin_label.next_to(w_axes.get_top(), UR)
        self.add(sin_label)

        self.play(
            theta_tracker.set_value, 1.25 * TAU,
            run_time=15,
            rate_func=linear,
        )

    def get_wave_axes(self):
        wave_axes = Axes(
            x_min=0,
            x_max=1.25 * TAU,
            y_min=-1.0,
            y_max=1.0,
            x_axis_config={
                "tick_frequency": TAU / 8,
                "unit_size": 1.0,
            },
            y_axis_config={
                "tick_frequency": 0.5,
                "include_tip": False,
                "unit_size": 1.5,
            }
        )
        wave_axes.y_axis.add_numbers(
            -1, 1, num_decimal_places=1
        )
        wave_axes.to_edge(RIGHT, buff=MED_SMALL_BUFF)

        pairs = [
            (PI / 2, "\\frac{\\pi}{2}"),
            (PI, "\\pi"),
            (3 * PI / 2, "\\frac{3\\pi}{2}"),
            (2 * PI, "2\\pi"),
        ]
        syms = VGroup()
        for val, tex in pairs:
            sym = OldTex(tex)
            sym.scale(0.5)
            sym.next_to(wave_axes.c2p(val, 0), DOWN, MED_SMALL_BUFF)
            syms.add(sym)
        wave_axes.add(syms)

        theta = OldTex("\\theta")
        theta.set_color(RED)
        theta.next_to(wave_axes.x_axis.get_end(), UP)
        wave_axes.add(theta)

        return wave_axes

    def get_edge_group(self):
        axes_max = 1.25
        radius = 1.5
        axes = Axes(
            x_min=-axes_max,
            x_max=axes_max,
            y_min=-axes_max,
            y_max=axes_max,
            axis_config={
                "tick_frequency": 0.5,
                "include_tip": False,
                "big_tick_numbers": [-1, 1],
                "tick_size": 0.05,
                "unit_size": radius,
            },
        )
        axes.to_edge(LEFT, buff=MED_LARGE_BUFF)

        background = SurroundingRectangle(axes, buff=MED_SMALL_BUFF)
        background.set_stroke(WHITE, 1)
        background.set_fill(GREY_E, 1)

        circle = Circle(radius=radius)
        circle.move_to(axes)
        circle.set_stroke(WHITE, 1)

        nums = VGroup()
        for u in 1, -1:
            num = Integer(u)
            num.set_height(0.2)
            num.set_stroke(BLACK, 3, background=True)
            num.next_to(axes.c2p(u, 0), DOWN + u * RIGHT, SMALL_BUFF)
            nums.add(num)

        axes.add(nums)

        return background, circle, axes


class CosWave(SineWave):
    CONFIG = {
        "include_square": False,
    }

    def construct(self):
        w_axes = self.get_wave_axes()
        square, circle, c_axes = self.get_edge_group()

        self.add(w_axes)
        self.add(square, circle, c_axes)

        theta_tracker = ValueTracker(0)
        c_dot = Dot(color=YELLOW)
        c_line = Line(DOWN, UP, color=GREEN)
        w_dot = Dot(color=YELLOW)
        w_line = Line(DOWN, UP, color=GREEN)

        def update_c_dot(dot, axes=c_axes, tracker=theta_tracker):
            theta = tracker.get_value()
            dot.move_to(axes.c2p(
                np.cos(theta),
                np.sin(theta),
            ))

        def update_c_line(line, axes=c_axes, tracker=theta_tracker):
            theta = tracker.get_value()
            x = np.cos(theta)
            y = np.sin(theta)
            line.set_points_as_corners([
                axes.c2p(0, y),
                axes.c2p(x, y),
            ])

        def update_w_dot(dot, axes=w_axes, tracker=theta_tracker):
            theta = tracker.get_value()
            dot.move_to(axes.c2p(theta, np.cos(theta)))

        def update_w_line(line, axes=w_axes, tracker=theta_tracker):
            theta = tracker.get_value()
            x = theta
            y = np.cos(theta)
            if y == 0:
                y = 1e-6
            line.set_points_as_corners([
                axes.c2p(x, 0),
                axes.c2p(x, y),
            ])

        def get_partial_circle(circle=circle, tracker=theta_tracker):
            result = circle.copy()
            theta = tracker.get_value()
            result.pointwise_become_partial(
                circle, 0, clip(theta / TAU, 0, 1),
            )
            result.set_stroke(RED, width=3)
            return result

        def get_partial_wave(axes=w_axes, tracker=theta_tracker):
            theta = tracker.get_value()
            graph = axes.get_graph(np.cos, x_min=0, x_max=theta, step_size=0.025)
            graph.set_stroke(PINK, 3)
            return graph

        def get_h_line(axes=w_axes, tracker=theta_tracker):
            theta = tracker.get_value()
            return Line(
                axes.c2p(0, 0),
                axes.c2p(theta, 0),
                stroke_color=RED
            )

        def get_square(line=c_line):
            square = Square()
            square.set_stroke(WHITE, 1)
            square.set_fill(MAROON_B, opacity=0.5)
            square.match_width(line)
            square.move_to(line, DOWN)
            return square

        def get_square_graph(axes=w_axes, tracker=theta_tracker):
            theta = tracker.get_value()
            graph = axes.get_graph(
                lambda x: np.cos(x)**2, x_min=0, x_max=theta, step_size=0.025
            )
            graph.set_stroke(MAROON_B, 3)
            return graph

        c_dot.add_updater(update_c_dot)
        c_line.add_updater(update_c_line)
        w_dot.add_updater(update_w_dot)
        w_line.add_updater(update_w_line)
        h_line = always_redraw(get_h_line)
        partial_circle = always_redraw(get_partial_circle)
        partial_wave = always_redraw(get_partial_wave)

        self.add(partial_circle)
        self.add(partial_wave)
        self.add(h_line)
        self.add(c_line, c_dot)
        self.add(w_line, w_dot)

        if self.include_square:
            self.add(always_redraw(get_square))
            self.add(always_redraw(get_square_graph))

        cos_label = OldTex(
            "\\cos\\left(\\theta\\right)",
            tex_to_color_map={"\\theta": RED}
        )
        cos_label.next_to(w_axes.get_top(), UR)
        self.add(cos_label)

        self.play(
            theta_tracker.set_value, 1.25 * TAU,
            run_time=15,
            rate_func=linear,
        )


class CosSquare(CosWave):
    CONFIG = {
        "include_square": True
    }
