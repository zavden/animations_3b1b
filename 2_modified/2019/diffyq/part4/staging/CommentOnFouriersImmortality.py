# ==============================================================================
# Scene:      CommentOnFouriersImmortality
# Source:     videos/_2019/diffyq/part4/staging.py (lines 345-391)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl CommentOnFouriersImmortality.py CommentOnFouriersImmortality -w -m --fps 15
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


class CommentOnFouriersImmortality(FourierGainsImmortality):
    def construct(self):
        immortals = self.get_immortals()
        immortals.to_edge(LEFT)
        fourier = immortals.fourier
        name = OldTexText("Joseph", "Fourier")
        name.scale(1.5)
        name.move_to(FRAME_WIDTH * RIGHT / 4)
        name.to_edge(DOWN)

        fourier_things = VGroup(
            OldTexText("Fourier transform"),
            OldTexText("Fourier series"),
            OldTexText("Complex Fourier series"),
            OldTexText("Discrete Fourier transform"),
            OldTexText("Fractional Fourier transform"),
            OldTexText("Fast Fourier transform"),
            OldTexText("Quantum Fourier transform"),
            OldTexText("Fourier transform spectroscopy"),
            OldTex("\\vdots"),
        )
        fourier_things.arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=MED_LARGE_BUFF
        )
        fourier_things.to_corner(UL)
        fourier_things[-1].shift(RIGHT + 0.25 * UP)

        self.add(immortals)
        immortals.remove(immortals.fourier)
        self.play(
            fourier.set_height, 6,
            fourier.next_to, name, UP,
            FadeInFromDown(name),
        )
        self.play(FadeOut(immortals))
        self.wait(2)
        self.play(
            LaggedStartMap(
                FadeInFrom, fourier_things,
                lambda m: (m, UP),
                run_time=5,
                lag_ratio=0.3,
            )
        )
        self.wait()
