# ==============================================================================
# Scene:      AppreciatingWithMath
# Source:     videos/_2026/print_gallery/supplements.py (lines 779-819)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl AppreciatingWithMath.py AppreciatingWithMath -w -m --fps 15
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

class AppreciatingWithMath(InteractiveScene):
    def construct(self):
        # Test
        randy = Randolph()
        randy.to_edge(DOWN)

        # CHANGE: LogImage.png lived in Grant's output folder; now it is next to this file
        # (placeholder image: the placeholder Print Gallery strip rotated 90 degrees).
        path = Path(__file__).parent / "LogImage.png"
        log_image = ImageMobject(path)
        log_image.set_width(7)
        log_image.to_corner(UL)
        log_label = Tex(R"\ln(z)", t2c={"z": BLUE})
        log_label.move_to(log_image).shift(0.45 * UP)
        log_group = Group(log_image, log_label)

        self.play(
            randy.change("raise_left_hand", 3 * UL),
            FadeIn(log_image, UP),
            Write(log_label),
        )
        self.play(Blink(randy))
        self.wait()
        self.play(randy.change("pondering", 3 * UR))
        self.play(Blink(randy))
        self.wait()

        # Add bubble
        rect = Rectangle(3, 1.5).set_opacity(0)
        bubble = randy.get_bubble(rect, direction=RIGHT)
        self.play(
            Write(bubble),
            log_group.animate.replace(rect, 0),
            randy.animate.look_at(bubble)
        )
        self.play(Blink(randy))
        self.play(randy.change("tease", 3 * UR))
        self.wait()
        self.play(Blink(randy))
        self.wait()
