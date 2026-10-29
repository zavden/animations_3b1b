# ==============================================================================
# Scene:      ThinkingAboutRediscovery
# Source:     videos/_2024/holograms/supplements.py (lines 1314-1340)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThinkingAboutRediscovery.py ThinkingAboutRediscovery -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ThinkingAboutRediscovery(InteractiveScene):
    def construct(self):
        # Test
        randy = Randolph()
        randy.body.insert_n_curves(100)
        randy.to_corner(DL)
        bubble = ThoughtBubble(filler_shape=(5, 2))
        bubble.pin_to(randy)
        bubble = bubble[0]
        bubble.set_fill(opacity=0)

        rect = FullScreenRectangle().set_fill(BLACK, 1)
        rect.append_points([rect.get_points()[-1], *bubble[-1].get_points()])
        self.add(rect, randy)

        self.play(
            randy.change('pondering'),
            Write(bubble, stroke_color=WHITE, lag_ratio=0.2)
        )
        self.play(Blink(randy))
        self.wait(2)
        self.play(randy.change('thinking', bubble.get_top()))
        self.play(Blink(randy))
        self.play(randy.change('tease', bubble.get_top()))
        for _ in range(2):
            self.play(Blink(randy))
            self.wait(2)
