# ==============================================================================
# Scene:      MoveAroundPolesSeeDynamics
# Source:     videos/_2025/laplace/derivatives.py (lines 40-213)
# Category:   1 · Renders unmodified
# Includes code copied from: _2025/laplace/integration.py
#
# Run from this folder:
#     manimgl MoveAroundPolesSeeDynamics.py MoveAroundPolesSeeDynamics -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2025/laplace/integration.py -----

def z_to_color(z, sat=0.5, lum=0.5):
    angle = math.atan2(z.imag, z.real)
    return Color(hsl=(angle / TAU, sat, lum))


def get_complex_graph(
    s_plane,
    func,
    min_real=None,
    pole_buff=1e-3,
    color_by_phase=True,
    opacity=0.7,
    shading=(0.1, 0.1, 0.1),
    resolution=(301, 301),
    saturation=0.5,
    luminance=0.5,
    mesh_resolution=(61, 61),
    mesh_stroke_style=dict(
        color=WHITE,
        width=1,
        opacity=0.15
    )
):
    u_range = list(s_plane.x_range[:2])
    v_range = list(s_plane.y_range[:2])

    if min_real is not None:
        u_range[0] = min_real + pole_buff

    unit_size = s_plane.x_axis.get_unit_size()
    graph = ParametricSurface(
        lambda u, v: [
            *s_plane.c2p(u, v)[:2],
            unit_size * abs(func(complex(u, v)))
        ],
        u_range=u_range,
        v_range=v_range,
        resolution=resolution
    )
    graph.set_shading(*shading)

    if color_by_phase:
        graph.color_by_uv_function(
            lambda u, v: z_to_color(func(complex(u, v)), sat=saturation, lum=luminance)
        )

    graph.set_opacity(opacity)
    graph.set_sort_to_camera()

    # Add mesh
    mesh = SurfaceMesh(graph, resolution=mesh_resolution)
    mesh.set_stroke(**mesh_stroke_style)

    return Group(graph, mesh)



# ----- From _2025/laplace/derivatives.py -----

class MoveAroundPolesSeeDynamics(InteractiveScene):
    def construct(self):
        # Add s_plane (and graph)
        frame = self.frame
        s_plane = ComplexPlane((-3, 3), (-3, 3))
        s_plane.add_coordinate_labels(font_size=20)

        s_trackers = Group(
            ComplexValueTracker(+2j),
            ComplexValueTracker(-2j),
            ComplexValueTracker(+1.0j - 0.2),
            ComplexValueTracker(-1.0j - 0.2),
            ComplexValueTracker(-1.0),
        )

        t_tracker = ValueTracker(0)
        t_tracker.add_updater(lambda m, dt: m.increment_value(dt))
        get_t = t_tracker.get_value

        s_points = Group(TrueDot(), GlowDot()).replicate(len(s_trackers))
        s_points.set_color(YELLOW)
        for point, s_tracker in zip(s_points, s_trackers):
            point.s_tracker = s_tracker
            point.add_updater(lambda m: m.move_to(s_plane.n2p(m.s_tracker.get_value())))

        frame.reorient(-14, 82, 0, (-4.89, 2.68, 3.02), 10.32)
        self.add(t_tracker)

        # Add title
        arrow = Vector(3 * RIGHT, thickness=6)
        kw = dict(
            t2c={"t": BLUE, "s": YELLOW},
            font_size=72
        )
        title = VGroup(Tex(R"f(t)", **kw), arrow, Tex(R"F(s)", **kw))
        title.arrange(RIGHT)
        title.to_edge(UP)
        lt_label = Tex(R"\mathcal{L}")
        lt_label.next_to(arrow, UP, buff=0)
        arrow.add(lt_label)
        title.fix_in_frame()

        self.add(title[0])

        # Add time graph
        axes = Axes((0, 15), (-2, 2), width=6, height=3)
        axes.to_edge(LEFT)
        axes.shift(2 * DOWN)
        time_graph = axes.get_graph(self.get_time_func(s_trackers, amp=0.4))
        time_graph.set_stroke(BLUE, 2)
        axes.fix_in_frame()
        time_graph.fix_in_frame()

        self.add(axes, time_graph)

        # Add mass
        amp_factor_tracker = ValueTracker(2.0)

        number_line = NumberLine((-2, 2), width=6)
        number_line.next_to(axes, UP, LARGE_BUFF)
        number_line.add_numbers(font_size=16)
        number_line.fix_in_frame()

        tip = ArrowTip(angle=-90 * DEG)
        tip.stretch(0.25, 0)
        tip.func = self.get_time_func(s_trackers, amp=0.4)
        tip.add_updater(lambda m: m.move_to(number_line.n2p(m.func(get_t())), DOWN))
        tip.fix_in_frame()

        mass = Square(side_length=0.5)
        mass.set_fill(BLUE_E, 1)
        mass.set_stroke(WHITE, 2)
        mass.always.next_to(tip, UP)
        mass.fix_in_frame()
        mass_ghost = mass.copy()
        mass_ghost.set_opacity(0)

        v_vect = always_redraw(lambda: Arrow(
            mass.get_center(),
            mass.get_center() + np.clip(5 * (mass.get_center() - mass_ghost.get_center()), -1, 1),
            buff=0,
            thickness=4,
            fill_color=RED
        ).fix_in_frame())

        self.add(number_line, tip, mass, v_vect, mass_ghost)
        self.wait(5)

        # Show graph
        epsilon = 1e-5

        def get_graph():
            graph = get_complex_graph(
                s_plane,
                self.get_s_func(s_trackers),
                # resolution=(101, 101)
                # resolution=(31, 31)
            )
            for line in graph[1]:
                if line.get_z(OUT) > 1e3:
                    line.set_stroke(opacity=0)
            return graph

        def update_graph(graph):
            graph.become(get_graph())

        graph = get_graph()

        self.play(
            FadeIn(s_plane, lag_ratio=0.01),
            FadeIn(s_points),
            FadeIn(graph[0]),
            Write(graph[1]),
            Write(title[1]),
            FadeIn(title[2], RIGHT)
        )
        self.play(
            frame.animate.reorient(0, 0, 0, (-5.0, 1.08, 0.0), 9.62).set_field_of_view(10 * DEG),
            run_time=3
        )
        self.wait(8)

        # Move s
        t_tracker.set_value(0)
        s_trackers.remove(*s_trackers[2:])
        s_trackers[1].add_updater(lambda m: m.set_value(s_trackers[0].get_value().conjugate()))
        s_tracker = s_trackers[0]
        s_tracker.set_value(2j)

        amp_tracker = ValueTracker(1)

        time_graph.add_updater(lambda m: m.match_points(axes.get_graph(self.get_time_func(s_trackers))))
        time_graph.set_clip_plane(DOWN, 0)

        def new_func(t):
            return amp_tracker.get_value() * math.cos(2 * t)

        tip.func = new_func

        update_graph(graph)
        self.add(*s_trackers)
        self.remove(s_points[2:])
        self.wait(10)

        amp_tracker.add_updater(lambda m: m.set_value(0.992 * m.get_value()))
        self.add(amp_tracker)
        self.play(
            s_tracker.animate.set_value(-0.5 + 2j),
            UpdateFromFunc(graph, update_graph),
            run_time=2
        )
        self.wait(4)

        amp_tracker.clear_updaters()
        amp_tracker.add_updater(lambda m: m.set_value(1.005 * m.get_value()))
        self.play(
            s_tracker.animate.set_value(0.2 + 2j),
            UpdateFromFunc(graph, update_graph),
            run_time=3
        )
        self.wait(15)

    def get_time_func(self, s_trackers, amp=0.5):
        def time_func(t):
            return amp * np.sum([np.exp(st.get_value() * t) for st in s_trackers]).real

        return time_func

    def get_s_func(self, s_trackers, epsilon=1e-5, amp=0.5):
        def s_func(s):
            s += epsilon
            return amp * np.sum([1.0 / (s - st.get_value() + epsilon) for st in s_trackers])

        return s_func
