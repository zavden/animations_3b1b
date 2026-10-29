# ==============================================================================
# Scene:      PiGesture1
# Source:     videos/_2020/ctracing.py (lines 336-349)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PiGesture1.py PiGesture1 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PiGesture1(Scene):
    def construct(self):
        randy = Randolph(mode="raise_right_hand", height=2)
        bubble = randy.get_bubble(
            bubble_type=SpeechBubble,
            height=2, width=3,
        )
        bubble.write("This one's\\\\great")
        bubble.content.scale(0.8)
        bubble.content.set_color(BLACK)
        bubble.set_color(BLACK)
        bubble.set_fill(opacity=0)
        randy.set_stroke(BLACK, 5, background=True)
        self.add(randy, bubble, bubble.content)
