# ==============================================================================
# Scene:      StateNeedForBayesRule
# Source:     videos/_2020/beta/beta1.py (lines 3562-3629)
# Category:   1 · Renders unmodified
# Includes code copied from: _2020/beta/helpers.py
#
# Run from this folder:
#     manimgl StateNeedForBayesRule.py StateNeedForBayesRule -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2020/beta/helpers.py -----

def get_beta_dist_axes(y_max=20, y_unit=2, label_y=False, **kwargs):
    config = {
        "x_min": 0,
        "x_max": 1,
        "x_axis_config": {
            "unit_size": 0.1,
            "tick_frequency": 0.1,
            "include_tip": False,
        },
        "y_min": 0,
        "y_max": y_max,
        "y_axis_config": {
            "unit_size": 1,
            "tick_frequency": y_unit,
            "include_tip": False,
        },
    }
    result = Axes(**config)
    origin = result.c2p(0, 0)
    kw = {
        "about_point": origin,
        "stretch": True,
    }
    result.x_axis.set_width(11, **kw)
    result.y_axis.set_height(6, **kw)

    x_vals = np.arange(0, 1, 0.2) + 0.2
    result.x_axis.add_numbers(
        *x_vals,
        num_decimal_places=1
    )

    if label_y:
        result.y_axis.add_numbers(
            *np.arange(y_unit, y_max, y_unit)
        )
        label = OldTexText("Probability density")
        label.scale(0.5)
        label.next_to(result.y_axis.get_top(), UR, SMALL_BUFF)
        label.next_to(result.y_axis, UP, SMALL_BUFF)
        label.align_to(result.y_axis.numbers, LEFT)
        result.add(label)
        result.y_axis_label = label

    result.to_corner(DR, LARGE_BUFF)

    return result



# ----- From _2020/beta/beta1.py -----

class StateNeedForBayesRule(TeacherStudentsScene):
    def construct(self):
        axes = get_beta_dist_axes(y_max=1, y_unit=0.25, label_y=False)
        axes.y_axis.set_height(
            2,
            about_point=axes.c2p(0, 0),
            stretch=True,
        )
        axes.set_width(5)
        graph = axes.get_graph(lambda x: x**10)
        graph.set_stroke(BLUE, 3)
        alt_graph = graph.copy()
        alt_graph.add_line_to(axes.c2p(1, 0))
        alt_graph.add_line_to(axes.c2p(0, 0))
        alt_graph.set_stroke(width=0)
        alt_graph.set_fill(BLUE_E, 1)

        plot = VGroup(axes, alt_graph, graph)

        student0, student1, student2 = self.students
        plot.next_to(student2.get_corner(UL), UP, MED_LARGE_BUFF)
        plot.shift(LEFT)

        v_lines = VGroup(
            DashedLine(axes.c2p(0.8, 0), axes.c2p(0.8, 1)),
            DashedLine(axes.c2p(1, 0), axes.c2p(1, 1)),
        )
        v_lines.set_stroke(YELLOW, 2)

        self.play(
            LaggedStart(
                ApplyMethod(student0.change, "pondering", plot),
                ApplyMethod(student1.change, "pondering", plot),
                ApplyMethod(student2.change, "raise_left_hand", plot),
            ),
            FadeIn(plot, DOWN),
            run_time=1.5
        )
        self.play(*map(ShowCreation, v_lines))
        self.play(
            self.teacher.change, "tease",
            *[
                ApplyMethod(
                    v_line.move_to,
                    axes.c2p(0.9, 0),
                    DOWN,
                )
                for v_line in v_lines
            ]
        )
        self.play_student_changes(
            "thinking", "thinking", "pondering",
            look_at=v_lines,
        )
        self.wait(2)

        self.teacher_says(
            "But first...",
            added_anims=[
                FadeOut(plot, LEFT),
                FadeOut(v_lines, LEFT),
                self.change_students(
                    "erm", "erm", "erm",
                    look_at=self.teacher.eyes,
                )
            ]
        )
        self.wait(5)
