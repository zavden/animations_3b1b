# ==============================================================================
# Scene:      AverageDiceValues
# Source:     videos/_2023/clt/wordy_scenes.py (lines 1012-1046)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AverageDiceValues.py AverageDiceValues -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AverageDiceValues(InteractiveScene):
    def construct(self):
        # Test
        avg_label = TexText("Average value = 0.00")
        avg_label.make_number_changeable("0.00")
        avg_label.next_to(ORIGIN, RIGHT)
        avg_label.set_y(FRAME_HEIGHT / 4)
        self.add(avg_label)

        self.old_dice = VGroup()
        for _ in range(20):
            self.show_sample(avg_label, 100)
            self.wait(2)

    def show_sample(self, avg_label, n_dice, added_anims=[]):
        dice = VGroup(*(
            DieFace(random.randint(1, 6), fill_color=BLUE_E, dot_color=WHITE, stroke_width=1)
            for x in range(n_dice)
        ))
        dice.arrange_in_grid()
        dice.set_height(3.5)
        dice.next_to(avg_label, LEFT, buff=LARGE_BUFF)
        dice.to_edge(UP, buff=MED_SMALL_BUFF)

        self.play(LaggedStart(
            FadeOut(self.old_dice, run_time=0.5),
            ShowIncreasingSubsets(dice, run_time=1, int_func=np.ceil),
            UpdateFromFunc(avg_label[-1], lambda m: m.set_value(
                np.mean([die.value for die in dice])
            )),
            *added_anims
        ))
        avg_label[-1].set_color(YELLOW)

        self.old_dice = dice
