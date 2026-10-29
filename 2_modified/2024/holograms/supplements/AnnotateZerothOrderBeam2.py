# ==============================================================================
# Scene:      AnnotateZerothOrderBeam2
# Source:     videos/_2024/holograms/supplements.py (lines 826-876)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl AnnotateZerothOrderBeam2.py AnnotateZerothOrderBeam2 -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Private images from Grant's Dropbox (DiffractionGratingGreenLaser.jpg) replaced with regenerable placeholders
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/DiffractionGratingGreenLaser.jpg  (placeholder; script: _lib/assets/generated/2024/holograms/make_holograms_assets.py)
# ==============================================================================

from manim_imports_ext import *

class AnnotateZerothOrderBeam2(InteractiveScene):
    def construct(self):
        image = ImageMobject("DiffractionGratingGreenLaser.jpg")
        # self.add(image.set_height(FRAME_HEIGHT))

        # Names
        points = [
            (-0.67, 1.64, 0.0),
            (3.64, 1.9, 0.0),
            (-4.9, 1.85, 0.0),
            (-5.4, 1.01),
            (2.42, 0.028),
        ]

        names = VGroup(
            Text("Zeroth-order beam"),
            Text("First-order beams"),
            Text("Second-order beams"),
        )
        names.next_to(points[0], UP, buff=2.5)
        names.shift_onto_screen()
        arrow0 = Arrow(names[0], points[0])
        arrows1 = VGroup(
            Arrow(names[1].get_bottom(), points[1]),
            Arrow(names[1].get_bottom(), points[2]),
        )
        arrows2 = VGroup(
            Arrow(names[2].get_bottom(), points[3]),
            Arrow(names[2].get_bottom(), points[4]),
        )
        VGroup(names, arrow0, arrows1, arrows2).set_fill(GREY_E)

        self.play(
            Write(names[0]),
            GrowArrow(arrow0),
            run_time=1
        )
        self.wait()
        self.remove(arrow0)
        self.play(
            TransformMatchingStrings(names[0], names[1], key_map={"Zeroth": "First", "m": "ms"}),
            TransformFromCopy(arrow0.replicate(2), arrows1),
            run_time=1
        )
        self.wait()
        self.play(
            TransformMatchingStrings(names[1], names[2], key_map={"First": "Second"}),
            ReplacementTransform(arrows1, arrows2),
            run_time=1
        )
        self.wait()
