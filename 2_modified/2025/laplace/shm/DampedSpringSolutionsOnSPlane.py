# ==============================================================================
# Scene:      DampedSpringSolutionsOnSPlane
# Source:     videos/_2025/laplace/shm.py (lines 768-948)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl DampedSpringSolutionsOnSPlane.py DampedSpringSolutionsOnSPlane -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The image LaplaceFormulaStill.png is read next to the file instead of from Grant's Dropbox
#   - LaplaceFormulaStill.png is a placeholder image: the quadratic formula s = (-mu ± sqrt(mu^2 - 4mk)) / 2m on a black background
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/generated/2025/laplace/LaplaceFormulaStill.png
#
# Notes:
#   LaplaceFormulaStill.png is not public. It was reconstructed as the quadratic formula for the roots of m s^2 + mu s + k (what the points of the s plane show; the code's s_rhs_point is the start of the right-hand side of 's = ...') with make_LaplaceFormulaStill.py. It is an approximation, not Grant's frame.
# ==============================================================================

from manim_imports_ext import *

class DampedSpringSolutionsOnSPlane(InteractiveScene):
    def construct(self):
        # Add the plane
        plane = ComplexPlane((-3, 2), (-2, 2))
        plane.set_height(5)
        plane.background_lines.set_stroke(BLUE, 1)
        plane.faded_lines.set_stroke(BLUE, 0.5, 0.25)
        plane.add_coordinate_labels(font_size=24)
        plane.move_to(DOWN)
        plane.to_edge(RIGHT, buff=1.0)
        self.add(plane)

        # Add the sliders
        colors = [interpolate_color_by_hsl(RED, TEAL, a) for a in np.linspace(0, 1, 3)]
        chars = ["m", R"\mu", "k"]
        m_slider, mu_slider, k_slider = sliders = VGroup(
            self.get_slider(char, color)
            for char, color in zip(chars, colors)
        )
        m_tracker, mu_tracker, k_tracker = trackers = Group(
            slider.value_tracker for slider in sliders
        )
        sliders.arrange(RIGHT, buff=MED_LARGE_BUFF)
        sliders.next_to(plane, UP, aligned_edge=LEFT)

        for tracker, value in zip(trackers, [1, 0, 3]):
            tracker.set_value(value)

        self.add(trackers)
        self.add(sliders[0], sliders[2])

        # Add the dots
        def get_roots():
            a, b, c = [t.get_value() for t in trackers]
            m = -b / 2
            p = c / a
            disc = m**2 - p
            radical = math.sqrt(disc) if disc >= 0 else 1j * math.sqrt(-disc)
            return (m + radical, m - radical)

        def update_dots(dots):
            roots = get_roots()
            for dot, root in zip(dots, roots):
                dot.move_to(plane.n2p(root))

        root_dots = GlowDot().replicate(2)
        root_dots.add_updater(update_dots)

        s_rhs_point = Point((-4.09, -1.0, 0.0))
        rect_edge_point = (-3.33, -1.18, 0.0)

        def update_lines(lines):
            for line, dot in zip(lines, root_dots):
                line.put_start_and_end_on(
                    s_rhs_point.get_center(),
                    dot.get_center(),
                )

        lines = Line().replicate(2)
        lines.set_stroke(YELLOW, 2, 0.35)
        lines.add_updater(update_lines)

        self.add(root_dots)

        # Play with k
        self.play(ShowCreation(lines, lag_ratio=0, suspend_mobject_updating=True))
        self.play(k_tracker.animate.set_value(1), run_time=2)
        self.play(m_tracker.animate.set_value(4), run_time=2)
        self.wait()
        self.play(k_tracker.animate.set_value(3), run_time=2)
        self.play(m_tracker.animate.set_value(1), run_time=2)
        self.wait()

        # Play with mu
        self.play(
            s_rhs_point.animate.move_to(rect_edge_point),
            VFadeOut(lines),
            VFadeIn(sliders[1])
        )
        self.wait()
        self.play(mu_tracker.animate.set_value(3), run_time=5)
        self.wait()
        self.play(mu_tracker.animate.set_value(0.5), run_time=3)
        self.play(ShowCreation(lines, lag_ratio=0, suspend_mobject_updating=True))

        # Background
        self.add_background_image()

        # Zoom out and show graph
        frame = self.frame

        axes = Axes((0, 10, 1), (-1, 1, 1), width=10, height=3.5)
        axes.next_to(plane, DOWN, MED_LARGE_BUFF, aligned_edge=LEFT)

        def func(t):
            roots = get_roots()
            return 0.5 * (np.exp(roots[0] * t) + np.exp(roots[1] * t)).real

        graph = axes.get_graph(func)
        graph.set_stroke(TEAL, 3)
        axes.bind_graph_to_func(graph, func)

        graph_label = Tex(R"\text{Re}[e^{st}]", t2c={"s": YELLOW}, font_size=72)
        graph_label.next_to(axes.get_corner(UL), DL)

        self.play(
            frame.animate.set_height(12, about_point=4 * UP + 2 * LEFT),
            FadeIn(axes, time_span=(1.5, 3)),
            ShowCreation(graph, suspend_mobject_updating=True, time_span=(1.5, 3)),
            Write(graph_label),
            run_time=3
        )
        self.wait()

        # Show exponential decay
        exp_graph = axes.get_graph(lambda t: np.exp(get_roots()[0].real * t))
        exp_graph.set_stroke(WHITE, 1)

        self.play(ShowCreation(exp_graph))
        self.wait()

        # More play
        self.play(k_tracker.animate.set_value(1), run_time=2)
        self.play(k_tracker.animate.set_value(4), run_time=2)
        self.play(FadeOut(exp_graph))
        self.wait()
        self.play(mu_tracker.animate.set_value(2), run_time=3)
        self.play(k_tracker.animate.set_value(2), run_time=2)
        self.wait()
        self.play(mu_tracker.animate.set_value(3.5), run_time=3)
        self.play(k_tracker.animate.set_value(5), run_time=2)
        self.wait()
        self.play(
            mu_tracker.animate.set_value(0.5),
            m_tracker.animate.set_value(3),
            run_time=3
        )
        self.wait()

        # Smooth all the way to end
        self.play(mu_tracker.animate.set_value(4.2), run_time=12)

    def add_background_image(self):
        # CHANGE: the image lived in Grant's Dropbox; now it is next to this file (placeholder image with the quadratic formula).
        image = ImageMobject(str(Path(__file__).parent / 'LaplaceFormulaStill.png'))
        image.replace(self.frame)
        image.set_z_index(-1)
        self.background_image = image
        self.add(image)

    def get_slider(self, char_name, color=WHITE, x_range=(0, 5), height=1.5, font_size=36):
        tracker = ValueTracker(0)
        number_line = NumberLine(x_range, width=height, tick_size=0.05)
        number_line.rotate(90 * DEG)

        indicator = ArrowTip(width=0.1, length=0.2)
        indicator.rotate(PI)
        indicator.add_updater(lambda m: m.move_to(number_line.n2p(tracker.get_value()), LEFT))
        indicator.set_color(color)

        label = Tex(Rf"{char_name} = 0.00", font_size=font_size)
        label[char_name].set_color(color)
        label.rhs = label.make_number_changeable("0.00")
        label.always.next_to(indicator, RIGHT, SMALL_BUFF)
        label.rhs.f_always.set_value(tracker.get_value)

        slider = VGroup(number_line, indicator, label)
        slider.value_tracker = tracker
        return slider

    def insertion(self):
        # Insertion after "play with mu" above
        self.wait()
        self.play(mu_tracker.animate.set_value(3), run_time=3)
        self.play(k_tracker.animate.set_value(1), run_time=2)
        self.play(k_tracker.animate.set_value(4), run_time=2)
        self.wait()
        self.play(mu_tracker.animate.set_value(4), run_time=2)
        self.play(k_tracker.animate.set_value(0.5), run_time=2)
        self.wait()
        self.play(mu_tracker.animate.set_value(0.5), run_time=4)
        self.play(k_tracker.animate.set_value(2), run_time=4)
