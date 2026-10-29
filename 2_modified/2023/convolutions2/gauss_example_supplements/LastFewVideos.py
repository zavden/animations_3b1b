# ==============================================================================
# Scene:      LastFewVideos
# Source:     videos/_2023/convolutions2/gauss_example_supplements.py (lines 167-200)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl LastFewVideos.py LastFewVideos -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - 4 placeholder thumbnails (EquationThumbnail.png, Thumbnail.png, Thumbnail.jpg, Thumbnail2.png) at the root of _lib/assets/raster_images/ (make_convolutions2_assets.py); the scene asks for them by Grant's Dropbox path and manim_imports_ext finds them by name
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class LastFewVideos(InteractiveScene):
    def construct(self):
        self.add(FullScreenRectangle())

        # Images
        root = "/Users/grant/3Blue1Brown Dropbox/3Blue1Brown/videos/"
        images = Group(*(
            ImageMobject(os.path.join(root, ext))
            for ext in [
                "2022/convolutions/discrete/images/EquationThumbnail.png",
                "2023/clt/main/images/Thumbnail.png",
                "2023/clt/Thumbnail.jpg",
                "2023/convolutions2/Thumbnail/Thumbnail2.png",
            ]
        ))
        titles = VGroup(*(
            Text("Convolutions (discrete)"),
            Text("Central limit theorem"),
            TexText(R"Why $\pi$ is in a Gaussian"),
            Text("Convolutions (continuous)"),
        ))
        titles.scale(1.4)
        thumbnails = Group()
        for image, title in zip(images, titles):
            rect = SurroundingRectangle(image, buff=0)
            rect.set_stroke(WHITE, 3)
            title.next_to(image, UP, buff=MED_LARGE_BUFF)
            thumbnails.add(Group(rect, image, title))

        thumbnails.arrange_in_grid(buff=thumbnails[0].get_width() * 0.2)
        thumbnails.set_height(FRAME_HEIGHT - 1)

        self.play(LaggedStartMap(FadeIn, thumbnails, shift=UP, lag_ratio=0.7, run_time=4))
        self.wait()
