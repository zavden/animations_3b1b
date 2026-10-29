# ==============================================================================
# Scene:      PreviewQuarterBehindReason
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 615-647)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PreviewQuarterBehindReason.py PreviewQuarterBehindReason -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PreviewQuarterBehindReason(InteractiveScene):
    def construct(self):
        # Plane
        plane = ComplexPlane(
            (-3, 3), (-3, 3),
            background_line_style=dict(stroke_width=2, stroke_color=BLUE),
            faded_line_style=dict(stroke_width=1, stroke_opacity=0.3, stroke_color=BLUE),
        )
        plane.set_height(7)
        self.add(plane)

        # Add little vectors
        z1 = 1 + complex(-4e-3, -0.05)
        amp = 0.08
        zs = np.array([amp * z1**n for n in range(1000)])
        vects = VGroup(*(
            Vector(plane.n2p(z), stroke_width=2)
            for z in zs
        ))
        vects.set_submobject_colors_by_gradient(YELLOW, RED)
        for v1, v2 in zip(vects, vects[1:]):
            v2.shift(v1.get_end() - v2.get_start())

        big_vect = Vector(stroke_width=5)
        big_vect.add_updater(lambda m: m.put_start_and_end_on(
            plane.n2p(0), vects[-1].get_end() if len(vects) > 0 else plane.n2p(amp)
        ))

        self.add(big_vect)
        self.play(
            ShowIncreasingSubsets(vects, rate_func=linear, run_time=8)
        )
        self.wait()
