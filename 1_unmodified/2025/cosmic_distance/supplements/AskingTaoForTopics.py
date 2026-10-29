# ==============================================================================
# Scene:      AskingTaoForTopics
# Source:     videos/_2025/cosmic_distance/supplements.py (lines 85-114)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskingTaoForTopics.py AskingTaoForTopics -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskingTaoForTopics(InteractiveScene):
    def construct(self):
        # Test
        morty = Mortimer()
        morty.to_edge(DOWN).set_x(4)
        morty.body.insert_n_curves(100)

        tau = TauCreature("plain")
        tau[4].set_fill(border_width=1)
        tau.set_height(3)
        tau.to_edge(DOWN)
        tau.set_x(-4)

        self.add(morty)
        self.add(tau)

        self.play(morty.change("raise_right_hand"))
        self.play(Transform(tau, TauCreature("pondering").move_to(tau)))
        self.wait()
        self.play(Blink(morty))
        self.play(tau[:4].animate.stretch(0, 1, about_edge=DOWN), rate_func=squish_rate_func(there_and_back, 0.4, 0.6))
        self.wait()

        self.play(
            Transform(tau, TauCreature("hooray").move_to(tau)),
            FadeIn(tau.get_bubble("How about the\nCosmic Distance Ladder?", bubble_type=SpeechBubble), lag_ratio=0.1, run_time=2),
            morty.change("tease", look_at=ORIGIN),
        )
        self.play(Blink(morty))
        self.play(tau[:4].animate.stretch(0, 1, about_edge=DOWN), rate_func=squish_rate_func(there_and_back, 0.4, 0.6))
