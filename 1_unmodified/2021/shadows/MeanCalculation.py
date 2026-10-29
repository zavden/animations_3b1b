# ==============================================================================
# Scene:      MeanCalculation
# Source:     videos/_2021/shadows.py (lines 785-820)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MeanCalculation.py MeanCalculation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MeanCalculation(Scene):
    def construct(self):
        values = [1.55, 1.33, 1.46, 1.34, 1.50, 1.26, 1.42, 1.54, 1.51]
        nums = VGroup(*(
            DecimalNumber(x)
            for x in values
        ))
        nums.arrange(DOWN, aligned_edge=LEFT)
        nums.to_corner(UR, buff=LARGE_BUFF).shift(0.5 * LEFT)

        self.add(nums)

        mean_label = Text("Mean", font_size=36)
        mean_label.set_color(GREEN)
        mean_label.set_backstroke()
        mean_arrow = Vector(0.25 * UR)
        mean_arrow.match_color(mean_label)
        mean_arrow.next_to(mean_label, UR, SMALL_BUFF)
        mean_label.add(mean_arrow)

        for n in range(len(nums)):
            brace = Brace(nums[:n + 1], LEFT, buff=SMALL_BUFF)
            mean = DecimalNumber(np.mean(values[:n + 1]))
            mean.next_to(brace, LEFT)
            mean.match_color(mean_label)
            VGroup(brace, mean).set_backstroke()
            mean_label.next_to(mean, DL, SMALL_BUFF)

            self.add(brace, mean, mean_label)
            self.wait(0.5)
            self.remove(brace, mean)
        self.add(brace, mean)
        self.wait()

        # Embed
        self.embed()
