# ==============================================================================
# Scene:      FourierGainsImmortality
# Source:     videos/_2019/diffyq/part4/staging.py (lines 137-210)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl FourierGainsImmortality.py FourierGainsImmortality -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use CairoImageMobject to keep Cairo's default height and pixel reading, without changing other years.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: keep Cairo's height (2) and the pixel_array reading through a local adapter.
from cairo_compat import CairoImageMobject as ImageMobject

class FourierGainsImmortality(Scene):
    CONFIG = {
        "mathematicians": [
            "Pythagoras",
            "Euclid",
            "Archimedes",
            "Fermat",
            "Newton",
            "Leibniz",
            "Johann_Bernoulli2",
            "Euler",
            "Joseph Fourier",
            "Gauss",
            "Riemann",
            "Cantor",
            "Noether",
            "Ramanujan",
            "Godel",
            "Turing",
        ]
    }

    def construct(self):
        fourier = ImageMobject("Joseph Fourier")
        fourier.set_height(5)
        fourier.to_edge(LEFT)
        name = OldTexText("Joseph Fourier")
        name.next_to(fourier, DOWN)

        immortals = self.get_immortals()
        immortals.remove(immortals.fourier)
        immortals.to_edge(RIGHT)

        self.add(fourier, name)
        self.play(LaggedStartMap(
            FadeIn, immortals,
            lag_ratio=0.1,
            run_time=2,
        ))
        self.play(
            TransformFromCopy(fourier, immortals.fourier)
        )
        self.wait()

    def get_immortals(self):
        images = Group(*[
            ImageMobject(name)
            for name in self.mathematicians
        ])
        for image in images:
            image.set_height(1)
        images.arrange_in_grid(n_rows=4)

        last_row = images[-4:]
        low_center = last_row.get_center()
        last_row.arrange(RIGHT, buff=0.4, center=False)
        last_row.move_to(low_center)

        frame = SurroundingRectangle(images)
        frame.set_color(WHITE)
        title = OldTexText("Immortals of Math")
        title.match_width(frame)
        title.next_to(frame, UP)

        result = Group(title, frame, *images)
        result.set_height(FRAME_HEIGHT - 1)
        result.to_edge(RIGHT)
        for image, name in zip(images, self.mathematicians):
            setattr(
                result,
                name.split(" ")[-1].lower(),
                image,
            )
        return result
