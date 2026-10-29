# ==============================================================================
# Scene:      HyperbolicFlowEvaluation
# Source:     videos/_2021/matrix_exp.py (lines 6120-6121)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl HyperbolicFlowEvaluation.py HyperbolicFlowEvaluation -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - VectorField/StreamLines are imported from legacy_arrow_vector_field (arrow API with func(x, y) and step_multiple, from before Sept 2024).
#   - Matrix/DecimalMatrix: `element_to_mobject_config` no longer exists: Matrix uses `element_config`; DecimalMatrix uses `num_decimal_places=` and `decimal_config=`.
# ==============================================================================

from manim_imports_ext import *
# CHANGE: VectorField/StreamLines with manimgl's arrow API from before Sept 2024 (see _lib/legacy_arrow_vector_field.py)
from legacy_arrow_vector_field import VectorField, StreamLines

def get_matrix_exponential(matrix, height=1.5, scalar_tex="t", **matrix_config):
    elem = matrix[0][0]
    if isinstance(elem, str):
        mat_class = Matrix
    elif isinstance(elem, int) or isinstance(elem, np.int64):
        mat_class = IntegerMatrix
    else:
        mat_class = DecimalMatrix

    matrix = mat_class(matrix, **matrix_config)
    base = OldTex("e")
    base.set_height(0.4 * height)
    matrix.set_height(0.6 * height)
    matrix.move_to(base.get_corner(UR), DL)
    result = VGroup(base, matrix)
    if scalar_tex:
        scalar = OldTex(scalar_tex)
        scalar.set_height(0.7 * base.get_height())
        scalar.next_to(matrix, RIGHT, buff=SMALL_BUFF, aligned_edge=DOWN)
        result.add(scalar)
    return result


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


def mat_exp(matrix, N=100):
    curr = np.identity(len(matrix))
    curr_sum = curr
    for n in range(1, N):
        curr = np.dot(curr, matrix) / n
        curr_sum += curr
    return curr_sum


class ExponentialPhaseFlow(Scene):
    CONFIG = {
        "field_config": {
            "color_by_magnitude": False,
            "magnitude_range": (0.5, 5),
            "arc_len": 5,
        },
        "plane_config": {
            "x_range": [-4, 4],
            "y_range": [-2, 2],
            "height": 8,
            "width": 16,
        },
        "matrix": [
            [1, 0],
            [0, 1],
        ],
        "label_height": 3,
        "run_time": 30,
        "slow_factor": 0.25,
    }

    def construct(self):
        mr = np.array(self.field_config["magnitude_range"])
        self.field_config["magnitude_range"] = self.slow_factor * mr
        plane = NumberPlane(**self.plane_config)
        plane.add_coordinate_labels()

        vector_field, animated_lines = get_vector_field_and_stream_lines(
            self.func, plane,
            **self.field_config,
        )

        box = Square()
        box.replace(Line(plane.c2p(-1, -1), plane.c2p(1, 1)), stretch=True)
        box.set_stroke(GREY_A, 1)
        box.set_fill(BLUE_E, 0.8)
        move_points_along_vector_field(box, self.func, plane)

        basis_vectors = VGroup(
            Vector(RIGHT, fill_color=GREEN),
            Vector(UP, fill_color=RED),
        )
        basis_vectors[0].add_updater(lambda m: m.put_start_and_end_on(
            plane.get_origin(),
            box.pfp(7 / 8)
        ))
        basis_vectors[1].add_updater(lambda m: m.put_start_and_end_on(
            plane.get_origin(),
            box.pfp(1 / 8)
        ))

        self.add(plane)
        self.add(vector_field)
        self.add(animated_lines)
        self.add(box)
        self.add(*basis_vectors)
        self.wait(self.run_time)

    def func(self, x, y):
        return self.slow_factor * np.dot([x, y], np.transpose(self.matrix))

    def get_label(self):
        exponential = get_matrix_exponential(self.matrix)
        changing_t = DecimalNumber(0, color=YELLOW)
        changing_t.match_height(exponential[2])
        changing_t.move_to(exponential[2], DL)
        exponential.replace_submobject(2, changing_t)

        equals = OldTex("=")
        rhs = DecimalMatrix(
            np.zeros((2, 2)),
            # CHANGE: element_to_mobject_config no longer exists in Matrix/DecimalMatrix (see element_config / decimal_config)
            num_decimal_places=3,
            h_buff=1.8,
        )
        rhs.match_height(exponential)

        equation = VGroup(
            exponential,
            equals,
            rhs,
        )
        equation.arrange(RIGHT)
        equation.to_corner(UL)


class ExponentialEvaluationWithTime(Scene):
    flow_scene_class = ExponentialPhaseFlow

    def construct(self):
        flow_scene_attrs = merge_dicts_recursively(
            ExponentialPhaseFlow.CONFIG,
            self.flow_scene_class.CONFIG,
        )
        matrix = np.array(flow_scene_attrs["matrix"])
        slow_factor = flow_scene_attrs["slow_factor"]

        def get_t():
            return slow_factor * self.time

        exponential = get_matrix_exponential(matrix)
        dot = OldTex("\\cdot")
        dot.move_to(exponential[2], LEFT)
        changing_t = DecimalNumber(0)
        changing_t.match_height(exponential[2])
        changing_t.next_to(dot, RIGHT, SMALL_BUFF)
        changing_t.align_to(exponential[1], DOWN)
        changing_t.add_updater(lambda m: m.set_value(get_t()).set_color(YELLOW))
        lhs = VGroup(*exponential[:2], dot, changing_t)

        equals = OldTex("=")
        rhs = DecimalMatrix(
            np.zeros((2, 2)),
            # CHANGE: element_to_mobject_config no longer exists in Matrix/DecimalMatrix (see element_config / decimal_config)
            num_decimal_places=2,
            element_alignment_corner=ORIGIN,
            h_buff=2.0,
        )
        for mob in rhs.get_entries():
            mob.edge_to_fix = ORIGIN

        rhs.match_height(lhs)

        def update_rhs(rhs):
            result = mat_exp(matrix * get_t())
            for mob, value in zip(rhs.get_entries(), result.flatten()):
                mob.set_value(value)
            return rhs

        rhs.add_updater(update_rhs)

        equation = VGroup(lhs, equals, rhs)
        equation.arrange(RIGHT)
        equation.center()

        self.add(equation)
        self.wait(flow_scene_attrs["run_time"])
        self.embed()


class HyperbolicPhaseFlow(ExponentialPhaseFlow):
    CONFIG = {
        "field_config": {
            "sample_freq": 8,
        },
        "matrix": [
            [1, 0],
            [0, -1],
        ]
    }


class HyperbolicFlowEvaluation(ExponentialEvaluationWithTime):
    flow_scene_class = HyperbolicPhaseFlow
