# ==============================================================================
# Scene:      OtherGreatOnes
# Source:     videos/_2023/SoME3/main.py (lines 371-404)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl OtherGreatOnes.py OtherGreatOnes -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - 31 placeholder thumbnails <title>.png at the root of _lib/assets/raster_images/ (make_some3_assets.py); the scenes ask for them by Grant's Dropbox path and manim_imports_ext finds them by name
# ==============================================================================

from manim_imports_ext import *

class OtherGreatOnes(InteractiveScene):
    def construct(self):
        self.add(FullScreenRectangle())
        names = [
           "Signed Distance Functions",
           "A Study In Greyscale",
           "Conservative matrix fields",
           "Are Elo Systems Overrated?",
           "The essence of multivariable calculus",
           "The Principle of Least Action",
        ]
        thumbnail_dir = "/Users/grant/3Blue1Brown Dropbox/3Blue1Brown/videos/2023/SoME3/EntryThumbnails"

        pieces = Group(*(
            Group(
                Text(name),
                ImageMobject(
                    os.path.join(thumbnail_dir, name),
                    height=4
                )
            ).arrange(UP)
            for name in names
        ))
        pieces.arrange_in_grid(2, 3, buff=0.5)
        # pieces[3:].match_x(pieces[:3])
        pieces.set_width(FRAME_WIDTH - 1)
        pieces.to_edge(DOWN)

        title = Text("Some others I personally enjoyed a lot", font_size=60)
        title.to_edge(UP)

        self.add(title)
        self.play(LaggedStartMap(FadeIn, pieces, lag_ratio=0.5, run_time=4))
        self.wait()
