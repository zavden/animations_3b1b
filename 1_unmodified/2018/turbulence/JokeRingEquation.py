# ==============================================================================
# Scene:      JokeRingEquation
# Source:     videos/_2018/turbulence.py (lines 479-517)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl JokeRingEquation.py JokeRingEquation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class JokeRingEquation(Scene):
    def construct(self):
        items = VGroup(
            OldTexText("Container with a lip"),
            OldTexText("Fill with smoke (or fog)"),
            OldTexText("Hold awkwardly"),
        )
        line = Line(LEFT, RIGHT).set_width(items.get_width() + 1)
        items.add(line)
        items.add(OldTexText("Vortex ring"))
        items.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        line.shift(LEFT)
        plus = OldTex("+")
        plus.next_to(line.get_left(), UR, SMALL_BUFF)
        line.add(plus)
        items.to_edge(RIGHT)

        point = 3.8 * LEFT + 0.2 * UP
        arrow1 = Arrow(
            items[0].get_left(), point + 0.8 * UP + 0.3 * RIGHT,
            path_arc=90 * DEGREES,
        )
        arrow1.pointwise_become_partial(arrow1, 0, 0.99)

        arrow2 = Arrow(
            items[1].get_left(), point,
        )
        arrows = VGroup(arrow1, arrow2)

        for i in 0, 1:
            self.play(
                FadeInFromDown(items[i]),
                ShowCreation(arrows[i])
            )
            self.wait()
        self.play(LaggedStartMap(FadeIn, items[2:]))
        self.wait()
        self.play(FadeOut(arrows))
        self.wait()
