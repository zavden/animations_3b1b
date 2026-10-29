# ==============================================================================
# Scene:      NameCraigAndSally
# Source:     videos/_2024/holograms/supplements.py (lines 367-395)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl NameCraigAndSally.py NameCraigAndSally -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Private images from Grant's Dropbox (CraigSallyPaulGrant.png) replaced with regenerable placeholders
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/CraigSallyPaulGrant.png  (placeholder; script: _lib/assets/generated/2024/holograms/make_holograms_assets.py)
# ==============================================================================

from manim_imports_ext import *

class NameCraigAndSally(InteractiveScene):
    def construct(self):
        # Test
        image = ImageMobject("CraigSallyPaulGrant")
        image.set_height(FRAME_HEIGHT)

        craig_point = (1.2, 2.0, 0)
        sally_point = (3.9, 1.3, 0)

        craig_arrow = Vector(DR, thickness=5)
        craig_arrow.next_to(craig_point, UL)
        craig_name = Text("Craig Newswanger")
        craig_name.next_to(craig_arrow.get_start(), UP, buff=SMALL_BUFF)

        sally_arrow = Vector(DL, thickness=5)
        sally_arrow.next_to(sally_point, UR)
        sally_name = Text("Sally Weber")
        sally_name.next_to(sally_arrow.get_start(), UP, buff=SMALL_BUFF)

        VGroup(craig_arrow, craig_name, sally_arrow, sally_name).set_fill(WHITE).set_backstroke(BLACK, 5)

        self.play(
            GrowArrow(craig_arrow),
            FadeIn(craig_name),
        )
        self.play(
            GrowArrow(sally_arrow),
            FadeIn(sally_name),
        )
