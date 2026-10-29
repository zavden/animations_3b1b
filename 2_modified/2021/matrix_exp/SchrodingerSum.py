# ==============================================================================
# Scene:      SchrodingerSum
# Source:     videos/_2021/matrix_exp.py (lines 5059-5197)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SchrodingerSum.py SchrodingerSum -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - ParametricCurve(t_range=x_range[:2]) -> t_range=(*x_range[:2], 0.1): t_range now needs (min, max, step).
# ==============================================================================

from manim_imports_ext import *

class SchrodingerSum(Scene):
    def construct(self):
        # Add title
        equation_label = VGroup(
            OldTexText("Schrödinger equation:"),
            OldTex(
                "{i} \\hbar \\frac{\\partial}{\\partial t} |\\psi(t)\\rangle = \\hat{H} |\\psi(t)\\rangle",
                tex_to_color_map={
                    "|\\psi(t)\\rangle": BLUE,
                    "{i}": WHITE,
                    "\\frac{\\partial}{\\partial t}": GREY_A,
                },
                font_size=36
            )
        )
        equation_label.arrange(RIGHT, buff=MED_LARGE_BUFF)
        equation_label.set_width(FRAME_WIDTH - 1)
        equation_label.to_edge(UP)
        i_part = equation_label[1].get_part_by_tex("{i}")
        self.add(equation_label)

        # Axes
        x_range = np.array([-5, 5, 1])
        y_range = np.array([-1, 1, 0.5])
        axes = ThreeDAxes(
            x_range=x_range,
            y_range=y_range,
            z_range=y_range,
            height=1.25,
            depth=1.25,
            width=4,
            axis_config={"include_tip": False, "tick_size": 0.05},
        )
        # plane = ComplexPlane(y_range, y_range)
        # plane.rotate(PI / 2, DOWN)
        # plane.match_depth(axes)
        # axes.add(plane)
        # axes.y_axis.set_opacity(0)
        # axes.z_axis.set_opacity(0)

        lil_axes = VGroup(*(axes.deepcopy() for x in range(3)))
        lil_axes.arrange(DOWN, buff=MED_LARGE_BUFF)
        lil_axes.to_corner(DL)
        brace = Brace(lil_axes, RIGHT, buff=MED_LARGE_BUFF)
        axes.scale(2)
        axes.next_to(brace, RIGHT)

        for ax in [axes, *lil_axes]:
            ax.rotate(-30 * DEGREES, UP)
            ax.rotate(10 * DEGREES, RIGHT)
            ax.set_flat_stroke(False)

        # Graphs
        def func0(x, t):
            magnitude = np.exp(-x * x / 2)
            phase = np.exp(complex(0, 0.5 * t))
            return magnitude * phase

        def func1(x, t):
            magnitude = np.exp(-x * x / 2) * 2 * x
            magnitude *= 1 / math.sqrt(2)
            phase = np.exp(complex(0, 1.5 * t))
            return magnitude * phase

        def func2(x, t):
            magnitude = -1 * np.exp(-x * x / 2) * (2 - 4 * x * x)
            magnitude *= 1 / math.sqrt(8)
            phase = np.exp(complex(0, 2.5 * t))
            return magnitude * phase

        def comb_func(x, t):
            return (func0(x, t) + func1(x, t) + func2(x, t)) / 3

        def to_xyz(func, x):
            z = func(x, get_t())
            return (x, z.real, z.imag)

        t_tracker = ValueTracker()
        t_tracker.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(t_tracker)
        get_t = t_tracker.get_value

        def get_graph(axes, func, color):
            fade_tracker = ValueTracker(1)
            result = VGroup()
            graph = always_redraw(lambda: ParametricCurve(
                lambda x: axes.c2p(*to_xyz(func, x)),
                # CHANGE: ParametricCurve requires t_range with 3 values (min, max, step)
                t_range=(*x_range[:2], 0.1),
                color=color,
                stroke_opacity=fade_tracker.get_value(),
                flat_stroke=False,
            ))
            result.add(graph)
            for x in np.linspace(0, 1, 100):
                line = Line(stroke_color=color, stroke_width=2)
                line.x = x
                line.axes = axes
                line.graph = graph
                line.fade_tracker = fade_tracker
                line.add_updater(lambda m: m.set_points_as_corners([
                    m.axes.x_axis.pfp(m.x),
                    m.graph.pfp(m.x),
                ]).set_opacity(0.5 * m.fade_tracker.get_value()))
                result.add(line)
            result.fade_tracker = fade_tracker
            return result

        graph0, graph1, graph2, comb_graph = graphs = [
            get_graph(axes, func, color)
            for axes, func, color in zip(
                [*lil_axes, axes],
                [func0, func1, func2, comb_func],
                [BLUE, TEAL, GREEN, YELLOW]
            )
        ]

        lil_axes[1].save_state()
        lil_axes[1].scale(2)
        lil_axes[1].move_to(DOWN)

        self.add(lil_axes[1], graph1)
        self.wait(10)
        self.add(*graphs)
        self.play(
            FadeIn(lil_axes[::2]),
            FadeIn(axes),
            Restore(lil_axes[1]),
            GrowFromCenter(brace),
            *(
                UpdateFromAlphaFunc(g.fade_tracker, lambda m, a: m.set_value(a))
                for g in (*graphs[::2], comb_graph)
            )
        )
        self.wait(15)
        self.play(
            FlashAround(i_part, color=RED),
            i_part.animate.set_color(RED)
        )
        self.wait(30)
