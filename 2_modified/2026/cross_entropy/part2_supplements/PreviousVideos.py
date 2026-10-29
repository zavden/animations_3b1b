# ==============================================================================
# Scene:      PreviousVideos
# Source:     videos/_2026/cross_entropy/part2_supplements.py (lines 99-125)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl PreviousVideos.py PreviousVideos -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The 2 YouTube thumbnails (downloaded at run time) are replaced with local color cards carrying the video title (yt_card_<id>.png)
#
# Placeholder assets (not Grant's originals):
#   - raster_images/yt_card_IHZwWFHWa-w.png and yt_card_Ilg3gGewQ5U.png (_lib/assets/generated/replacements/visual/make_video_cards.py)
# ==============================================================================

from manim_imports_ext import *

class PreviousVideos(InteractiveScene):
    def construct(self):
        # Test
        images = Group(
            # CHANGE: the YouTube thumbnail was downloaded at run time; now it is a local color card with the title (raster_images/yt_card_<id>.png, make_video_cards.py)
            ImageMobject("yt_card_IHZwWFHWa-w"),
            ImageMobject("yt_card_Ilg3gGewQ5U"),
        )
        thumbnails = Group(
            Group(
                SurroundingRectangle(image, buff=0).set_stroke(WHITE, 3),
                image
            )
            for image in images
        )
        thumbnails.set_width(4)
        thumbnails.arrange(DOWN, buff=1.5)
        thumbnails.to_corner(UL).to_edge(LEFT, buff=LARGE_BUFF)
        titles = VGroup(Text("Gradient Descent"), Text("Backpropagation"))

        for title, tn in zip(titles, thumbnails):
            title.next_to(tn, DOWN)
            self.play(LaggedStart(
                FadeIn(tn, 0.5 * DOWN),
                FadeIn(title, 1.0 * DOWN),
                lag_ratio=0.2
            ))
        self.wait()
