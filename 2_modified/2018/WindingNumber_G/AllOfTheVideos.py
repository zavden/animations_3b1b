# ==============================================================================
# Scene:      AllOfTheVideos
# Source:     videos/_2018/WindingNumber_G.py (lines 2888-2910)
# Category:   2 · Renders with modifications
# Includes code copied from: _2018/WindingNumber.py, _2018/uncertainty.py
#
# Run from this folder:
#     manimgl AllOfTheVideos.py AllOfTheVideos -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - the Dropbox folder of old thumbnails is gone; 16 generated placeholder thumbnails (_lib/assets/generated/2018/WindingNumber_G/make_old_thumbnails.py)
#
# Placeholder assets (not Grant's originals):
#   - raster_images/WindingOldThumbnails/thumb_01..16.png (generated placeholders, make_old_thumbnails.py)
# ==============================================================================

from manim_imports_ext import *
import warnings
import mpmath


# ----- From _2018/uncertainty.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")



# ----- From _2018/WindingNumber.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


mpmath.mp.dps = 7



# ----- From _2018/WindingNumber_G.py -----

class AllOfTheVideos(Scene):
    CONFIG = {
        "camera_config" : {
            "background_opacity" : 1,
        }
    }
    def construct(self):
        # CHANGE: the Dropbox folder of old thumbnails is gone; 16 generated placeholder thumbnails (_lib/assets/generated/2018/WindingNumber_G/make_old_thumbnails.py)
        thumbnail_dir = os.path.join(manim_config.directories.raster_images, "WindingOldThumbnails")
        n = 4
        images = Group(*[
            ImageMobject(os.path.join(thumbnail_dir, file))
            for file in os.listdir(thumbnail_dir)[:n**2]
        ])
        for image in images:
            rect = SurroundingRectangle(image, buff = 0)
            rect.set_stroke(WHITE, 1)
            image.add(rect)
        images.arrange_in_grid(n, n, buff = 0)
        images.set_height(FRAME_HEIGHT)
        random.shuffle(images.submobjects)

        self.play(LaggedStartMap(FadeIn, images, run_time = 4))
        self.wait()
