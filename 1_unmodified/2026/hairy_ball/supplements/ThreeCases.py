# ==============================================================================
# Scene:      ThreeCases
# Source:     videos/_2026/hairy_ball/supplements.py (lines 236-264)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThreeCases.py ThreeCases -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ThreeCases(InteractiveScene):
    def construct(self):
        # Test
        titles = VGroup(
            VGroup(Text("2 null points"), Text("Obvious")),
            VGroup(Text("1 null point"), Text("Clever")),
            VGroup(Text("0 null points"), Text("Very clever")),
        )
        for title in titles:
            title[0].set_color(GREY_B)
            title[1].scale(1.25)
            title.arrange(DOWN)
        titles.arrange(RIGHT, buff=1.5, aligned_edge=UP)
        titles.to_edge(UP)

        vc_cross = Cross(titles[2][1])

        why_not = Text("Why not?")
        why_not.next_to(title)
        why_not.set_color(YELLOW)
        why_not.next_to(titles[2], DOWN, aligned_edge=RIGHT)

        for title in titles:
            self.add(title[0])
        for title in titles:
            self.play(FadeIn(title[1], lag_ratio=0.1))
        self.wait()
        self.play(ShowCreation(vc_cross))
        self.play(Write(why_not))
