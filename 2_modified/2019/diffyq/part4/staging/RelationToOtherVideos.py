# ==============================================================================
# Scene:      RelationToOtherVideos
# Source:     videos/_2019/diffyq/part4/staging.py (lines 35-134)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl RelationToOtherVideos.py RelationToOtherVideos -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use CairoImageMobject to keep Cairo's default height and pixel reading, without changing other years.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: keep Cairo's height (2) and the pixel_array reading through a local adapter.
from cairo_compat import CairoImageMobject as ImageMobject

class RelationToOtherVideos(Scene):
    CONFIG = {
        "camera_config": {
            "background_color": GREY_D,
        },
    }

    def construct(self):
        # Show three videos
        videos = self.get_video_thumbnails()
        brace = Brace(videos, UP)
        text = OldTexText("Heat equation")
        text.scale(2)
        text.next_to(brace, UP)

        self.play(
            LaggedStartMap(
                FadeInFrom, videos,
                lambda m: (m, LEFT),
                lag_ratio=0.4,
                run_time=2,
            ),
            GrowFromCenter(brace),
            FadeInFromDown(text),
        )
        self.wait()
        group = Group(text, brace, videos)

        # Show Fourier thinking
        fourier = ImageMobject("Joseph Fourier")
        fourier.set_height(4)
        fourier.to_edge(RIGHT)
        group.generate_target()
        group.target.to_edge(DOWN)
        fourier.align_to(group.target[0], DOWN)
        bubble = ThoughtBubble(
            direction=RIGHT,
            width=3,
            height=2,
            fill_opacity=0.5,
            stroke_color=WHITE,
        )
        bubble[-1].shift(0.25 * DOWN + 0.5 * LEFT)
        bubble[:-1].rotate(20 * DEGREES)
        for mob in bubble[:-1]:
            mob.rotate(-20 * DEGREES)
        bubble.move_to(
            fourier.get_center(), RIGHT
        )
        bubble.shift(LEFT)
        bubble.to_edge(UP, buff=SMALL_BUFF)

        self.play(
            MoveToTarget(group),
            FadeIn(fourier, LEFT)
        )
        self.play(Write(bubble, run_time=1))
        self.wait()

        # Discount first two
        first_two = videos[:2]
        first_two.generate_target()
        first_two.target.scale(0.5)
        first_two.target.to_corner(DL)
        new_brace = Brace(first_two.target, UP)

        self.play(
            # fourier.scale, 0.8,
            fourier.match_x, new_brace,
            fourier.to_edge, UP,
            MoveToTarget(first_two),
            Transform(brace, new_brace),
            text.scale, 0.7,
            text.next_to, new_brace, UP,
            FadeOut(bubble, LEFT),
        )
        self.play(
            videos[2].scale, 1.7,
            videos[2].to_corner, UR,
        )
        self.wait()

    #
    def get_video_thumbnails(self):
        thumbnails = Group(
            ImageMobject("diffyq_part2_thumbnail"),
            ImageMobject("diffyq_part3_thumbnail"),
            ImageMobject("diffyq_part4_thumbnail"),
        )
        for thumbnail in thumbnails:
            thumbnail.set_height(4)
            thumbnail.add(SurroundingRectangle(
                thumbnail,
                color=WHITE,
                stroke_width=2,
                buff=0
            ))
        thumbnails.arrange(RIGHT, buff=LARGE_BUFF)
        thumbnails.set_width(FRAME_WIDTH - 1)
        return thumbnails
