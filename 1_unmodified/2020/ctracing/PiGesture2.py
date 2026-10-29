# ==============================================================================
# Scene:      PiGesture2
# Source:     videos/_2020/ctracing.py (lines 352-369)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PiGesture2.py PiGesture2 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PiGesture2(Scene):
    def construct(self):
        randy = Randolph(mode="raise_left_hand", height=2)
        randy.look(UL)
        # randy.flip()
        randy.set_color(GREY_BROWN)
        bubble = randy.get_bubble(
            bubble_type=SpeechBubble,
            height=2, width=3,
            direction=LEFT,
        )
        bubble.write("So is\\\\this one")
        bubble.content.scale(0.8)
        bubble.content.set_color(BLACK)
        bubble.set_color(BLACK)
        bubble.set_fill(opacity=0)
        randy.set_stroke(BLACK, 5, background=True)
        self.add(randy, bubble, bubble.content)
