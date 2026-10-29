# ==============================================================================
# Scene:      VariousMusicalNotes
# Source:     videos/_2018/uncertainty.py (lines 961-1081)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl VariousMusicalNotes.py VariousMusicalNotes -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - 5x fewer samples (0.004 vs 0.001 over +-7 units, still 80 samples per period of the sin): the graph was rebuilt every frame and took 3.5 s per frame (timeout at 900 s)
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class VariousMusicalNotes(Scene):
    def construct(self):
        freq = 20
        # x-coordinate of this point represents log(a)
        # where the bell curve component of the signal
        # is exp(-a*(x**2))
        graph_width_tracker = ExponentialValueTracker(1)
        def get_graph():
            a = graph_width_tracker.get_value()
            return FunctionGraph(
                lambda x : np.exp(-a*x**2)*np.sin(freq*x)-0.5,
                # CHANGE: 5x fewer samples (0.004 vs 0.001 over +-7 units, still 80 samples per period of the sin): the graph was rebuilt every frame and took 3.5 s per frame (timeout at 900 s)
                step_size = 0.004,
            )
        graph = get_graph()
        def graph_update(graph):
            graph.set_points(get_graph().get_points())
        graph_update_anim = UpdateFromFunc(graph, graph_update)
        def change_width_anim(width, **kwargs):
            a = 2.0/(width**2)
            return AnimationGroup(
                ApplyMethod(graph_width_tracker.set_value, a),
                graph_update_anim,
                **kwargs
            )
        change_width_anim(FRAME_X_RADIUS).update(1)
        graph_update_anim.update(0)

        phrases = [
            OldTexText(*words.split(" "))
            for words in [
                "Very clear frequency",
                "Less clear frequency",
                "Extremely unclear frequency",
            ]
        ]


        #Show graphs and phrases
        widths = [FRAME_X_RADIUS, 1, 0.2]
        for width, phrase in zip(widths, phrases):
            brace = Brace(Line(LEFT, RIGHT), UP)
            brace.stretch(width, 0)
            brace.next_to(graph.get_center(), UP, buff = 1.2)
            phrase.next_to(brace, UP)

            if width is widths[0]:
                self.play(ShowCreation(graph, rate_func=linear)),
                self.play(
                    GrowFromCenter(brace),
                    Write(phrase, run_time = 1)
                )
            else:
                self.play(
                    change_width_anim(width),
                    ReplacementTransform(
                        VGroup(last_phrase, last_brace),
                        VGroup(phrase, brace),
                        rate_func = squish_rate_func(smooth, 0.5, 1),
                    ),
                    run_time = 2
                )
            self.wait()
            # self.play(*map(FadeOut, [graph, brace, phrase]))
            last_phrase = phrase
            last_brace = brace

        #Talk about correlations
        short_signal_words = OldTexText(
            "Short", "signal", "correlates",
            "with", "wide range", "of frequencies"
        )
        long_signal_words = OldTexText(
            "Only", "wide", "signals", "correlate",
            "with a", "short range", "of frequencies"
        )
        phrases = VGroup(short_signal_words, long_signal_words)
        for phrase in phrases:
            phrase.scale(0.8)
            phrase.set_color_by_tex_to_color_map({
                "short" : RED,
                "long" : GREEN,
                "wide" : GREEN,
            }, case_sensitive = False)
        phrases.arrange(DOWN)
        phrases.to_edge(UP)

        long_graph = FunctionGraph(
            lambda x : 0.5*np.sin(freq*x),
            x_min = -FRAME_WIDTH,
            x_max = FRAME_WIDTH,
            n_components = 0.001
        )
        long_graph.set_color(BLUE)
        long_graph.next_to(graph, UP, MED_LARGE_BUFF)

        self.play(
            ShowCreation(long_graph),
            *list(map(FadeOut, [last_brace, last_phrase]))
        )
        self.play(
            Write(short_signal_words),
            change_width_anim(widths[2])
        )
        self.play(
            long_graph.stretch, 0.35, 0,
            long_graph.set_color, GREEN,
            run_time = 5,
            rate_func = wiggle
        )
        self.wait()
        self.play(
            Write(long_signal_words),
            change_width_anim(widths[0]),
        )
        self.play(
            long_graph.stretch, 0.95, 0,
            long_graph.set_color, average_color(GREEN, BLUE),
            run_time = 4,
            rate_func = wiggle
        )
        self.wait()
