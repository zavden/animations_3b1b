# ==============================================================================
# Scene:      VectorFieldSolution
# Source:     videos/_2024/linalg/eigenlecture.py (lines 284-318)
# Category:   2 · Renders with modifications
# Includes code copied from: _2021/matrix_exp.py
#
# Run from this folder:
#     manimgl VectorFieldSolution.py VectorFieldSolution -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - get_vector_field_and_stream_lines used the global variable `axes` (not defined here, a bug of Grant's); the `coordinate_system` argument is used
# ==============================================================================

from manim_imports_ext import *


# ----- From _2021/matrix_exp.py -----

def get_vector_field_and_stream_lines(
    func, coordinate_system,
    magnitude_range=(0.5, 4),
    vector_opacity=0.75,
    vector_thickness=0.03,
    color_by_magnitude=False,
    line_color=GREY_A,
    line_width=3,
    line_opacity=0.75,
    sample_freq=5,
    n_samples_per_line=10,
    arc_len=3,
    time_width=0.3,
):
    vector_field = VectorField(
        func, coordinate_system,
        magnitude_range=magnitude_range,
        vector_config={
            "fill_opacity": vector_opacity,
            "thickness": vector_thickness,
        }
    )
    stream_lines = StreamLines(
        func, coordinate_system,
        step_multiple=1.0 / sample_freq,
        n_samples_per_line=n_samples_per_line,
        arc_len=arc_len,
        magnitude_range=magnitude_range,
        color_by_magnitude=color_by_magnitude,
        stroke_color=line_color,
        stroke_width=line_width,
        stroke_opacity=line_opacity,
    )
    animated_lines = AnimatedStreamLines(
        stream_lines,
        line_anim_config={
            "time_width": time_width,
        },
    )

    return vector_field, animated_lines



# ----- From _2024/linalg/eigenlecture.py -----

def get_vector_field_and_stream_lines(
    func, coordinate_system,
    # Vector config
    vector_stroke_width=5,
    vector_opacity=0.5,
    density=4,
    # Streamline config
    sample_freq=5,
    n_samples_per_line=10,
    solution_time=1,
    arc_len=3,  # Does nothing
    time_width=0.5,
    line_color=WHITE,
    line_width=3,
    line_opacity=1.0,
):
    # Vector field
    # CHANGE: `axes` was not defined inside the function (in the original it relied on a global); the `coordinate_system` argument is used
    vector_field = VectorField(
        func, coordinate_system,
        density=density,
        stroke_width=vector_stroke_width,
        stroke_opacity=vector_opacity,
    )

    # Streamlines
    # CHANGE: same as above, `axes` -> `coordinate_system`
    stream_lines = StreamLines(
        func, coordinate_system,
        density=sample_freq,
        n_samples_per_line=n_samples_per_line,
        solution_time=solution_time,
        magnitude_range=vector_field.magnitude_range,
        color_by_magnitude=False,
        stroke_color=line_color,
        stroke_width=line_width,
        stroke_opacity=line_opacity,
    )
    animated_lines = AnimatedStreamLines(
        stream_lines,
        line_anim_config=dict(time_width=time_width),
        rate_multiple=0.25,
    )

    return vector_field, animated_lines


class VectorFieldSolution(InteractiveScene):
    def construct(self):
        # Add axes
        mat = np.array([[1, 2], [3, 1]])
        # mat = np.array([[2, 0], [0, -1]])
        axes = NumberPlane((-4, 4), (-2, 2), faded_line_ratio=1)
        axes.set_height(FRAME_HEIGHT)
        axes.background_lines.set_stroke(BLUE, 1)
        axes.faded_lines.set_stroke(BLUE, 0.5, 0.5)
        axes.add_coordinate_labels(font_size=36)

        def func(v):
            return 0.5 * np.dot(v, mat.T)

        self.add(axes)

        # Calculate eigen vectors
        eigenvalues, eigenvectors = np.linalg.eig(mat)
        eigenlines = VGroup(
            Line(-v, v).set_length(10)
            for v in eigenvectors.T
        )
        eigenlines.set_stroke(TEAL, 5)

        # Show the flow
        config = dict()
        # config = dict(step_multiple=0.5, vector_stroke_width=8)
        vector_field, animated_lines = get_vector_field_and_stream_lines(func, axes, **config)

        self.add(vector_field, animated_lines)
        vector_field.set_stroke(opacity=1)
        self.play(vector_field.animate.set_stroke(opacity=0.5))
        self.wait(10)
        self.play(ShowCreation(eigenlines))
        self.wait(10)
