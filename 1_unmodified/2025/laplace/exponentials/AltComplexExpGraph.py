# ==============================================================================
# Scene:      AltComplexExpGraph
# Source:     videos/_2025/laplace/exponentials.py (lines 638-641)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AltComplexExpGraph.py AltComplexExpGraph -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ComplexExpGraph(InteractiveScene):
    s_value = 1j
    orientation1 = (-77, -1, 0, (1.01, -0.1, 3.21), 7.55)
    orientation2 = (-33, -2, 0, (1.68, -0.09, 3.79), 10.88)

    def construct(self):
        # Set up parts
        self.set_floor_plane("xz")
        frame = self.frame

        plane = ComplexPlane((-2, 2), (-2, 2))
        plane.scale(0.75)
        moving_plane = plane.copy()

        t_axis = NumberLine((0, 12))
        t_axis.rotate(90 * DEG, DOWN)
        t_axis.shift(-t_axis.n2p(0))

        self.add(plane)
        self.add(t_axis)

        # Trackers and graph
        t_tracker = ValueTracker(0)
        get_t = t_tracker.get_value
        s = self.s_value

        def get_z():
            return np.exp(s * get_t())

        def z_to_point(z):
            return plane.n2p(z) + get_t() * OUT

        moving_plane.add_updater(lambda m: m.move_to(t_axis.n2p(get_t())))
        point = GlowDot()
        point.add_updater(lambda m: m.move_to(z_to_point(get_z())))
        vector = Vector()
        vector.add_updater(lambda m: m.put_start_and_end_on(
            z_to_point(0),
            z_to_point(get_z())
        ))
        graph = TracedPath(vector.get_end, stroke_color=TEAL)

        t_label = Tex("t = 0.00", font_size=30)
        t_label_rhs = t_label.make_number_changeable("0.00")
        t_label_rhs.add_updater(lambda m: m.set_value(get_t()))
        t_label.add_updater(lambda m: m.next_to(moving_plane, UP, SMALL_BUFF))

        self.add(t_tracker, moving_plane, vector, point, graph)
        self.add(t_label)
        frame.reorient(*self.orientation1)
        self.play(
            frame.animate.reorient(*self.orientation2),
            t_tracker.animate.set_value(12).set_anim_args(rate_func=linear),
            VFadeIn(t_axis, time_span=(0, 1)),
            run_time=12
        )
        self.play(
            frame.animate.reorient(0, -89, -90, (0.06, -0.62, 5.27), 7.42).set_field_of_view(1 * DEG),
            FadeOut(plane),
            FadeOut(moving_plane),
            FadeOut(t_label),
            FadeOut(point),
            FadeOut(vector),
            run_time=3
        )


class AltComplexExpGraph(ComplexExpGraph):
    s_value = -0.2 + 1j
    orientation1 = (-37, -1, 0, (0.08, 0.1, 0.08), 6)
    orientation2 = (-21, -5, 0, (1.47, -0.44, 3.88), 12.29)
