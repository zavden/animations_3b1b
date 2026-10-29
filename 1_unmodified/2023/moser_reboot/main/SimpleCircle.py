# ==============================================================================
# Scene:      SimpleCircle
# Source:     videos/_2023/moser_reboot/main.py (lines 288-305)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleCircle.py SimpleCircle -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimpleCircle(InteractiveScene):
    def construct(self):
        # Test
        circle = Circle()
        circle.set_height(7.75)
        circle.set_stroke(RED, width=3)
        circle.move_to(2.6 * RIGHT)
        radians = np.arange(1, 7)
        dots = VGroup(*(
            Dot(circle.pfp(radians[i] / TAU))
            for i in [0, 2, 4, 1, 3, 5]
        ))

        self.add(circle)
        for dot in dots:
            self.wait()
            self.add(dot)
        self.wait()
