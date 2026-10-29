# ==============================================================================
# Scene:      DivergenceAtSlowFastPoint
# Source:     videos/_2018/div_curl.py (lines 1658-1713)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DivergenceAtSlowFastPoint.py DivergenceAtSlowFastPoint -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DivergenceAtSlowFastPoint(Scene):
    CONFIG = {
        "vector_field_config": {
            "length_func": lambda norm: 0.1 + 0.4 * norm / 4.0,
            "min_magnitude": 0,
            "max_magnitude": 3,
        },
        "stream_lines_config": {
            "start_points_generator_config": {
                "delta_x": 0.125,
                "delta_y": 0.125,
            },
            "virtual_time": 1,
            "min_magnitude": 0,
            "max_magnitude": 3,
        },
    }

    def construct(self):
        def func(point):
            return 3 * sigmoid(point[0]) * RIGHT
        vector_field = self.vector_field = VectorField(
            func, **self.vector_field_config
        )

        circle = Circle(color=WHITE)
        slow_words = OldTexText("Slow flow in")
        fast_words = OldTexText("Fast flow out")
        words = VGroup(slow_words, fast_words)
        for word, vect in zip(words, [LEFT, RIGHT]):
            word.add_background_rectangle()
            word.next_to(circle, vect)

        div_tex = OldTex(
            "\\text{div}\\,\\textbf{F}(x, y) > 0"
        )
        div_tex.add_background_rectangle()
        div_tex.next_to(circle, UP)

        self.add(vector_field)
        self.add_foreground_mobjects(circle, div_tex)
        self.begin_flow()
        self.wait(2)
        for word in words:
            self.add_foreground_mobjects(word)
            self.play(Write(word))
        self.wait(8)

    def begin_flow(self):
        stream_lines = StreamLines(
            self.vector_field.func,
            **self.stream_lines_config
        )
        stream_line_animation = AnimatedStreamLines(stream_lines)
        stream_line_animation.update(3)
        self.add(stream_line_animation)
