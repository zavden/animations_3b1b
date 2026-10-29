# ==============================================================================
# Scene:      PhraseDirichletsTheoremFor10
# Source:     videos/_2019/spirals.py (lines 3839-3913)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PhraseDirichletsTheoremFor10.py PhraseDirichletsTheoremFor10 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PhraseDirichletsTheoremFor10(TeacherStudentsScene):
    def construct(self):
        expression = OldTex(
            "\\lim_{x \\to \\infty}",
            "\\left(",
            "{\\text{\\# of primes $p$ where $p \\le x$} \\text{ and $p \\equiv 1$ mod 10}",
            "\\over",
            "\\text{\\# of primes $p$ where $p \\le x$}}",
            "\\right)",
            "=",
            "\\frac{1}{4}",
        )
        lim, lp, num, over, denom, rp, eq, fourth = expression
        expression.shift(UP)

        denom.save_state()
        denom.move_to(self.hold_up_spot, DOWN)
        denom.shift_onto_screen()

        num[len(denom):].set_color(YELLOW)

        x_example = VGroup(
            OldTexText("Think, for example, $x = $"),
            Integer(int(1e6)),
        )
        x_example.arrange(RIGHT)
        x_example.scale(1.5)
        x_example.to_edge(UP)

        #
        teacher = self.teacher
        students = self.students
        self.play(
            FadeInFromDown(denom),
            teacher.change, "raise_right_hand",
            self.change_students(*["pondering"] * 3),
        )
        self.wait()
        self.play(FadeInFromDown(x_example))
        self.wait()
        self.play(
            Restore(denom),
            teacher.change, "thinking",
        )
        self.play(
            TransformFromCopy(denom, num[:len(denom)]),
            Write(over),
        )
        self.play(
            Write(num[len(denom):]),
            students[0].change, "confused",
            students[2].change, "erm",
        )
        self.wait(2)
        self.play(
            Write(lp),
            Write(rp),
            Write(eq),
        )
        self.play(FadeIn(fourth, LEFT))
        self.play(FadeIn(lim, RIGHT))
        self.play(
            ChangeDecimalToValue(
                x_example[1], int(1e7),
                run_time=8,
                rate_func=linear,
            ),
            VFadeOut(x_example, run_time=8),
            self.change_students(*["thinking"] * 3),
            Blink(
                teacher,
                run_time=4,
                rate_func=squish_rate_func(there_and_back, 0.65, 0.7)
            ),
        )
