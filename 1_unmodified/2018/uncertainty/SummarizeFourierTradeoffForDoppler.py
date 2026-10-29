# ==============================================================================
# Scene:      SummarizeFourierTradeoffForDoppler
# Source:     videos/_2018/uncertainty.py (lines 2773-2831)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SummarizeFourierTradeoffForDoppler.py SummarizeFourierTradeoffForDoppler -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class SummarizeFourierTradeoffForDoppler(Scene):
    def construct(self):
        time_axes = Axes(
            x_min = 0, x_max = 12,
            y_min = -0.5, y_max = 1,
        )
        time_axes.center().to_edge(UP, buff = LARGE_BUFF)
        frequency_axes = time_axes.copy()
        frequency_axes.next_to(time_axes, DOWN, buff = 2)
        time_label = OldTexText("Time")
        frequency_label = OldTexText("Frequency")
        for label, axes in (time_label, time_axes), (frequency_label, frequency_axes):
            label.next_to(axes.get_right(), UP, SMALL_BUFF)
            axes.add(label)
        frequency_label.shift_onto_screen()
        title = OldTexText("Fourier Trade-off")
        title.next_to(time_axes, DOWN)
        self.add(title)


        #Position determines log of scale value for exponentials
        a_mob = VectorizedPoint()
        x_values = [3, 5, 6, 7, 8]
        v_values = [5, 5.5, 5.75, 6.5, 7]
        def get_top_graphs():
            a = np.exp(a_mob.get_center()[0])
            graphs = VGroup(*[
                time_axes.get_graph(lambda t : np.exp(-5*a*(t-x)**2))
                for x in x_values
            ])
            graphs.set_color(WHITE)
            graphs.color_using_background_image("blue_yellow_gradient")
            return graphs
        def get_bottom_graphs():
            a = np.exp(a_mob.get_center()[0])
            graphs = VGroup(*[
                frequency_axes.get_graph(lambda t : np.exp(-(5./a)*(t-v)**2))
                for v in v_values
            ])
            graphs.set_color(RED)
            return graphs

        top_graphs = get_top_graphs()
        bottom_graphs = get_bottom_graphs()
        update_top_graphs = Mobject.add_updater(
            top_graphs, 
            lambda g : Transform(g, get_top_graphs()).update(1)
        )
        update_bottom_graphs = Mobject.add_updater(
            bottom_graphs, 
            lambda g : Transform(g, get_bottom_graphs()).update(1)
        )

        self.add(time_axes, frequency_axes)
        self.add(update_top_graphs, update_bottom_graphs)

        shift_vect = 2*RIGHT
        for s in 1, -2, 1:
            self.play(a_mob.shift, s*shift_vect, run_time = 3)
