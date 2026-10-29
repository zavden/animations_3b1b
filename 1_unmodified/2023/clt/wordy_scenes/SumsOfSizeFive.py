# ==============================================================================
# Scene:      SumsOfSizeFive
# Source:     videos/_2023/clt/wordy_scenes.py (lines 387-429)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SumsOfSizeFive.py SumsOfSizeFive -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class SumsOfSizeFive(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        stds = self.students

        self.play(
            morty.change("raise_right_hand", self.screen),
            self.change_students("pondering", "happy", "tease", look_at=self.screen)
        )
        self.wait()

        # Show sums
        def get_sum():
            values = [
                Integer(random.choice([-1, 1]), include_sign=True)
                for x in range(5)
            ]
            lhs = Tex(R"\text{Sum} = ")
            rhs = Integer(sum(v.get_value() for v in values))
            result = VGroup(lhs, *values, Tex(R" = "), rhs)
            result.arrange(RIGHT, buff=0.15)
            result.next_to(self.screen, RIGHT, buff=-0.5)
            return result

        curr_sum = get_sum()

        brace = Brace(curr_sum[1:-2], UP)
        brace_text = brace.get_text("5 values")
        brace_text.set_color(YELLOW)

        self.add(curr_sum)
        self.play(GrowFromCenter(brace), FadeIn(brace_text))
        for x in range(7):
            new_sum = get_sum()
            self.play(
                FadeOut(curr_sum[1:], lag_ratio=0.1, shift=0.2 * UP),
                FadeIn(new_sum[1:], lag_ratio=0.1, shift=0.2 * UP),
                *(pi.animate.look_at(new_sum) for pi in self.pi_creatures)
            )
            self.wait()
            curr_sum = new_sum

        self.wait()
