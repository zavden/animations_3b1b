# ==============================================================================
# Scene:      AssumingNormality
# Source:     videos/_2023/clt/wordy_scenes.py (lines 1200-1243)
# Category:   1 · Renders unmodified
# Includes code copied from: _2023/clt/main.py
#
# Run from this folder:
#     manimgl AssumingNormality.py AssumingNormality -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *


# ----- From _2023/clt/main.py -----

def gauss_func(x, mu, sigma):
    pre_factor = 1 / (sigma * math.sqrt(2 * PI))
    return pre_factor * np.exp(-0.5 * ((x - mu) / sigma)**2)



# ----- From _2023/clt/wordy_scenes.py -----

class AssumingNormality(InteractiveScene):
    def construct(self):
        # Setup
        randy = Randolph().to_corner(DL)
        morty = Mortimer().to_corner(DR)

        randy.shift(2 * RIGHT)
        thought = ThoughtBubble(height=2, width=3, direction=RIGHT)
        thought.pin_to(randy)
        curve = FunctionGraph(lambda x: 5 * gauss_func(x, 0, 1), x_range=(-3, 3, 0.1))
        curve.set_stroke(YELLOW, 3)
        curve.scale(0.35)
        curve.move_to(thought.get_bubble_center() + 0.15 * UL)

        self.add(FullScreenRectangle().set_fill(GREY_E, 0.5))
        self.add(randy, morty)
        self.add(thought, curve)

        # Words
        self.play(
            randy.says(
                TexText(
                    R"""
                    It's a $3\sigma$ event, \\
                    so $p < 0.003$
                    """,
                    t2c={R"\sigma": RED}
                ),
                look_at=morty.eyes,
                mode="tease"
            ),
            morty.change("hesitant", randy.eyes)
        )
        self.play(Blink(morty))
        self.wait()
        self.play(Blink(randy))
        self.wait()
        self.play(
            morty.says("Is it though?", look_at=randy.eyes, mode="sassy"),
            randy.change("guilty", morty.eyes)
        )
        self.wait()
        self.play(Blink(randy))
        self.wait()
