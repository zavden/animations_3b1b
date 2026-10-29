# ==============================================================================
# Scene:      PiGesture3
# Source:     videos/_2020/ctracing.py (lines 372-387)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PiGesture3.py PiGesture3 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PiGesture3(Scene):
    def construct(self):
        randy = Randolph(mode="hooray", height=2)
        randy.flip()
        bubble = randy.get_bubble(
            bubble_type=SpeechBubble,
            height=2, width=3,
            direction=LEFT,
        )
        bubble.write("And this\\\\one")
        bubble.content.scale(0.8)
        bubble.content.set_color(BLACK)
        bubble.set_color(BLACK)
        bubble.set_fill(opacity=0)
        randy.set_stroke(BLACK, 5, background=True)
        self.add(randy, bubble, bubble.content)
