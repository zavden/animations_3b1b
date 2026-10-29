# ==============================================================================
# Scene:      CompareCountries
# Source:     videos/_2020/covid.py (lines 1211-1264)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CompareCountries.py CompareCountries -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CompareCountries(Scene):
    def construct(self):
        # Introduce
        sk_flag = ImageMobject(os.path.join("flags", "kr"))
        au_flag = ImageMobject(os.path.join("flags", "au"))
        flags = Group(sk_flag, au_flag)
        flags.set_height(3)
        flags.arrange(RIGHT, buff=LARGE_BUFF)
        flags.next_to(ORIGIN, UP)

        labels = VGroup()
        case_numbers = [6593, 64]
        for flag, cn in zip(flags, case_numbers):
            label = VGroup(Integer(cn), OldTexText("cases"))
            label.arrange(RIGHT, buff=MED_SMALL_BUFF)
            label[1].align_to(label[0][-1], DOWN)
            label.scale(1.5)
            label.next_to(flag, DOWN, MED_LARGE_BUFF)
            label[0].set_value(0)
            labels.add(label)

        self.play(LaggedStartMap(FadeInFromDown, flags, lag_ratio=0.25))
        self.play(
            ChangeDecimalToValue(labels[0][0], case_numbers[0]),
            ChangeDecimalToValue(labels[1][0], case_numbers[1]),
            UpdateFromAlphaFunc(
                labels,
                lambda m, a: m.set_opacity(a),
            )
        )
        self.wait()

        # Compare
        arrow = Arrow(
            labels[1][0].get_bottom(),
            labels[0][0].get_bottom(),
            path_arc=-90 * DEGREES,
        )
        arrow_label = OldTexText("100x better")
        arrow_label.set_color(YELLOW)
        arrow_label.next_to(arrow, DOWN)

        alt_arrow_label = OldTexText("1 month behind")
        alt_arrow_label.set_color(RED)
        alt_arrow_label.next_to(arrow, DOWN)

        self.play(ShowCreation(arrow))
        self.play(FadeIn(arrow_label, 0.5 * UP))
        self.wait(2)
        self.play(
            FadeIn(alt_arrow_label, 0.5 * UP),
            FadeOut(arrow_label, 0.5 * DOWN),
        )
        self.wait(2)
