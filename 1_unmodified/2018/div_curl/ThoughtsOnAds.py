# ==============================================================================
# Scene:      ThoughtsOnAds
# Source:     videos/_2018/div_curl.py (lines 4260-4378)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThoughtsOnAds.py ThoughtsOnAds -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ThoughtsOnAds(Scene):
    def construct(self):
        title = Title(
            "Internet advertising",
            match_underline_width_to_text=True,
            underline_buff=SMALL_BUFF,
        )

        line = NumberLine(
            color=GREY_B,
            x_min=0,
            x_max=12,
            big_tick_numbers=[]
        )
        line.move_to(DOWN)

        arrows = VGroup(Vector(2 * LEFT), Vector(2 * RIGHT))
        arrows.arrange(RIGHT, buff=2)
        arrows.next_to(line, DOWN)

        misaligned = OldTexText("Misaligned")
        misaligned.next_to(arrows[0], DOWN)
        aligned = OldTexText("Well-aligned")
        aligned.next_to(arrows[1], DOWN)

        VGroup(arrows[0], misaligned).set_color(RED)
        VGroup(arrows[1], aligned).set_color(BLUE)

        left_text = OldTexText(
            "Any website presented \\\\",
            "as a click-maximizing \\\\ slideshow"
        )
        left_text.scale(0.8)
        left_text.next_to(line, UP, buff=MED_LARGE_BUFF)
        left_text.to_edge(LEFT)

        viewer, brand, creator = vcb = VGroup(
            *list(map(TexText, ["viewer", "brand", "creator"]))
        )
        brand.next_to(creator, LEFT, LARGE_BUFF)
        viewer.next_to(vcb[1:], UP, LARGE_BUFF)
        arrow_config = {
            "path_arc": 60 * DEGREES,
            "tip_length": 0.15,
        }
        vcb_arrows = VGroup(*[
            VGroup(
                Arrow(p1, p2, **arrow_config),
                Arrow(p2, p1, **arrow_config),
            )
            for p1, p2 in [
                (creator.get_left(), brand.get_right()),
                (brand.get_top(), viewer.get_bottom()),
                (viewer.get_bottom(), creator.get_top()),
            ]
        ])
        vcb_arrows.set_stroke(width=2)
        vcb_arrows.set_color(BLUE)
        vcb_group = VGroup(vcb, vcb_arrows)
        vcb_group.next_to(line, UP, buff=MED_LARGE_BUFF)
        vcb_group.to_edge(RIGHT)

        knob = RegularPolygon(n=3, start_angle=-90 * DEGREES)
        knob.set_height(0.25)
        knob.set_stroke(width=0)
        knob.set_fill(YELLOW, 1)
        knob.move_to(line.get_left(), DOWN)

        right_rect = Rectangle(
            width=3,
            height=0.25,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=BLUE,
            fill_opacity=0.5
        )
        right_rect.move_to(line, RIGHT)
        right_rect_label = Group(
            ImageMobject("3b1b_logo", height=1),
            OldTexText("(hopefully)").scale(0.8)
        )
        right_rect_label.arrange(DOWN, buff=SMALL_BUFF)
        # OldTexText(
        #     "Where I hope \\\\ I've been"
        # )
        right_rect_label.next_to(
            right_rect, UP, SMALL_BUFF
        )
        # right_rect_label.set_color(BLUE)

        self.add(title)
        self.play(ShowCreation(line))
        self.play(
            Write(misaligned),
            Write(aligned),
            *list(map(GrowArrow, arrows)),
            run_time=1
        )

        self.play(
            FadeIn(left_text),
            FadeIn(knob, 2 * RIGHT)
        )
        self.wait()
        self.play(
            LaggedStartMap(FadeInFromDown, vcb),
            LaggedStartMap(ShowCreation, vcb_arrows),
            ApplyMethod(
                knob.move_to, line.get_right(), DOWN,
                run_time=2
            )
        )
        self.wait(2)
        self.play(vcb_group.shift, 2 * UP)
        self.play(
            DrawBorderThenFill(right_rect),
            FadeIn(right_rect_label),
        )
        self.wait()
