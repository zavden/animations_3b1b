# ==============================================================================
# Scene:      ImageTokens
# Source:     videos/_2024/transformers/embedding.py (lines 265-296)
# Category:   2 · Renders with modifications
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl ImageTokens.py ImageTokens -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/SmallFluffCreature.png  (_lib/assets/generated/2024/transformers/make_embedding_images.py)
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *


# ----- From _2024/transformers/helpers.py -----

def create_pixels(image_mob, pixel_width=0.1):
    x0, y0, z0 = image_mob.get_corner(UL)
    x1, y1, z1 = image_mob.get_corner(DR)
    points = np.array([
        [x, y, 0]
        for y in np.arange(y0, y1, -pixel_width)
        for x in np.arange(x0, x1, pixel_width)
    ])
    square = Square(pixel_width).set_fill(WHITE, 1).set_stroke(width=0)
    pixels = VGroup(
        square.copy().move_to(point, UL).set_color(
            Color(rgb=image_mob.point_to_rgb(point))
        )
        for point in points
    )
    return pixels



# ----- From _2024/transformers/embedding.py -----

class ImageTokens(InteractiveScene):
    n_divisions = 52

    def construct(self):
        # Add image
        image = ImageMobject("SmallFluffCreature")  # Change
        image.set_height(5)
        self.add(image)

        # Add pixels
        pixels = create_pixels(image, pixel_width=image.get_width() / self.n_divisions)
        big_pixels = create_pixels(image, pixel_width=image.get_width() / (self.n_divisions / 4))

        patches = big_pixels.copy().set_fill(opacity=0)
        p_points = np.array([p.get_center() for p in pixels])
        bp_points = np.array([bp.get_center() for bp in big_pixels])

        for pixel in pixels:
            dists = np.linalg.norm(bp_points - pixel.get_center(), axis=1)
            patches[np.argmin(dists)].add(pixel)

        # Anim test
        self.play(FadeIn(patches))
        self.remove(image)
        self.play(patches.animate.space_out_submobjects(2.0).scale(0.75))
        self.wait()
        self.play(LaggedStart(
            (patch.animate.set_stroke(TEAL, 3).set_anim_args(rate_func=there_and_back)
            for patch in patches),
            lag_ratio=5.0 / len(patches),
        ))
        self.wait()
