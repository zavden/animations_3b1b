# ==============================================================================
# Scene:      RealExtension
# Source:     videos/_2025/laplace/main_equations.py (lines 1384-1494)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RealExtension.py RealExtension -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RealExtension(InteractiveScene):
    def construct(self):
        # Show limited domain
        axes = Axes((-1, 10), (-1, 5), width=FRAME_WIDTH - 1, height=6)
        self.add(axes)

        def func(x):
            decay = math.exp(-0.05 * (x + 1))
            poly = -0.003 * x**3 - 0.2 * (0.15 * x)**2 + 0.2 * x
            return (decay + 0.5) * (math.cos(1.0 * x) + 1.5) + poly

        limited_domain = (2, 6)

        partial_graph = axes.get_graph(func, x_range=limited_domain)
        partial_graph.set_stroke(BLUE, 5)
        f_label = Tex(R"f(x)")
        f_label.next_to(partial_graph.get_end(), UL)

        limited_domain_line = Line(
            axes.c2p(limited_domain[0], 0),
            axes.c2p(limited_domain[1], 0),
        )
        limited_domain_line.set_stroke(BLUE, 5)
        limited_domain_words = Text("Limited Domain")
        limited_domain_words.next_to(limited_domain_line, UP, SMALL_BUFF)

        self.add(axes)
        self.play(
            ShowCreation(partial_graph),
            Write(f_label)
        )
        self.play(
            ShowCreation(limited_domain_line),
            FadeIn(limited_domain_words, lag_ratio=0.1)
        )
        self.wait()
        self.play(TransformFromCopy(limited_domain_line, partial_graph))
        self.wait()

        # Extend the graph
        points = partial_graph.get_anchors()

        def get_extension(nudge_size=0):
            pre_xs = np.arange(1, -2, -1)
            post_xs = np.arange(7, 11)
            result = VGroup(
                self.get_extension(axes, points[3::-1], pre_xs, func, nudge_size=nudge_size),
                self.get_extension(axes, points[-4:], post_xs, func, nudge_size=nudge_size),
            )
            result[0].set_clip_plane(LEFT, axes.c2p(limited_domain[0], 0)[0])
            result[1].set_clip_plane(RIGHT, -axes.c2p(limited_domain[1], 0)[0])
            return result

        extension = get_extension()
        self.play(ShowCreation(extension, lag_ratio=0, run_time=4))

        # Change around
        extension.save_state()
        for n in range(5):
            new_extension = get_extension(nudge_size=3)
            self.play(extension.animate.become(new_extension), run_time=1)
        self.play(Restore(extension))

        # Show a derivative
        x_tracker = ValueTracker(limited_domain[0])
        tan_line = always_redraw(lambda : axes.get_tangent_line(
            x_tracker.get_value(), partial_graph, length=2
        ).set_stroke(WHITE, 3))

        self.play(GrowFromCenter(tan_line, suspend_mobject_updating=True))
        self.play(x_tracker.animate.set_value(limited_domain[1]), run_time=5)
        self.play(FadeOut(tan_line, suspend_mobject_updating=True))

        # Wiggly spaghetti
        def tweaked_func(x):
            x0, x1 = limited_domain
            if x < x0:
                return func(x) + 0.5 * (x - x0)**2
            elif x < x1:
                return func(x)
            else:
                return func(x) - 0.5 * (x - x1)**2

        full_graph = axes.get_graph(func)
        modifed_graph = axes.get_graph(tweaked_func)

        group = VGroup(full_graph, modifed_graph)
        group.set_stroke(RED, 5)
        group.set_z_index(-1)

        self.play(
            FadeOut(extension),
            FadeIn(full_graph),
        )
        self.play(
            full_graph.animate.become(modifed_graph),
            rate_func=lambda t: wiggle(t, 5),
            run_time=8
        )

    def get_extension(self, axes, pre_start, xs, func, nudge_size=0, stroke_width=5, stroke_color=RED):
        ys = np.array([func(x) + (nudge_size * (random.random() - 0.5)) for x in xs])
        new_points = axes.c2p(xs, ys)

        result = VMobject()
        result.set_points_smoothly([*pre_start, *new_points], approx=False)
        result.insert_n_curves(100)

        result.set_stroke(stroke_color, stroke_width)
        result.set_z_index(-1)
        return result
