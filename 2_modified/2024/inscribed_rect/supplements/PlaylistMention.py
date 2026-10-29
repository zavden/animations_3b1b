# ==============================================================================
# Scene:      PlaylistMention
# Source:     videos/_2024/inscribed_rect/supplements.py (lines 780-808)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl PlaylistMention.py PlaylistMention -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The YouTube thumbnail (downloaded at run time) is replaced with a local color card with the title (yt_card_OkmNXy7er84.png)
#
# Placeholder assets (not Grant's originals):
#   - raster_images/yt_card_OkmNXy7er84.png (_lib/assets/generated/replacements/visual/make_video_cards.py)
#
# Notes:
#   ImageMobject downloads the YouTube thumbnail by URL when rendering: it needs an internet connection (with a network it works unchanged, with the real thumbnail).
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class PlaylistMention(InteractiveScene):
    def construct(self):
        # Test
        rects = ScreenRectangle().replicate(8)
        rects.set_fill(GREY_E, 1)
        rects.set_stroke(WHITE, 1)
        group = Group()
        for x, rect in zip(np.linspace(1, 0, len(rects)), rects):
            rect.shift(x * 0.75 * UR)
            group.add(rect)
            group.add(Point())

        # CHANGE: the YouTube thumbnail was downloaded at run time; now it is a local color card with the title (raster_images/yt_card_<id>.png, make_video_cards.py)
        thumbnail = ImageMobject("yt_card_OkmNXy7er84")
        thumbnail.replace(rects[-1])
        group.add(thumbnail)

        group.set_height(2)
        group.to_edge(UP, buff=1.0)

        words = Text("More neat proofs\nand puzzle solutions")
        words.next_to(group, DOWN, buff=2.5)
        arrow = Arrow(words, group)
        self.play(
            FadeIn(group, UP),
            Write(words),
            GrowArrow(arrow)
        )
        self.wait()
        self.play(FadeOut(words), FadeOut(arrow))
