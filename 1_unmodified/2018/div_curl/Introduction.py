# ==============================================================================
# Scene:      Introduction
# Source:     videos/_2018/div_curl.py (lines 189-251)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Introduction.py Introduction -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Introduction(MovingCameraScene):
    CONFIG = {
        "stream_lines_config": {
            "start_points_generator_config": {
                "delta_x": 1.0 / 8,
                "delta_y": 1.0 / 8,
                "y_min": -8.5,
                "y_max": 8.5,
            }
        },
        "vector_field_config": {},
        "virtual_time": 3,
    }

    def construct(self):
        # Divergence
        def div_func(p):
            return p / 3
        div_vector_field = VectorField(
            div_func, **self.vector_field_config
        )
        stream_lines = StreamLines(
            div_func, **self.stream_lines_config
        )
        stream_lines.shuffle()
        div_title = self.get_title("Divergence")

        self.add(div_vector_field)
        self.play(
            LaggedStartMap(ShowPassingFlash, stream_lines),
            FadeIn(div_title[0]),
            *list(map(GrowFromCenter, div_title[1]))
        )

        # Curl
        def curl_func(p):
            return rotate_vector(p / 3, 90 * DEGREES)

        curl_vector_field = VectorField(
            curl_func, **self.vector_field_config
        )
        stream_lines = StreamLines(
            curl_func, **self.stream_lines_config
        )
        stream_lines.shuffle()
        curl_title = self.get_title("Curl")

        self.play(
            ReplacementTransform(div_vector_field, curl_vector_field),
            ReplacementTransform(
                div_title, curl_title,
                path_arc=90 * DEGREES
            ),
        )
        self.play(ShowPassingFlash(stream_lines, run_time=3))
        self.wait()

    def get_title(self, word):
        title = OldTexText(word)
        title.scale(2)
        title.to_edge(UP)
        title.add_background_rectangle()
        return title
