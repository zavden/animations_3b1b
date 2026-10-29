# ==============================================================================
# Scene:      LengthsOnDifferentColors
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 876-947)
# Category:   2 · Renders with modifications
# Includes code copied from: _2023/optics_puzzles/objects.py
#
# Run from this folder:
#     manimgl LengthsOnDifferentColors.py LengthsOnDifferentColors -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - ImageMobject used an absolute path in Grant's Dropbox (RainbowTubes.jpg); changed to the file name (placeholder image in raster_images)
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/RainbowTubes.jpg (placeholder, make_optics_puzzles_assets.py)
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *


# ----- From _2023/optics_puzzles/objects.py -----

class TwistedRibbon(ParametricSurface):
    def __init__(
        self,
        axes,
        amplitude,
        twist_rate,
        start_point=(0, 0, 0),
        color=WHITE,
        opacity=0.4,
        resolution=(101, 11),
    ):
        super().__init__(
            lambda u, v: axes.c2p(
                u,
                v * amplitude * np.sin(TAU * twist_rate * u),
                v * amplitude * np.cos(TAU * twist_rate * u)
            ),
            u_range=axes.x_range[:2],
            v_range=(-1, 1),
            color=color,
            opacity=opacity,
            resolution=resolution,
            preferred_creation_axis=0,
        )
        self.shift(axes.c2p(*start_point) - axes.get_origin())



# ----- From _2023/optics_puzzles/annotations.py -----

class LengthsOnDifferentColors(InteractiveScene):
    def construct(self):
        # Setup
        # CHANGE: the image lived in Grant's Dropbox (absolute path); now it is looked up by name in raster_images (placeholder)
        image = ImageMobject("RainbowTubes")
        image.set_height(FRAME_HEIGHT)
        # self.add(image)

        plane = NumberPlane()
        plane.fade(0.75)
        # self.add(plane)

        # Rectangles
        rects = Rectangle().replicate(4)
        rects.set_stroke(width=0)
        rects.set_fill(BLACK, opacity=0)
        rects.set_height(2)
        rects.set_width(FRAME_WIDTH, stretch=True)
        rects.arrange(DOWN, buff=0)

        # Braces
        lines = VGroup(
            Line(plane.c2p(3.2, 2.8), plane.c2p(-0.5, 2.8)),
            Line(plane.c2p(3.2, 0.9), plane.c2p(0.6, 0.9)),
            Line(plane.c2p(3.2, -1.0), plane.c2p(1.0, -1.0)),
            Line(plane.c2p(3.2, -3.0), plane.c2p(1.3, -3.0)),
        )
        braces = VGroup(*(
            Brace(line, DOWN, buff=SMALL_BUFF)
            for line in lines
        ))
        braces.set_backstroke(BLACK, 3)
        numbers = VGroup(*(
            DecimalNumber(line.get_length() / 7, font_size=36, unit=R" \text{m}")
            for line in lines
        ))
        for number, brace in zip(numbers, braces):
            number.next_to(brace, DOWN, buff=SMALL_BUFF)

        # Show braces
        for brace, rect, number in zip(braces, rects, numbers):
            other_rects = VGroup(*(r for r in rects if r is not rect))
            self.play(
                GrowFromPoint(brace, brace.get_right()),
                CountInFrom(number, 0),
                UpdateFromFunc(VGroup(), lambda m: number.next_to(brace, DOWN, SMALL_BUFF)),
                rect.animate.set_opacity(0),
                other_rects.animate.set_opacity(0.8),
            )
            self.wait(2)
        self.play(FadeOut(rects))

        # Ribbons
        axes_3d = ThreeDAxes((0, 6))
        ribbons = Group()
        twist_rates = [1.0 / PI / line.get_length() for line in lines]
        twist_rates = [0.09, 0.11, 0.115, 0.12]
        for line, twist_rate in zip(lines, twist_rates):
            ribbon = TwistedRibbon(
                axes_3d,
                amplitude=0.25,
                twist_rate=twist_rate,
                color=rgb_to_color(image.point_to_rgb(line.get_start())),
            )
            ribbon.rotate(PI / 2, RIGHT)
            ribbon.set_opacity(0.75)
            ribbon.flip(UP)
            ribbon.next_to(line, UP, MED_LARGE_BUFF, aligned_edge=RIGHT)
            ribbons.add(ribbon)

        for ribbon in ribbons:
            self.play(ShowCreation(ribbon, run_time=2))
        self.wait()
