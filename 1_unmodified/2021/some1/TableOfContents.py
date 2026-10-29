# ==============================================================================
# Scene:      TableOfContents
# Source:     videos/_2021/some1.py (lines 19-51)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TableOfContents.py TableOfContents -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TableOfContents(Scene):
    def construct(self):
        # plane = NumberPlane()
        # self.add(plane, FullScreenFadeRectangle(opacity=0.8))

        items = VGroup(
            Text("Summer of Math Exposition"),
            Text("The Universal Advice"),
            Text("How to structure math explanations"),
            Text("Thoughts on animation software"),
            Text("The 3b1b Podcast/Second channel"),
        )
        items.arrange(DOWN, buff=LARGE_BUFF, aligned_edge=LEFT)
        items.to_edge(LEFT, buff=0.5)

        self.add(items)

        for i in range(len(items)):
            for item in items:
                item.generate_target()
                if item is items[i]:
                    height = 0.55
                    opacity = 1.0
                else:
                    height = 0.3
                    opacity = 0.25
                item.target.scale(
                    height / item[0].get_height(),
                    about_edge=LEFT
                )
                item.target.set_opacity(opacity)
            self.play(*map(MoveToTarget, items))
            self.wait()
