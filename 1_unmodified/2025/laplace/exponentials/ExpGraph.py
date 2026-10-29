# ==============================================================================
# Scene:      ExpGraph
# Source:     videos/_2025/laplace/exponentials.py (lines 234-310)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExpGraph.py ExpGraph -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ExpGraph(InteractiveScene):
    def construct(self):
        # Set up graph
        axes = Axes((-1, 4), (0, 20), width=10, height=6)
        axes.to_edge(RIGHT)
        x_axis_label = Tex("t")
        x_axis_label.next_to(axes.x_axis.get_right(), UL, MED_SMALL_BUFF)
        axes.add(x_axis_label)

        graph = axes.get_graph(np.exp)
        graph.set_stroke(BLUE, 3)

        title = Tex(R"\frac{d}{dt} e^t = e^t", t2c={"t": GREY_B}, font_size=60)
        title.to_edge(UP)
        title.match_x(axes.c2p(1.5, 0))

        self.add(axes)
        self.add(graph)
        self.add(title)

        # Add height tracker
        t_tracker = ValueTracker(1)
        get_t = t_tracker.get_value
        v_line = always_redraw(
            lambda: axes.get_v_line_to_graph(get_t(), graph, line_func=Line).set_stroke(RED, 3)
        )
        height_label = Tex(R"e^t", font_size=42)
        height_label.always.next_to(v_line, RIGHT, SMALL_BUFF)
        height_label_height = height_label.get_height()
        height_label.add_updater(lambda m: m.set_height(
            min(height_label_height, 0.7 * v_line.get_height())
        ))

        self.play(
            ShowCreation(v_line, suspend_mobject_updating=True),
            FadeIn(height_label, UP, suspend_mobject_updating=True),
        )
        self.wait()

        # Add tangent line
        tangent_line = always_redraw(
            lambda: axes.get_tangent_line(get_t(), graph, length=10).set_stroke(BLUE_A, 1)
        )
        unit_size = axes.x_axis.get_unit_size()
        unit_line = Line(axes.c2p(0, 0), axes.c2p(1, 0))
        unit_line.add_updater(lambda m: m.move_to(v_line.get_end(), LEFT))
        unit_line.set_stroke(WHITE, 2)
        unit_label = Integer(1, font_size=24)
        unit_label.add_updater(lambda m: m.next_to(unit_line.pfp(0.6), UP, 0.5 * SMALL_BUFF))
        tan_v_line = always_redraw(
            lambda: v_line.copy().shift(v_line.get_vector() + unit_size * RIGHT)
        )

        deriv_label = Tex(R"\frac{d}{dt} e^t = e^t", font_size=42)
        deriv_label[R"\frac{d}{dt}"].scale(0.75, about_edge=RIGHT)
        deriv_label_height = deriv_label.get_height()
        deriv_label.add_updater(lambda m: m.set_height(
            min(deriv_label_height, 0.8 * v_line.get_height())
        ))
        deriv_label.always.next_to(tan_v_line, RIGHT, SMALL_BUFF)

        self.play(ShowCreation(tangent_line, suspend_mobject_updating=True))
        self.play(
            VFadeIn(unit_line),
            VFadeIn(unit_label),
            VFadeIn(tan_v_line, suspend_mobject_updating=True),
            TransformFromCopy(title, deriv_label),
        )
        self.play(
            ReplacementTransform(v_line.copy().clear_updaters(), tan_v_line, path_arc=45 * DEG),
            FadeTransform(height_label.copy(), deriv_label["e^t"][1], path_arc=45 * DEG, remover=True),
        )
        self.wait()

        # Move it around
        for t in [2.35, 0, 1, 2]:
            self.play(t_tracker.animate.set_value(t), run_time=5)
