# ==============================================================================
# Scene:      YouAsAMathematician
# Source:     videos/_2025/laplace/main_supplements.py (lines 212-251)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl YouAsAMathematician.py YouAsAMathematician -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class YouAsAMathematician(InteractiveScene):
    def construct(self):
        # Test
        randy = Randolph(height=2.5)
        randy.flip()
        randy.to_edge(DOWN, buff=MED_SMALL_BUFF)

        you = Text("You")
        you.next_to(randy, UR, LARGE_BUFF)
        mathematician = Text("(Mathematician)")
        mathematician.next_to(you, DOWN, aligned_edge=LEFT)
        arrow = Arrow(you.get_corner(DL), randy.body.get_corner(UR) + 0.7 * LEFT, buff=0.1, thickness=5)

        self.play(
            randy.change('pondering', 3 * UL),
            GrowArrow(arrow),
            Write(you)
        )
        self.play(FadeIn(mathematician, 0.25 * DOWN))
        self.play(Blink(randy))
        self.wait()

        # Reference machine
        label = VGroup(you, mathematician)
        self.play(
            randy.change("raise_left_hand", 3 * UR),
            label.animate.next_to(randy, RIGHT).set_opacity(0.5),
            FadeOut(arrow, scale=0.5, shift=DL),
        )
        self.play(Blink(randy))
        self.wait(2)
        self.play(
            randy.change("hesitant", 3 * UL)
        )
        for _ in range(2):
            self.play(Blink(randy))
            self.wait(2)
        self.play(randy.change("pondering", 3 * UL))
        for _ in range(2):
            self.play(Blink(randy))
