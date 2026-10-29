# ==============================================================================
# Scene:      TangentTaylorSeries
# Source:     videos/_2019/clacks/solution1.py (lines 2795-2860)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TangentTaylorSeries.py TangentTaylorSeries -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TangentTaylorSeries(TeacherStudentsScene):
    def construct(self):
        series = OldTex(
            "\\tan", "(", "\\theta", ")", "=", "\\theta", "+",
            "\\frac{1}{3}", "\\theta", "^3", "+",
            "\\frac{2}{15}", "\\theta", "^5", "+", "\\cdots",
            tex_to_color_map={"\\theta": YELLOW},
        )
        series.move_to(2 * UP)
        series.move_to(self.hold_up_spot, DOWN)
        series_error = series[7:]
        series_error_rect = SurroundingRectangle(series_error)

        example = OldTex(
            "\\tan", "\\left(", "\\frac{1}{100}", "\\right)",
            "=", "\\frac{1}{100}", "+",
            "\\frac{1}{3}", "\\left(",
            "\\frac{1}{1{,}000{,}000}",
            "\\right)", "+",
            "\\frac{2}{15}", "\\left(",
            "\\frac{1}{10{,}000{,}000{,}000}",
            "\\right)", "+", "\\cdots",
        )
        example.set_color_by_tex("\\frac{1}{1", BLUE)
        example.set_width(FRAME_WIDTH - 1)
        example.next_to(self.students, UP, buff=2)
        example.shift_onto_screen()
        error = example[7:]
        error_rect = SurroundingRectangle(error)
        error_rect.set_color(RED)
        error_decimal = DecimalNumber(
            np.tan(0.01) - 0.01,
            num_decimal_places=15,
        )
        error_decimal.next_to(error_rect, DOWN)
        approx = OldTex("\\approx")
        approx.next_to(error_decimal, LEFT)
        error_decimal.add(approx)
        error_decimal.match_color(error_rect)

        self.play(
            FadeInFromDown(series),
            self.teacher.change, "raise_right_hand",
        )
        self.play(
            ShowCreation(series_error_rect),
            self.change_students(*3 * ["pondering"])
        )
        self.play(FadeOut(series_error_rect))
        self.play(
            series.center, series.to_edge, UP,
        )
        self.look_at(series)
        self.play(
            TransformFromCopy(series[:8], example[:8]),
            TransformFromCopy(series[8], example[9]),
            TransformFromCopy(series[10:12], example[11:13]),
            TransformFromCopy(series[12], example[14]),
            TransformFromCopy(series[14:], example[16:]),
            *map(GrowFromCenter, [example[i] for i in (8, 10, 13, 15)])
        )
        self.play_student_changes("happy", "confused", "sad")
        self.play(ShowCreation(error_rect))
        self.play(ShowIncreasingSubsets(error_decimal))
        self.play_all_student_changes("hooray")
        self.wait(3)
