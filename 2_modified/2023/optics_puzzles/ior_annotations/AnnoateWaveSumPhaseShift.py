# ==============================================================================
# Scene:      AnnoateWaveSumPhaseShift
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 577-612)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl AnnoateWaveSumPhaseShift.py AnnoateWaveSumPhaseShift -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The WaveSumPhaseShift image is missing (private): placeholder image; the code does not change
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/WaveSumPhaseShift.png (placeholder, make_optics_puzzles_assets.py)
# ==============================================================================

from manim_imports_ext import *

class AnnoateWaveSumPhaseShift(InteractiveScene):
    def construct(self):
        image = ImageMobject("WaveSumPhaseShift")
        image.set_height(FRAME_HEIGHT).center()
        # self.add(image)

        # Test
        wave_len = 4.0
        point1 = (-1.31, 2.33, 0)
        point2 = (-2.3, 0, 0)

        line = DashedLine(UP, DOWN)
        lines1 = line.get_grid(1, 6, h_buff=wave_len / 2)
        lines1.set_height(1.0, stretch=True)
        lines1.set_stroke(YELLOW, 3)
        lines1.move_to(point1 + wave_len * LEFT / 2, LEFT)

        lines2 = lines1.copy()
        lines2.move_to(point2 + wave_len * LEFT / 2, LEFT)

        arrow = Arrow(
            lines2[1].get_top(),
            lines1[1].get_bottom(),
            buff=0.2
        )
        label = TexText(R"$90^\circ$ behind")
        label.next_to(arrow.get_center(), RIGHT)

        self.play(LaggedStartMap(ShowCreation, lines2, lag_ratio=0, run_time=0.5))
        self.wait()
        self.play(
            TransformFromCopy(lines2, lines1),
            GrowArrow(arrow),
            FadeIn(label, lag_ratio=0.1),
        )
        self.wait()
