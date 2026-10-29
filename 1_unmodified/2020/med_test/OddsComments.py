# ==============================================================================
# Scene:      OddsComments
# Source:     videos/_2020/med_test.py (lines 3755-3778)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl OddsComments.py OddsComments -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class OddsComments(Scene):
    def construct(self):
        morty = Mortimer()
        morty.to_corner(DR)
        randy = Randolph()
        randy.next_to(morty, LEFT, buff=2)

        self.play(FadeIn(morty))
        self.play(
            PiCreatureSays(
                morty,
                "The chances are\\\\1 to 1",
                run_time=1
            ),
            FadeIn(randy)
        )
        self.play(Blink(morty))
        self.play(
            PiCreatureSays(randy, "The chances are\\\\2 to 1", run_time=1),
            RemovePiCreatureBubble(morty, target_mode="happy")
        )
        self.play(Blink(morty))
        self.play(Blink(randy))
        self.wait()
