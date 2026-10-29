# ==============================================================================
# Scene:      MathVsIntuition
# Source:     videos/_2026/print_gallery/supplements.py (lines 66-88)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl MathVsIntuition.py MathVsIntuition -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - LogImage.png is read next to the file instead of from Grant's output folder
#   - LogImage.png is a placeholder image (a placeholder Print Gallery strip rotated 90 degrees)
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/generated/2026/print_gallery/exponential/LogImage.png
#
# Notes:
#   The original images (the rectified 'Print Gallery' lithograph and LogImage) are private. Placeholder images were generated with _lib/assets/generated/2026/print_gallery/make_print_gallery_assets.py: periodic strips with picture frames, with square cells in (log r, theta) space; after exp / Droste zoom the ring and sector structure is visible. It is not Escher's work.
# ==============================================================================

from manim_imports_ext import *

class MathVsIntuition(InteractiveScene):
    def construct(self):
        morty = Mortimer().to_edge(DOWN)
        morty.body.insert_n_curves(100)
        # CHANGE: LogImage.png lived in Grant's output folder; now it is next to this file
        # (placeholder image: the placeholder Print Gallery strip rotated 90 degrees).
        log_image = ImageMobject(Path(__file__).parent / "LogImage.png")
        log_image.set_height(3)
        log_image.next_to(morty, UP).to_edge(LEFT)

        self.play(
            morty.change("raise_right_hand", log_image),
            FadeIn(log_image, UP)
        )
        self.play(Blink(morty))
        self.wait()
        self.play(
            morty.change("raise_left_hand", 3 * UR),
            log_image.animate.scale(0.5, about_edge=LEFT).fade(0.5),
        )
        self.play(Blink(morty))
        self.wait()
