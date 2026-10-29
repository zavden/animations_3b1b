# ==============================================================================
# Scene:      MentionPRFNuance
# Source:     videos/_2018/uncertainty.py (lines 2071-2174)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MentionPRFNuance.py MentionPRFNuance -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class MentionPRFNuance(TeacherStudentsScene):
    def construct(self):
        title = OldTexText(
            "Speed of light", "$\\gg$", "Speed of a plane"
        )
        title.to_edge(UP)
        self.add(title)

        axes = self.axes = Axes(
            x_min = 0, x_max = 10,
            y_min = 0, y_max = 2,
        )
        axes.next_to(title, DOWN, buff = MED_LARGE_BUFF)
        frequency_label = OldTexText("Frequency")
        frequency_label.scale(0.7)
        frequency_label.next_to(axes.x_axis.get_right(), UP)
        axes.add(frequency_label)
        self.add(axes)

        pulse_x, shift_x = 4, 6
        pulse_graph = self.get_spike_graph(pulse_x)
        shift_graph = self.get_spike_graph(shift_x)
        shift_graph.set_stroke(YELLOW, 2)
        peak_points = VGroup(pulse_graph.peak_point, shift_graph.peak_point)
        self.add(pulse_graph)

        brace = Brace(peak_points, UP, buff = SMALL_BUFF)
        displayed_doppler_shift = OldTexText("How I'm showing the \\\\", "Doppler shift")
        actual_doppler_shift = OldTexText("Actual\\\\", "Doppler shift")
        doppler_shift_words = VGroup(displayed_doppler_shift, actual_doppler_shift)
        doppler_shift_words.set_color(YELLOW)
        doppler_shift_words.scale(0.75)
        displayed_doppler_shift.next_to(brace, UP, buff = SMALL_BUFF)
        actual_doppler_shift.move_to(pulse_graph.peak_point)
        actual_doppler_shift.align_to(displayed_doppler_shift)

        self.play(
            Animation(pulse_graph),
            self.teacher.change, "raise_right_hand", 
            run_time = 1
        )
        self.play(
            ShowCreation(shift_graph),
            FadeIn(brace),
            Write(displayed_doppler_shift, run_time = 1),
            self.change_students(*3*["sassy"]),
        )
        self.play(
            UpdateFromAlphaFunc(
                shift_graph, 
                lambda g, a : Transform(
                    g, self.get_spike_graph(
                        interpolate(shift_x, pulse_x+0.01, a),
                    ).match_style(shift_graph)
                ).update(1),
            ),
            UpdateFromFunc(
                brace,
                lambda b : b.match_width(
                    peak_points, stretch = True
                ).next_to(peak_points, UP, SMALL_BUFF)
            ),
            Transform(
                displayed_doppler_shift, actual_doppler_shift,
                rate_func = squish_rate_func(smooth, 0.3, 0.6)
            ),
            run_time = 3
        )
        self.wait(2)

        everything = VGroup(
            title,
            axes, pulse_graph, shift_graph,
            brace, displayed_doppler_shift
        )
        rect = SurroundingRectangle(everything, color = WHITE)
        everything.add(rect)

        self.teacher_says(
            "I'll ignore certain \\\\ nuances for now.",
            target_mode = "shruggie",
            added_anims = [
                everything.scale, 0.4,
                everything.to_corner, UP+LEFT,
                UpdateFromAlphaFunc(
                    rect, lambda m, a : m.set_stroke(width = 2*a)
                )
            ],
        )
        self.play_student_changes(*3*["hesitant"])
        self.wait(2)




    def get_spike_graph(self, x, color = RED, **kwargs):
        graph = self.axes.get_graph(
            lambda t : np.exp(-10*(t-x)**2)*np.cos(10*(t-x)),
            color = color,
            **kwargs
        )
        graph.peak_point = VectorizedPoint(self.axes.input_to_graph_point(x, graph))
        graph.add(graph.peak_point)
        return graph
