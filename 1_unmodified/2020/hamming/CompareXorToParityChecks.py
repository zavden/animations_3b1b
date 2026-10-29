# ==============================================================================
# Scene:      CompareXorToParityChecks
# Source:     videos/_2020/hamming.py (lines 5855-5927)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CompareXorToParityChecks.py CompareXorToParityChecks -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CompareXorToParityChecks(Scene):
    def construct(self):
        # Title
        bg_rect = FullScreenRectangle()
        bg_rect.set_fill(GREY_E, 1)
        bg_rect.set_stroke(width=0)
        self.add(bg_rect)

        title = OldTexText("One algorithm, multiple perspectives")
        title.scale(1.5)
        title.to_edge(UP)
        title.add_to_back(Underline(title))
        self.add(title)

        # Options
        rects = VGroup(*[ScreenRectangle() for x in range(3)])
        rects.set_fill(BLACK, 1)
        rects.set_stroke(GREY_B, 3)
        rects.set_height(3)
        rects.arrange(RIGHT, buff=1)
        rects.shift(-rects[:2].get_center())

        labels = VGroup(
            OldTexText("Multiple parity checks"),
            OldTexText("One big xor"),
            OldTexText("Matrix product"),
        )
        for label, rect in zip(labels, rects):
            label.next_to(rect, DOWN)
        labels.set_color(BLUE)

        self.add(rects[:2])
        self.add(labels[:2])

        self.play(Write(title, run_time=2))
        self.wait(2)

        # Hardware/software labels
        hw_label = OldTexText("(nicer for hardware)")
        sw_label = OldTexText("(nicer for software)")

        for l1, l2 in zip(labels, [hw_label, sw_label]):
            l2.next_to(l1, DOWN)

        self.play(FadeIn(hw_label, 0.25 * UP))
        self.wait()
        self.play(FadeIn(sw_label, 0.25 * UP))
        self.wait()

        # Third view
        icons = Group(
            ImageMobject("ParityCheckIcon"),
            ImageMobject("XorViewIcon"),
        )
        for icon, rect in zip(icons, rects):
            icon.replace(rect)
            icon.scale(0.95)

        groups = Group(
            Group(rects[0], labels[0], icons[0], hw_label),
            Group(rects[1], labels[1], icons[1], sw_label),
            Group(rects[2], labels[2]),
        )
        groups.generate_target()
        groups.target[:2].arrange(DOWN, buff=LARGE_BUFF)
        groups.target[:2].match_height(groups.target[2])
        groups.target[2].next_to(groups.target[:2], RIGHT, LARGE_BUFF)
        groups.target.set_height(5)
        groups.target.center()
        groups.target.to_edge(DOWN, buff=1)
        groups[2].set_opacity(0)
        self.play(MoveToTarget(groups))
        self.wait()
