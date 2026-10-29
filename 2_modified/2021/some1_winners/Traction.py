# ==============================================================================
# Scene:      Traction
# Source:     videos/_2021/some1_winners.py (lines 765-792)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Traction.py Traction -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - raster_images/some1_thumbnails/<slug>.jpg: 90 placeholder thumbnails (30 WINNERS/HONORABLE_MENTIONS videos with their title and author + 60 synthetic entries) in _lib/assets/ (make_some1_assets.py); the scene would download them from YouTube with urllib
# ==============================================================================

from manim_imports_ext import *

def yt_slug_to_image_file(slug):
    return os.path.join(
        get_raster_image_dir(),
        "some1_thumbnails",
        slug + ".jpg"
    )


class Traction(Scene):
    def construct(self):
        slug_count_pairs = [
            ("PKjbBQ0PBCQ", "$\\sim$800,000"),
            ("ACZC_XEyg9U", "$\\sim$100,000"),
            ("4y_nmpv-9lI", "$\\sim$140,000"),
            ("cCKOl5li6YM", "$\\sim$400,000"),
        ]
        groups = Group()
        for slug, count in slug_count_pairs:
            rect = ScreenRectangle()
            rect.set_height(3)
            rect.set_stroke(BLUE, 2)
            image = ImageMobject(yt_slug_to_image_file(slug))
            image.replace(rect, 1)
            text = OldTexText(f"{count} views")
            text.next_to(image, DOWN, MED_SMALL_BUFF)
            groups.add(Group(image, rect, text))

        groups.arrange_in_grid(v_buff=MED_LARGE_BUFF, h_buff=LARGE_BUFF)
        groups.set_height(FRAME_HEIGHT - 1)

        for elem in groups:
            self.play(
                FadeIn(elem[:2]),
                FadeIn(elem[-1], 0.5 * DOWN, scale=2)
            )
        self.wait()
