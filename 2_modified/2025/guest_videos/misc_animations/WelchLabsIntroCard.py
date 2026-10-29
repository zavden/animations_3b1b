# ==============================================================================
# Scene:      WelchLabsIntroCard
# Source:     videos/_2025/guest_videos/misc_animations.py (lines 4-34)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl WelchLabsIntroCard.py WelchLabsIntroCard -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Banners/thumbnails of other channels replaced with placeholder images carrying the name as text (_tools/placeholder.py)
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/WelchLabsBanner.png
#   - _lib/assets/generated/2025/guest_videos/WelchLabsBanner.png
#
# Notes:
#   The banners and thumbnails of other channels/videos are not public: placeholder images were generated with _tools/placeholder.py (only the name as text, no logos), copied to _lib/assets/raster_images/ because the code looks them up by name.
# ==============================================================================

from manim_imports_ext import *

class WelchLabsIntroCard(InteractiveScene):
    title_words = "This is a guest video by Welch Labs"
    subtitle_words = ""
    logo_file = "WelchLabsLogo"
    banner_file = "WelchLabsBanner"
    bottom_words = "This is part of a series of guest videos, see the end for more details"

    def construct(self):
        # Add title and banners
        group = Group(
            VGroup(
                Text(self.title_words, font_size=48),
                Text(self.subtitle_words, font_size=36, fill_color=GREY_A),
            ).arrange(DOWN),
            ImageMobject(self.banner_file).set_width(0.7 * FRAME_WIDTH),
            Text(self.bottom_words, font_size=36),
        )
        group.arrange(DOWN, buff=MED_LARGE_BUFF)
        group[2].scale(1.1, about_edge=DOWN)
        group[-1].to_edge(DOWN, buff=MED_LARGE_BUFF)

        self.play(LaggedStart(
            Write(group[0], run_time=1, lag_ratio=5e-2),
            FadeIn(group[1], scale=1.25),
            FadeIn(group[2], lag_ratio=0.01),
            lag_ratio=0.05
        ))
        self.wait(2)
        self.play(
            LaggedStartMap(FadeOut, group, shift=1.0 * DOWN, lag_ratio=0.1)
        )
