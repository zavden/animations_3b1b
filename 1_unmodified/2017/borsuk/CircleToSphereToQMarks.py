# ==============================================================================
# Scene:      CircleToSphereToQMarks
# Source:     videos/_2017/borsuk.py (lines 2504-2536)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CircleToSphereToQMarks.py CircleToSphereToQMarks -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CircleToSphereToQMarks(Scene):
    def construct(self):
        pi_groups = VGroup()
        modes = ["happy", "pondering", "pleading"]
        shapes = [
            Circle(color = BLUE, radius = 0.5), 
            VectorizedPoint(), 
            OldTex("???")
        ]
        for d, mode, shape in zip(it.count(2), modes, shapes):
            randy = Randolph(mode = mode)
            randy.scale(0.7)
            bubble = randy.get_bubble(
                height = 3, width = 4,
                direction = LEFT
            )
            bubble.pin_to(randy)
            bubble.position_mobject_inside(shape)
            title = OldTexText("%dD"%d)
            title.next_to(randy, UP)
            arrow = Arrow(LEFT, RIGHT)
            arrow.next_to(randy.get_corner(UP+RIGHT))
            pi_groups.add(VGroup(
                randy, bubble, shape, title, arrow
            ))

        pi_groups[-1].remove(pi_groups[-1][-1])
        pi_groups.arrange(buff = -1)
        for mob in pi_groups:
            self.play(FadeIn(mob))
        self.wait(2)
        self.play(pi_groups[-1][0].change_mode, "thinking")
        self.wait(2)
