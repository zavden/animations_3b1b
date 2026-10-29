# ==============================================================================
# Scene:      AnnotateSetup
# Source:     videos/_2024/holograms/supplements.py (lines 524-604)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl AnnotateSetup.py AnnotateSetup -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Private images from Grant's Dropbox (CraigSallyHologramSetup.png) replaced with regenerable placeholders
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/CraigSallyHologramSetup.png  (placeholder; script: _lib/assets/generated/2024/holograms/make_holograms_assets.py)
# ==============================================================================

from manim_imports_ext import *

class AnnotateSetup(InteractiveScene):
    def construct(self):
        # Add iamge
        image = ImageMobject("CraigSallyHologramSetup")
        image.set_height(FRAME_HEIGHT)
        # self.add(image)

        # Reference polarization
        pol_words = Text("Correct the polarization")
        pol_words.set_backstroke(BLACK, 5)
        point = (-0.5, 1.2, 0)
        pol_words.next_to(point, UR, buff=1.5).shift(LEFT)
        pol_arrow = Arrow(pol_words["Correct"].get_bottom(), point)

        self.play(
            Write(pol_words),
            GrowArrow(pol_arrow)
        )
        self.wait()
        self.play(
            FadeOut(pol_words),
            FadeOut(pol_arrow),
        )

        # Show object beam
        obj_beam_points = [
            (-1.625, 2.167, 0),
            (-1.625, 1.264, 0),
            (0.375, 1.264, 0),
            (-0.625, -3.625, 0),
            (-0.111, -3.167, 0),
        ]

        obj_beam = VMobject().set_points_as_corners(obj_beam_points)
        obj_beam.set_stroke(GREEN_SCREEN, 4)
        obj_beam_name = Text("Object beam")
        obj_beam_name.set_color(GREEN_SCREEN)
        obj_beam_name.next_to(obj_beam.pfp(0.5), RIGHT)

        scene_point = (1.278, -1.972, 0)
        scene_circle = Circle(radius=0.75).shift(scene_point)
        obj_beam_spread = VGroup(
            Line(obj_beam_points[-1], scene_circle.pfp(a) + np.random.uniform(-0.025, 0.025, 3))
            for a in np.arange(0, 1, 0.001)
        )
        obj_beam_spread.set_stroke(GREEN_SCREEN, 1, 0.25)

        self.play(
            ShowCreation(obj_beam, rate_func=linear),
            FadeIn(obj_beam_name, lag_ratio=0.1),
        )
        self.play(ShowCreation(obj_beam_spread, lag_ratio=0, rate_func=rush_from))
        self.wait()

        # Show reference beam
        ref_beam_points = [
            obj_beam_points[0],
            (-1.61, -1.39, 0),
            (-1.056, -1.809, 0),
        ]
        ref_beam = obj_beam.copy()
        ref_beam.set_points_as_corners(ref_beam_points)
        ref_beam_name = Text("Reference beam")
        ref_beam_name.match_style(obj_beam_name)
        ref_beam_name.next_to(ref_beam.pfp(0.5), LEFT)

        ref_circle = Circle(radius=0.5)
        ref_circle.rotate(PI / 2, RIGHT)
        ref_circle.move_to((1.23, -3.39, 0))
        ref_beam_spread = VGroup(
            Line(ref_beam_points[-1], ref_circle.pfp(a) + np.random.uniform(-0.025, 0.025, 3))
            for a in np.arange(0, 1, 0.001)
        )
        ref_beam_spread.match_style(obj_beam_spread)

        self.play(
            FadeTransform(obj_beam_name, ref_beam_name),
            ReplacementTransform(obj_beam, ref_beam),
            ReplacementTransform(obj_beam_spread, ref_beam_spread),
        )
        self.wait()
