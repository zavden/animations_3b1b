# ==============================================================================
# Scene:      ExampleQuestion
# Source:     videos/_2023/clt/wordy_scenes.py (lines 852-939)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExampleQuestion.py ExampleQuestion -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ExampleQuestion(TeacherStudentsScene):
    def construct(self):
        # Setup
        question = Text("""
            Consider rolling a fair die 100 times,
            and adding the results.

            Find a range of values such that you're
            95% sure the sum will fall within
            this range.
        """, alignment="LEFT")
        question.to_corner(UL)

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
        dice.set_height(3.0)
        dice.next_to(question, RIGHT, buff=1)
        dice.to_edge(UP, buff=1.0)

        sum_label = TexText("Sum = 100")
        sum_label.next_to(dice, UP)
        num = sum_label.make_number_changeable("100")
        n_tracker = ValueTracker(0)
        num.add_updater(lambda m: m.set_value(sum(die_values[:int(n_tracker.get_value())])))

        # Ask for an example
        morty = self.teacher
        stds = self.students

        self.play(
            stds[2].says("Can we see a\nconcrete example?"),
            morty.change("happy")
        )
        self.wait()

        # Add up dice
        die_highlights = dice.copy()
        die_highlights.set_stroke(YELLOW, 1)

        part1 = re.findall(r"Consider .*\n.* results.", question.get_string())[0]
        self.play(
            morty.change("raise_right_hand", question),
            self.change_students("pondering", "pondering", "tease", look_at=question),
            FadeIn(question[part1], lag_ratio=0.1, run_time=1.5),
            FadeOut(stds[2].bubble),
            FadeOut(stds[2].bubble.content),
        )
        self.play(
            FlashUnder(question["fair die"]),
            question["fair die"].animate.set_color(YELLOW),
            FadeIn(dice, lag_ratio=0.03, run_time=2),
        )
        self.play(
            *(pi.animate.look_at(dice) for pi in [morty, *stds])
        )
        n_tracker.set_value(0)
        self.play(
            VFadeIn(sum_label),
            n_tracker.animate.set_value(100).set_anim_args(run_time=2),
            ShowIncreasingSubsets(die_highlights, run_time=2)
        )
        self.play(FadeOut(die_highlights))
        self.wait()

        # Find a range
        part2 = re.findall(r"Find .*\n.*\n.* range.", question.get_string())[0]
        self.play(
            morty.change("tease", question),
            self.change_students("erm", "hesitant", "pondering", look_at=question),
            FadeIn(question[part2], lag_ratio=0.1, run_time=1.5),
        )
        self.wait()
        self.play(
            FlashUnder(question[r"95% sure"], color=TEAL),
            question[r"95% sure"].animate.set_color(TEAL)
        )
        self.wait(2)
        self.play(self.change_students("confused", "erm", "tease", look_at=question))
        self.wait(3)
