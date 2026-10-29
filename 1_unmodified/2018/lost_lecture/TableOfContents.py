# ==============================================================================
# Scene:      TableOfContents
# Source:     videos/_2018/lost_lecture.py (lines 1125-1160)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TableOfContents.py TableOfContents -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TableOfContents(Scene):
    def construct(self):
        items = VGroup(
            OldTexText("How the ellipse will arise"),
            OldTexText("Kepler's 2nd law"),
            OldTexText("The shape of velocities"),
        )
        items.arrange(
            DOWN, buff=LARGE_BUFF, aligned_edge=LEFT
        )
        items.to_edge(LEFT, buff=1.5)
        for item in items:
            item.add(Dot().next_to(item, LEFT))
            item.generate_target()
            item.target.set_fill(GREY, opacity=0.5)

        title = Title("The plan")
        scale_factor = 1.2

        self.add(title)
        self.play(LaggedStartMap(
            FadeIn, items,
            run_time=1,
            lag_ratio=0.7,
        ))
        self.wait()
        for item in items:
            other_items = VGroup(*[m for m in items if m is not item])
            new_item = item.copy()
            new_item.scale(scale_factor, about_edge=LEFT)
            new_item.set_fill(WHITE, 1)
            self.play(
                Transform(item, new_item),
                *list(map(MoveToTarget, other_items))
            )
            self.wait()
