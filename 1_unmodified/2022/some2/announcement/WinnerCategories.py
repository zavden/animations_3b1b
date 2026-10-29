# ==============================================================================
# Scene:      WinnerCategories
# Source:     videos/_2022/some2/announcement.py (lines 77-105)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WinnerCategories.py WinnerCategories -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WinnerCategories(InteractiveScene):
    def construct(self):
        # Text
        title = Text("In choosing winners, we will select:", font_size=60)
        title.to_edge(UP)
        kw = dict(t2c={"non-video": BLUE, "video": RED, "collaboration": YELLOW})
        cats = VGroup(
            Text("At least one video entry", **kw),
            Text("At least one non-video entry", **kw),
            Text("At least one collaboration", **kw),
        )
        cats[1].select_part("non-video").set_color(BLUE)
        cats.arrange(DOWN, buff=0.75, aligned_edge=LEFT)
        cats.next_to(title, DOWN, LARGE_BUFF)
        details = Text("(See initial substack post for details)", font_size=36)
        details.next_to(cats, DOWN, LARGE_BUFF)
        details.set_fill(GREY_B)

        self.add(title)
        self.play(Write(cats[0], run_time=1))
        self.wait(0.5)
        self.play(TransformMatchingStrings(cats[0].copy(), cats[1]))
        self.wait(0.5)
        self.play(TransformMatchingStrings(cats[1].copy(), cats[2]))
        self.play(FlashAround(cats[2], run_time=2))
        self.wait()

        self.play(FadeIn(details, 0.5 * DOWN))
        self.wait()
