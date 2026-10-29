# ==============================================================================
# Scene:      FinalCommentsOnPhaseSpace
# Source:     videos/_2019/clacks/solution1.py (lines 2952-3046)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl FinalCommentsOnPhaseSpace.py FinalCommentsOnPhaseSpace -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use CairoImageMobject to keep Cairo's default height and pixel reading, without changing other years.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: keep Cairo's height (2) and the pixel_array reading through a local adapter.
from cairo_compat import CairoImageMobject as ImageMobject

class FinalCommentsOnPhaseSpace(Scene):
    def construct(self):
        self.add_title()
        self.show_related_fields()
        self.state_to_point()
        self.puzzle_as_remnant()

    def add_title(self):
        title = self.title = OldTexText("Phase space")
        title.scale(2)
        title.to_edge(UP)
        title.set_color(YELLOW)

        self.play(Write(title))

    def show_related_fields(self):
        title = self.title

        images = Group(
            ImageMobject("ClacksThumbnail"),
            ImageMobject("PictoralODE"),
            # ImageMobject("DoublePendulumStart"),
            ImageMobject("MobiusStrip"),
        )
        colors = [BLUE_D, GREY_BROWN, BLUE_C]
        for image, color in zip(images, colors):
            image.set_height(2.5)
            image.add(SurroundingRectangle(
                image,
                color=color,
                stroke_width=5,
                buff=0,
            ))
        images.arrange(RIGHT)
        images.move_to(DOWN)

        arrows = VGroup(*[
            Arrow(
                title.get_bottom(), image.get_top(),
                color=WHITE,
            )
            for image in images
        ])

        for image, arrow in zip(images, arrows):
            self.play(
                GrowArrow(arrow),
                GrowFromPoint(image, title.get_bottom()),
            )
            self.wait()
        self.wait()

        self.to_fade = Group(images, arrows)

    def state_to_point(self):
        state = OldTexText("State")
        arrow = Arrow(
            2 * LEFT, 2 * RIGHT,
            color=WHITE,
            rectangular_stem_width=0.1,
            tip_length=0.5
        )
        point = OldTexText("Point")
        dynamics = OldTexText("Dynamics")
        geometry = OldTexText("Geometry")
        words = VGroup(state, point, dynamics, geometry)
        for word in words:
            word.scale(2)

        group = VGroup(state, arrow, point)
        group.arrange(RIGHT, buff=MED_LARGE_BUFF)
        group.move_to(2.5 * DOWN)

        dynamics.move_to(state, RIGHT)
        geometry.move_to(point, LEFT)

        self.play(
            FadeOut(self.to_fade, UP),
            FadeIn(state, UP)
        )
        self.play(
            GrowArrow(arrow),
            FadeIn(point, LEFT)
        )
        self.wait(2)
        for w1, w2 in [(state, dynamics), (point, geometry)]:
            self.play(
                FadeOut(w1, UP),
                FadeIn(w2, DOWN),
            )
            self.wait()
        self.wait()

    def puzzle_as_remnant(self):
        pass
