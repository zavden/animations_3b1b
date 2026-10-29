# ==============================================================================
# Scene:      CompareAlgorithmToPhysics
# Source:     videos/_2019/clacks/question.py (lines 1336-1392)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl CompareAlgorithmToPhysics.py CompareAlgorithmToPhysics -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use CairoImageMobject to keep Cairo's default height and pixel reading, without changing other years.
#   - Recreate by script the mathematical chart of algorithm efficiency/elegance for pi and use it instead of the missing private capture.
#   - Expose the glyphs of the digits of pi to keep their staggered entrance with LaggedStartMap.
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/CX19PiAlgorithmsChart.png
# ==============================================================================

from manim_imports_ext import *

# CHANGE: keep Cairo's height (2) and the pixel_array reading through a local adapter.
from cairo_compat import CairoImageMobject as ImageMobject

class CompareAlgorithmToPhysics(PiCreatureScene):
    def construct(self):
        morty = self.pi_creature
        # CHANGE: use the reproducible mathematical chart instead of a private render path.
        right_pic = ImageMobject("CX19PiAlgorithmsChart")
        right_rect = SurroundingRectangle(right_pic, buff=0, color=WHITE)
        right_pic.add(right_rect)
        right_pic.set_height(3)
        right_pic.next_to(morty, UR)
        right_pic.shift_onto_screen()

        left_rect = right_rect.copy()
        left_rect.next_to(morty, UL)
        left_rect.shift_onto_screen()

        self.play(
            FadeInFromDown(right_pic),
            morty.change, "raise_right_hand",
        )
        self.wait()
        self.play(
            FadeInFromDown(left_rect),
            morty.change, "raise_left_hand",
        )
        self.wait()

        # CHANGE: expose glyphs so the digits retain their staggered entrance.
        digits = OldTex("3.141592653589793238462643383279502884197...")[0]
        digits.set_width(FRAME_WIDTH - 1)
        digits.to_edge(UP)
        self.play(
            FadeOut(right_pic, 5 * RIGHT),
            # FadeOut(left_rect, 5 * LEFT),
            FadeOut(left_rect),
            PiCreatureBubbleIntroduction(
                morty, "This doesn't seem \\\\ like me...",
                bubble_type=ThoughtBubble,
                bubble_config={"direction": LEFT},
                target_mode="pondering",
                look_at=left_rect,
            ),
            LaggedStartMap(
                FadeInFrom, digits,
                lambda m: (m, LEFT),
                run_time=5,
                lag_ratio=0.2,
            )
        )
        self.blink()
        self.wait()
        self.play(morty.change, "confused", left_rect)
        self.wait(5)

    def create_pi_creature(self):
        return Mortimer().flip().to_edge(DOWN)
