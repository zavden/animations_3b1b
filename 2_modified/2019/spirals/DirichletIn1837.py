# ==============================================================================
# Scene:      DirichletIn1837
# Source:     videos/_2019/spirals.py (lines 3953-4042)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl DirichletIn1837.py DirichletIn1837 -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use CairoImageMobject to keep Cairo's default height and pixel reading, without changing other years.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: keep Cairo's height (2) and the pixel_array reading through a local adapter.
from cairo_compat import CairoImageMobject as ImageMobject

class DirichletIn1837(Scene):
    def construct(self):
        # Add timeline
        dates = list(range(1780, 2030, 10))
        timeline = NumberLine(
            x_min=1700,
            x_max=2020,
            tick_frequency=1,
            big_tick_numbers=dates,
            unit_size=0.2,
            stroke_color=GREY,
            stroke_width=2,
        )
        timeline.add_numbers(
            *dates,
            group_with_commas=False,
        )
        timeline.numbers.shift(SMALL_BUFF * DOWN)
        timeline.to_edge(RIGHT)

        # Special dates
        d_arrow, rh_arrow, pnt_arrow = arrows = VGroup(*[
            Vector(DOWN).next_to(timeline.n2p(date), UP)
            for date in [1837, 1859, 1896]
        ])
        d_label, rh_label, pnt_label = labels = VGroup(*[
            OldTexText(text).next_to(arrow, UP)
            for arrow, text in zip(arrows, [
                "Dirichlet's\\\\theorem\\\\1837",
                "Riemann\\\\hypothesis\\\\1859",
                "Prime number\\\\theorem\\\\1896",
            ])
        ])

        # Back in time
        frame = self.camera_frame
        self.add(timeline, arrows, labels)
        self.play(
            frame.move_to, timeline.n2p(1837),
            run_time=4,
        )
        self.wait()

        # Show picture
        image = ImageMobject("Dirichlet")
        image.set_height(3)
        image.next_to(d_label, LEFT)
        self.play(FadeIn(image, RIGHT))
        self.wait()

        # Flash
        self.play(
            Flash(
                d_label.get_center(),
                num_lines=12,
                line_length=0.25,
                flash_radius=1.5,
                line_stroke_width=3,
                lag_ratio=0.05,
            )
        )
        self.wait()

        # Transition title
        title, underline = self.get_title_and_underline()
        n = len(title[0])
        self.play(
            ReplacementTransform(d_label[0][:n], title[0][:n]),
            FadeOut(d_label[0][n:]),
            LaggedStartMap(
                FadeOutAndShiftDown, Group(
                    image, d_arrow,
                    rh_label, rh_arrow,
                    pnt_label, pnt_arrow,
                    *timeline,
                )
            ),
        )
        self.play(ShowCreation(underline))
        self.wait()

    def get_title_and_underline(self):
        frame = self.camera_frame
        title = OldTexText("Dirichlet's theorem")
        title.scale(1.5)
        title.next_to(frame.get_top(), DOWN, buff=MED_LARGE_BUFF)
        underline = Line()
        underline.match_width(title)
        underline.next_to(title, DOWN, SMALL_BUFF)
        return title, underline
