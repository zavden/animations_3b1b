# ==============================================================================
# Scene:      NextVideo
# Source:     videos/_2023/gauss_int/supplements.py (lines 1034-1143)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl NextVideo.py NextVideo -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Private thumbnails from Grant's Dropbox (absolute paths /Users/grant/...) replaced with placeholders
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/gauss_int/EquationThumbnail.png  (placeholder; script: _lib/assets/generated/2023/gauss_int/make_gauss_int_placeholders.py)
#   - _lib/assets/raster_images/gauss_int/Thumbnail.png  (placeholder; script: _lib/assets/generated/2023/gauss_int/make_gauss_int_placeholders.py)
#   - _lib/assets/raster_images/gauss_int/ProofSummary.jpg  (placeholder; script: _lib/assets/generated/2023/gauss_int/make_gauss_int_placeholders.py)
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class NextVideo(InteractiveScene):
    def construct(self):
        self.add(FullScreenRectangle().set_fill(GREY_E, 0.75))

        # Thumbnails
        images = Group(
            # CHANGE: the private thumbnails from Grant's Dropbox were replaced by placeholders in _lib/assets/raster_images/gauss_int/
            ImageMobject("gauss_int/EquationThumbnail.png"),
            ImageMobject("gauss_int/Thumbnail.png"),
            ImageMobject("gauss_int/ProofSummary.jpg"),
        )
        images.set_height(3)
        titles = VGroup(
            Text("Convolutions"),
            Text("Central Limit Theorem"),
            TexText(R"Why $\sqrt{\pi}$?"),
        )
        thumbnails = Group()
        for image, title in zip(images, titles):
            rect = SurroundingRectangle(image, buff=0).set_stroke(WHITE, 3)
            title.next_to(image, UP)
            title.set_max_width(image.get_width())
            thumbnails.add(Group(rect, image, title))

        thumbnails.arrange(DOWN, buff=LARGE_BUFF)
        thumbnails.set_height(7)
        thumbnails.to_corner(UL)
        thumbnails.to_edge(LEFT, buff=1.0)

        # Video 1
        morty = Mortimer(height=1).flip()
        morty.change_mode("tease")
        morty.next_to(images[0], RIGHT, MED_LARGE_BUFF, aligned_edge=DOWN)

        bubble = SpeechBubble(width=3, height=1)
        bubble.set_stroke(width=1)
        bubble.move_to(morty.get_corner(UR), DL).shift(SMALL_BUFF * LEFT)
        bubble.add_content(Text("In the next video..."))

        self.add(thumbnails[0])
        self.play(
            VFadeIn(morty),
            morty.change("speaking"),
            FadeIn(bubble),
            Write(bubble.content, run_time=1)
        )
        self.play(
            morty.animate.look_at(thumbnails[1]),
            FadeIn(thumbnails[1], DOWN)
        )

        # Video 2
        morty.generate_target()
        morty.target.align_to(thumbnails[1], DOWN)
        morty.target.change_mode("maybe").look_at(thumbnails[2])
        words = bubble.content
        words2 = Text("Or rather, the next one...", t2s={"next": ITALIC})
        bubble2 = morty.target.get_bubble(words2, bubble_type=SpeechBubble, width=4, height=1)
        bubble2.set_stroke(WHITE, 1)

        ghost1 = VGroup(morty, bubble, words).copy()
        to_fade = VGroup(ghost1)

        self.play(
            MoveToTarget(morty),
            Transform(bubble, bubble2),
            Transform(words, words2),
            ghost1.animate.set_opacity(0.25),
        )
        words.become(words2)
        self.play(Blink(morty), FadeIn(thumbnails[2], DOWN))

        # Video 3
        morty.generate_target()
        morty.target.align_to(thumbnails[2], DOWN)
        morty.target.change_mode("guilty")
        words3 = Text("But for real this time")
        bubble3 = morty.target.get_bubble(words3, bubble_type=SpeechBubble, width=4, height=1)
        bubble3.set_stroke(WHITE, 1)

        ghost2 = VGroup(morty, bubble, words).copy()
        to_fade.add(ghost2)

        self.play(
            MoveToTarget(morty),
            Transform(bubble, bubble3),
            Transform(words, words3),
            ghost2.animate.set_opacity(0.25)
        )
        words.become(words3)
        self.play(Blink(morty))
        self.wait(2)

        # Right screen
        screen = ScreenRectangle()
        screen.set_height(4)
        screen.set_stroke(WHITE, 2)
        screen.set_fill(BLACK, 1)
        screen.to_edge(RIGHT)

        arrows = VGroup(*(
            Arrow(thumbnail.get_right(), screen.get_left() + vect, buff=0.3)
            for thumbnail, vect in zip(thumbnails, [UP, ORIGIN, DOWN])
        ))

        self.play(
            LaggedStartMap(GrowArrow, arrows),
            FadeIn(screen),
            LaggedStartMap(FadeOut, VGroup(*to_fade, morty, bubble, words))
        )
        self.wait()
