# ==============================================================================
# Scene:      SchizophrenicNumbers
# Source:     videos/_2017/efvgt.py (lines 1705-1769)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SchizophrenicNumbers.py SchizophrenicNumbers -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Eyes.blink_anim does not exist in this pi creature module: animate Eyes.blink with ApplyMethod
# ==============================================================================

from manim_imports_ext import *

ADDER_COLOR = GREEN


MULTIPLIER_COLOR = YELLOW


class SchizophrenicNumbers(Scene):
    def construct(self):
        v_line = DashedLine(
            FRAME_Y_RADIUS*UP,
            FRAME_Y_RADIUS*DOWN
        )
        left_title = OldTexText("Additive group")
        left_title.shift(FRAME_X_RADIUS*LEFT/2)
        right_title = OldTexText("Multiplicative group")
        right_title.shift(FRAME_X_RADIUS*RIGHT/2)
        VGroup(left_title, right_title).to_edge(UP)
        self.add(v_line, left_title, right_title)

        numbers = VGroup(
            Randolph(mode = "happy").scale(0.2),
            OldTex("3").shift(UP+LEFT),
            OldTex("5.83").shift(UP+RIGHT),
            OldTex("\\sqrt{2}").shift(DOWN+LEFT),
            OldTex("2-i").shift(DOWN+RIGHT),
        )
        for number in numbers:
            number.set_color(ADDER_COLOR)
            number.scale(1.5)            
            if isinstance(number, PiCreature):
                continue
            number.eyes = Eyes(number[0], height = 0.1)
            number.add(number.eyes)
        numbers[3].eyes.next_to(numbers[3][1], UP, buff = 0)
        numbers.shift(FRAME_X_RADIUS*LEFT/2)

        self.play(FadeIn(numbers))
        self.blink_numbers(numbers)
        self.wait()
        self.add(numbers.copy())
        for number in numbers:
            number.generate_target()
            number.target.shift(FRAME_X_RADIUS*RIGHT)
            number.target.eyes.save_state()
            number.target.set_color(MULTIPLIER_COLOR)
            number.target.eyes.restore()
        self.play(*[
            MoveToTarget(
                number, 
                rate_func = squish_rate_func(
                    smooth, alpha, alpha+0.5
                ),
                run_time = 2,
            )
            for number, alpha in zip(numbers, np.linspace(0, 0.5, len(numbers)))
        ])
        self.wait()
        self.blink_numbers(numbers)
        self.wait()

    def blink_numbers(self, numbers):
        self.play(*[
            # CHANGE: Eyes.blink_anim does not exist in this pi creature module: animate Eyes.blink with ApplyMethod
            ApplyMethod(
                num.eyes.blink,
                rate_func = squish_rate_func(
                    there_and_back, alpha, alpha+0.2
                )
            )
            for num, alpha in zip(
                numbers[1:], 0.8*np.random.random(len(numbers))
            )
        ])
