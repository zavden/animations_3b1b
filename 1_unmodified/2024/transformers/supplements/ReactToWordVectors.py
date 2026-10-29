# ==============================================================================
# Scene:      ReactToWordVectors
# Source:     videos/_2024/transformers/supplements.py (lines 649-683)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReactToWordVectors.py ReactToWordVectors -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ReactToWordVectors(InteractiveScene):
    def construct(self):
        # Test
        morty = Mortimer().flip()
        randy = Randolph().flip()
        morty, randy = pis = VGroup(morty, randy)
        pis.arrange(RIGHT, buff=2.0)
        pis.to_edge(DOWN)
        randy.make_eye_contact(morty)

        self.add(pis)
        self.play(
            PiCreatureSays(
                morty, "This is how search\nworks you know!",
                target_mode="hooray",
                content_introduction_class=FadeIn,
                content_introduction_kwargs=dict(lag_ratio=0.1),
            ),
            randy.change("guilty"),
        )
        self.play(Blink(randy))
        self.wait()
        dots = Text(".....", font_size=120)
        dots[:1].set_opacity(0)
        dots[-1:].set_opacity(0)
        self.play(
            morty.debubble(),
            PiCreatureBubbleIntroduction(
                randy, dots, target_mode="confused",
                bubble_type=ThoughtBubble,
            ),
            morty.change("tease", look_at=6 * LEFT),
        )
        self.play(Blink(morty))
        self.wait()
