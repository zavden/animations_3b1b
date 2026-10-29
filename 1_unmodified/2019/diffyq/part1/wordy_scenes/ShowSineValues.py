# ==============================================================================
# Scene:      ShowSineValues
# Source:     videos/_2019/diffyq/part1/wordy_scenes.py (lines 383-422)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowSineValues.py ShowSineValues -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowSineValues(Scene):
    def construct(self):
        angle_tracker = ValueTracker(60 * DEGREES)
        get_angle = angle_tracker.get_value
        formula = always_redraw(
            lambda: self.get_sine_formula(get_angle())
        )
        self.add(formula)

        self.play(
            angle_tracker.set_value, 0,
            run_time=3,
        )
        self.wait()
        self.play(
            angle_tracker.set_value, 90 * DEGREES,
            run_time=3,
        )
        self.wait()

    def get_sine_formula(self, angle):
        sin, lp, rp = OldTex(
            "\\sin", "(", ") = "
        )
        input_part = Integer(
            angle / DEGREES,
            unit="^\\circ",
        )
        input_part.set_color(YELLOW)
        output_part = DecimalNumber(
            np.sin(input_part.get_value() * DEGREES),
            num_decimal_places=3,
        )
        result = VGroup(
            sin, lp, input_part, rp, output_part
        )
        result.arrange(RIGHT, buff=SMALL_BUFF)
        sin.scale(1.1, about_edge=DOWN)
        lp.align_to(rp, UP)
        return result
