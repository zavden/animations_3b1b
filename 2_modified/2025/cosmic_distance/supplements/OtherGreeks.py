# ==============================================================================
# Scene:      OtherGreeks
# Source:     videos/_2025/cosmic_distance/supplements.py (lines 1016-1037)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl OtherGreeks.py OtherGreeks -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The illustrations are looked up in KurtArtwork/ next to this file (before: Grant's Dropbox) and are placeholders.
#
# Placeholder assets (not Grant's originals):
#   - KurtArtwork/AristarchusProposingEarthGoesAroundTheSun.jpg and stencil-luma-masks/figure-1..9-masked.png (scene with 9 generic silhouettes and their masks, placeholders)
# ==============================================================================

from manim_imports_ext import *

class OtherGreeks(InteractiveScene):
    def construct(self):
        # Test
        # CHANGE: the illustrations lived in Grant's Dropbox; now there are placeholders in KurtArtwork/ next to this file.
        folder = Path(__file__).parent / 'KurtArtwork'
        base_image = ImageMobject(Path(folder, 'AristarchusProposingEarthGoesAroundTheSun.jpg'))
        sub_images = Group(
            ImageMobject(Path(folder, "stencil-luma-masks", f"figure-{n}-masked.png"))
            for n in range(1, 10)
        )
        for image in [base_image, *sub_images]:
            image.set_height(FRAME_HEIGHT)

        base_image.set_opacity(0.25)
        self.add(base_image)
        self.add(sub_images[0])
        self.play(
            *(
                FadeIn(im, rate_func=there_and_back_with_pause, time_span=(0.25 * n, 0.25 * n + 7))
                for n, im in enumerate(sub_images)
            ),
            run_time=8
        )
