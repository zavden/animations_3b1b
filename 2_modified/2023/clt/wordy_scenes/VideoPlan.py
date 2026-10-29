# ==============================================================================
# Scene:      VideoPlan
# Source:     videos/_2023/clt/wordy_scenes.py (lines 236-316)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl VideoPlan.py VideoPlan -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - ConvolutionThumbnail (private thumbnail) replaced with a placeholder
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/ConvolutionThumbnail.png  (placeholder; script: _lib/assets/generated/2023/gauss_int/make_gauss_int_placeholders.py)
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class VideoPlan(InteractiveScene):
    def construct(self):
        # Rectangles
        full_rect = FullScreenRectangle()
        screen_rect = ScreenRectangle()
        screen_rect.set_height(5.5)
        screen_rect.to_edge(DOWN)
        screen_rect.set_fill(BLACK, 1)
        screen_rect.set_stroke(width=2)
        rects = VGroup(full_rect, screen_rect)
        self.add(*rects)

        # CLT title
        big_name = Text("The Central\nLimit Theorem", font_size=120)
        name = Text("The Central Limit Theorem", font_size=60)
        name.to_edge(UP)
        subtitle = Text("from the basics")
        subtitle.set_color(GREY_A)
        subtitle.next_to(name, DOWN)

        rects.set_opacity(0)
        self.play(FadeIn(big_name, lag_ratio=0.1))
        self.wait()
        self.play(
            TransformMatchingStrings(big_name, name, run_time=1),
            full_rect.animate.set_opacity(1)
        )
        self.play(FadeIn(subtitle, 0.5 * DOWN))
        self.wait(2)

        # Next part
        group1 = VGroup(name, subtitle, screen_rect)
        group1.target = group1.generate_target()
        group1.target.set_width(FRAME_WIDTH * 0.5 - 1)
        group1.target.move_to(FRAME_WIDTH * LEFT * 0.25)

        screen2 = group1.target[2].copy()
        screen2.set_opacity(1)
        name2 = Text("Diving deeper")
        name2.scale(group1.target[0][0].get_height() / name2[0].get_height())
        name2.move_to(group1.target[0])
        group2 = VGroup(name2, screen2)
        group2.move_to(FRAME_WIDTH * RIGHT * 0.25)

        self.play(MoveToTarget(group1))
        self.play(
            FadeTransform(screen_rect.copy(), screen2),
            FadeTransform(name.copy(), name2),
        )
        self.wait()

        # Also follow-on to convolutions
        group1.target = group1.generate_target()
        group1.target[2].scale(0.75, about_edge=UP)
        group1.target[1].scale(0)
        group1.target.arrange(DOWN, buff=SMALL_BUFF)
        group1.target.to_corner(UL)

        conv_rect = group1.target[2].copy()
        conv_rect.set_stroke(WHITE, 3, 1)
        conv_image = ImageMobject("ConvolutionThumbnail")
        conv_image.replace(conv_rect)
        conv_name = Text("Convolutions")
        conv_name.replace(group1.target[0], dim_to_match=1)
        conv_group = Group(conv_name, conv_rect, conv_image)
        conv_group.to_corner(DL)

        arrows = VGroup(
            Arrow(group1.target[2].get_right(), screen2.get_left() + UP),
            Arrow(conv_rect.get_right(), screen2.get_left() + DOWN),
        )
        arrows.set_color(BLUE)

        self.play(LaggedStart(
            MoveToTarget(group1),
            FadeIn(conv_group, DOWN),
            name2.animate.next_to(screen2, UP),
            lag_ratio=0.25
        ))
        self.play(*map(GrowArrow, arrows))
        self.wait()
