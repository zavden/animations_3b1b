# ==============================================================================
# Scene:      ExampleQuestionNoPiCreatures
# Source:     videos/_2023/clt/wordy_scenes.py (lines 942-1009)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExampleQuestionNoPiCreatures.py ExampleQuestionNoPiCreatures -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ExampleQuestionNoPiCreatures(InteractiveScene):
    def construct(self):
        # Setup
        question = [
            Text("""
                Consider rolling a die
                100 times, and adding the
                results.
            """, alignment="LEFT"),
            Text("""
                Find a range of values such
                that you're 95% sure the sum
                will fall within this range.
            """, alignment="LEFT")
        ]
        question[0].to_corner(UL)
        question[1].to_corner(UR)

        # Dice
        def get_dice():
            die_values = np.random.randint(1, 7, 100)
            dice = VGroup(*(
                DieFace(
                    value,
                    fill_color=BLUE_E,
                    stroke_width=1,
                    dot_color=WHITE
                )
                for value in die_values
            ))
            dice.arrange_in_grid()
            dice.set_height(4.5)
            dice.next_to(question[0], DOWN, buff=1)
            return dice

        dice = get_dice()

        sum_label = TexText("Sum = 100", font_size=60)
        sum_label.next_to(dice, RIGHT, buff=LARGE_BUFF)
        num = sum_label.make_number_changeable("100")
        num.add_updater(lambda m: m.set_value(sum(
            die.value for die in dice
        )))

        # Add up dice
        self.play(FadeIn(question[0], lag_ratio=0.1, run_time=1.5))
        self.play(
            VFadeIn(sum_label),
            ShowIncreasingSubsets(dice, run_time=2)
        )
        self.wait()

        # Find a range
        self.play(
            FadeIn(question[1], lag_ratio=0.1, run_time=1.5),
        )
        self.wait()
        self.play(
            FlashUnder(question[1][r"95% sure"], color=TEAL),
            question[1][r"95% sure"].animate.set_color(TEAL)
        )

        # More sums
        for x in range(5):
            old_dice = dice.copy()
            dice.set_submobjects(list(get_dice()))
            self.play(ShowIncreasingSubsets(dice, run_time=2), FadeOut(old_dice, run_time=0.5))
            self.wait()
