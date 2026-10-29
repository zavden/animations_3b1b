# ==============================================================================
# Scene:      ButTheyreNotEquallyLikely
# Source:     videos/_2022/wordle/scenes.py (lines 1767-1793)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ButTheyreNotEquallyLikely.py ButTheyreNotEquallyLikely -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ButTheyreNotEquallyLikely(Scene):
    def construct(self):
        randy = Randolph()
        morty = Mortimer()
        pis = VGroup(randy, morty)
        pis.arrange(RIGHT, buff=2)
        pis.to_edge(DOWN)
        randy.make_eye_contact(morty)

        self.play(
            PiCreatureSays(
                randy, OldTexText("But they're \\emph{not}\\\\equally likely!"),
                target_mode="angry",
            ),
            morty.change("guilty", randy.eyes),
        )
        self.play(Blink(randy))
        self.wait()
        self.play(
            PiCreatureSays(
                morty, OldTexText("To warm up, let's\\\\assume they are."),
                target_mode="speaking",
            ),
            RemovePiCreatureBubble(randy),
        )
        self.play(Blink(morty))
        self.wait()
