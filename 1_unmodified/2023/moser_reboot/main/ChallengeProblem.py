# ==============================================================================
# Scene:      ChallengeProblem
# Source:     videos/_2023/moser_reboot/main.py (lines 1289-1311)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ChallengeProblem.py ChallengeProblem -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ChallengeProblem(InteractiveScene):
    def construct(self):
        numbers = VGroup(*(
            Integer(1 + choose(n, 2) + choose(n, 4))
            for n in range(100)
        ))
        numbers.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=RIGHT)
        numbers.to_corner(UL)
        numbers.shift(DR)
        numbers.add_updater(lambda m, dt: m.shift(2 * dt * UP))

        question = VGroup(
            Text("Challenge question", font_size=72).set_fill(YELLOW),
            Text("Will there ever be another power of 2?")
        )
        question.arrange(DOWN, buff=MED_LARGE_BUFF)
        question.next_to(numbers, RIGHT, LARGE_BUFF)
        question.set_y(0)

        # Test
        self.add(numbers)
        self.play(Write(question))
        self.wait(20)
