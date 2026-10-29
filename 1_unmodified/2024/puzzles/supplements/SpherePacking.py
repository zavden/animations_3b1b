# ==============================================================================
# Scene:      SpherePacking
# Source:     videos/_2024/puzzles/supplements.py (lines 767-797)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SpherePacking.py SpherePacking -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SpherePacking(InteractiveScene):
    samples = 4

    def construct(self):
        # Test
        frame = self.frame
        sphere = TrueDot(radius=math.sqrt(2) / 2)
        sphere.make_3d()
        max_x = 12
        spheres = Group(
            sphere.copy().move_to(coords)
            for coords in it.product(*3 * [np.arange(0, max_x)])
            if sum(coords) % 2 == 0
            if get_norm(coords) < max_x
        )
        spheres.sort(lambda p: get_norm(p))
        for sphere in spheres:
            sphere.set_color(random_bright_color(hue_range=(0.50, 0.55), luminance_range=(0.25, 0.5)))

        frame.reorient(89, 71, 0, (0, 0, 1), 10)
        self.play(
            LaggedStart(
                (FadeIn(sphere, scale=1.2)
                for sphere in spheres),
                lag_ratio=0.25,
                group_type=Group
            ),
            frame.animate.reorient(170, 64, 0, (2.7, -1.16, 1.8), 22.64),
            run_time=25
        )
        self.wait()
