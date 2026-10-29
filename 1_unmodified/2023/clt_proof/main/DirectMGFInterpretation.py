# ==============================================================================
# Scene:      DirectMGFInterpretation
# Source:     videos/_2023/clt_proof/main.py (lines 460-598)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DirectMGFInterpretation.py DirectMGFInterpretation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DirectMGFInterpretation(InteractiveScene):
    random_seed = 4
    n_samples = 30

    def construct(self):
        # Graph
        t_tracker = ValueTracker(1)
        get_t = t_tracker.get_value
        axes = Axes((-2, 2), (0, 15), width=8, height=7)
        axes.x_axis.add(Tex("x").next_to(
            axes.x_axis.get_right(), UR, SMALL_BUFF)
        )

        def get_exp_graph():
            t = get_t()
            graph = axes.get_graph(lambda x: np.exp(t * x))
            graph.set_stroke(BLUE, 2)
            return graph

        exp_graph = get_exp_graph()
        kw = dict(t2c={"t": YELLOW})
        graph_label = VGroup(
            Tex("e^{tX}", **kw).scale(1.3),
            Tex("t = 1.00", **kw),
        )
        graph_label.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        graph_label.to_corner(UR).shift(3 * LEFT)
        value = graph_label[1].make_number_changeable("1.00")
        value.add_updater(lambda m: m.set_value(get_t()))

        self.add(axes)
        self.add(exp_graph)
        self.add(graph_label)

        # Prepare samples
        samples = np.random.uniform(-2, 2, self.n_samples)

        def get_sample_group(samples):
            ys = np.exp(get_t() * samples)
            y_points = axes.y_axis.n2p(ys)
            x_points = axes.x_axis.n2p(samples)
            graph_points = axes.c2p(samples, ys)
            v_lines = VGroup(*(
                Line(xp, gp)
                for xp, gp in zip(x_points, graph_points)
            ))
            h_lines = VGroup(*(
                Line(gp, yp)
                for gp, yp in zip(graph_points, y_points)
            ))
            lines = VGroup(v_lines, h_lines)
            lines.set_stroke(WHITE, 1, 0.7)

            kw = dict(radius=0.075, glow_factor=1)
            x_dots = Group(*(GlowDot(point, color=YELLOW, **kw) for point in x_points))
            y_dots = Group(*(GlowDot(point, color=RED, **kw) for point in y_points))

            sample_group = Group(x_dots, v_lines, h_lines, y_dots)
            return sample_group

        def get_Ey():
            return np.exp(get_t() * samples).mean()

        x_dots, v_lines, h_lines, y_dots = s_group = get_sample_group(samples)

        # Show samples
        sample_arrows = VGroup(*(
            Vector(0.5 * DOWN).next_to(dot, UP, buff=0)
            for dot in x_dots
        ))
        sample_arrows.set_color(YELLOW)
        sample_words = Text("Samples of X")
        sample_words.next_to(sample_arrows, UP, aligned_edge=LEFT)

        self.play(
            # FadeIn(sample_words, time_span=(0, 1)),
            LaggedStartMap(VFadeInThenOut, sample_arrows, lag_ratio=0.1),
            LaggedStartMap(FadeIn, x_dots, lag_ratio=0.1),
            run_time=1,
        )
        # self.play(FadeOut(sample_words))

        # Show outputs
        Ey_tip = ArrowTip()
        Ey_tip.scale(0.5)
        Ey_tip.add_updater(lambda m: m.move_to(axes.y_axis.n2p(get_Ey()), RIGHT))
        Ey_label = Tex(R"\mathds{E}[e^{tX}]", **kw)
        Ey_label.add_updater(lambda m: m.next_to(Ey_tip, LEFT))

        y_dots.save_state()
        y_dots.set_points([l.get_end() for l in v_lines])
        for dot in y_dots:
            dot.set_radius(0)

        self.play(ShowCreation(v_lines, lag_ratio=0.3, run_time=2))
        self.wait()
        self.play(
            Restore(y_dots, lag_ratio=0),
            ShowCreation(h_lines, lag_ratio=0),
            run_time=2,
        )

        yd_mover = y_dots.copy()
        yd_mover.generate_target()
        points = yd_mover.get_points().copy()
        points[:] = Ey_tip.get_start()
        yd_mover.target.set_points(points)
        yd_mover.target.set_opacity(0)

        self.play(
            MoveToTarget(yd_mover),
            FadeIn(Ey_tip),
            FadeIn(Ey_label, scale=0.5),
        )
        self.wait()

        # Move around
        # self.frame.set_height(10)
        s_group.add_updater(lambda m: m.become(get_sample_group(samples)))
        exp_graph.add_updater(lambda g: g.become(get_exp_graph()))
        self.remove(*s_group)
        self.add(s_group)

        t_tracker.add_updater(lambda m: m.set_value(1.5 * math.sin(self.time / 6)))
        self.add(t_tracker)
        self.wait(48)

        for _ in range(15):
            target_t = random.uniform(0, 2.5)
            self.play(
                t_tracker.animate.set_value(target_t),
                run_time=7
            )

        for target_t in [1.5, 0.5, 1.2, 0.2, 2.0, 1.0]:
            self.play(
                t_tracker.animate.set_value(target_t),
                run_time=5
            )
