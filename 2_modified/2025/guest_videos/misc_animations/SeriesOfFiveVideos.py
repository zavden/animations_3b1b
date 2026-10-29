# ==============================================================================
# Scene:      SeriesOfFiveVideos
# Source:     videos/_2025/guest_videos/misc_animations.py (lines 270-341)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SeriesOfFiveVideos.py SeriesOfFiveVideos -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Banners/thumbnails of other channels replaced with placeholder images carrying the name as text (_tools/placeholder.py)
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/diffusion_TN.png
#   - _lib/assets/raster_images/alpha_geometry_TN.png
#   - _lib/assets/raster_images/phase_change_TN.png
#   - _lib/assets/raster_images/incomplete_cubes_TN.png
#   - _lib/assets/raster_images/euclid_TN.png
#   - _lib/assets/generated/2025/guest_videos/diffusion_TN.png
#   - _lib/assets/generated/2025/guest_videos/alpha_geometry_TN.png
#   - _lib/assets/generated/2025/guest_videos/phase_change_TN.png
#   - _lib/assets/generated/2025/guest_videos/incomplete_cubes_TN.png
#   - _lib/assets/generated/2025/guest_videos/euclid_TN.png
#
# Notes:
#   The banners and thumbnails of other channels/videos are not public: placeholder images were generated with _tools/placeholder.py (only the name as text, no logos), copied to _lib/assets/raster_images/ because the code looks them up by name.
# ==============================================================================

from manim_imports_ext import *

class SeriesOfFiveVideos(InteractiveScene):
    def construct(self):
        # Add images
        self.add(FullScreenRectangle(fill_color=GREY_E))

        pure_images = Group(
            ImageMobject(filename)
            for filename in [
                "diffusion_TN",
                "alpha_geometry_TN",
                "phase_change_TN",
                "incomplete_cubes_TN",
                "euclid_TN",
            ]
        )
        borders = VGroup(SurroundingRectangle(image, buff=0) for image in pure_images)
        borders.set_stroke(WHITE, 3)

        images = Group(
            Group(border, image)
            for border, image in zip(borders, pure_images)
        )

        images.set_width(4)
        images.arrange_in_grid(n_cols=3, buff=1)
        images[3:].match_x(images[:3]).shift(MED_LARGE_BUFF * DOWN)
        images.set_width(FRAME_WIDTH - 1)

        # Add names
        names = VGroup(
            Text(f"Guest video by {text}", font_size=30)
            for text in [
                "Welch Labs",
                "Aleph0",
                "Vilas Winstein",
                "Paul Dancstep",
                "Ben Syversen",
            ]
        )
        for name, image in zip(names, images):
            name.next_to(image, UP, MED_SMALL_BUFF)
            image.add(name)

        # Animate in
        frame = self.frame
        frame.set_height(4).move_to(images[-1])
        self.add(images[-1])
        self.wait()
        self.play(
            frame.animate.to_default_state(),
            LaggedStartMap(FadeIn, images[3::-1], lag_ratio=0.25),
            run_time=3,
        )
        self.wait()

        # Swap out for topics
        titles = VGroup(
            Text("Diffusion models"),
            Text("AlphaGeometry"),
            Text("Statistical Mechanics"),
            Text("Group theory"),
            Text("Euclid"),
        )
        titles.scale(0.8)
        for title, name, image in zip(titles, names, images):
            title.move_to(name, DOWN)
            self.play(
                LaggedStart(FadeIn(title, 0.25 * UP), FadeOut(name, 0.25 * UP), lag_ratio=0.2),
                pure_images.animate.set_opacity(0.25),
                borders.animate.set_stroke(opacity=0.25),
            )
        self.wait()
