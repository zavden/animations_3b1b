# ==============================================================================
# Scene:      PartTwoOfTour
# Source:     videos/_2019/diffyq/part2/staging.py (lines 5-48)
# Category:   2 · Renders with modifications
# Includes code copied from: _2019/diffyq/part1/staging.py
#
# Run from this folder:
#     manimgl PartTwoOfTour.py PartTwoOfTour -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use CairoImageMobject to keep Cairo's default height and pixel reading, without changing other years.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: keep Cairo's height (2) and the pixel_array reading through a local adapter.
from cairo_compat import CairoImageMobject as ImageMobject


# ----- From _2019/diffyq/part1/staging.py -----

class TourOfDifferentialEquations(MovingCameraScene):
    CONFIG = {
        "screen_rect_style": {
            "stroke_width": 2,
            "stroke_color": WHITE,
            "fill_opacity": 1,
            "fill_color": BLACK,
        },
        "camera_config": {"background_color": GREY_E},
        "zoomed_thumbnail_index": 0,
    }

    def construct(self):
        self.add_title()
        self.show_thumbnails()
        self.zoom_in_to_one_thumbnail()
        # self.show_words()

    def add_title(self):
        title = OldTexText(
            "A Tourist's Guide \\\\to Differential\\\\Equations"
        )
        title.scale(1.5)
        title.to_corner(UR)
        self.add(title)

    def show_thumbnails(self):
        thumbnails = self.thumbnails = Group(
            Group(ScreenRectangle(**self.screen_rect_style)),
            Group(ScreenRectangle(**self.screen_rect_style)),
            Group(ScreenRectangle(**self.screen_rect_style)),
            Group(ScreenRectangle(**self.screen_rect_style)),
            Group(ScreenRectangle(**self.screen_rect_style)),
        )
        n = len(thumbnails)
        thumbnails.set_height(1.5)

        line = self.line = CubicBezier(
            [-5, 3, 0],
            [3, 3, 0],
            [-3, -3, 0],
            [5, -3, 0],
        )
        line.shift(MED_SMALL_BUFF * LEFT)
        for thumbnail, a in zip(thumbnails, np.linspace(0, 1, n)):
            thumbnail.move_to(line.point_from_proportion(a))
        dots = OldTex("\\dots")
        dots.next_to(thumbnails[-1], RIGHT)

        self.add_phase_space_preview(thumbnails[0])
        self.add_heat_preview(thumbnails[1])
        self.add_fourier_series(thumbnails[2])
        self.add_matrix_exponent(thumbnails[3])
        self.add_laplace_symbol(thumbnails[4])

        self.play(
            ShowCreation(
                line,
                rate_func=lambda t: np.clip(t * (n + 1) / n, 0, 1)
            ),
            LaggedStart(*[
                GrowFromCenter(
                    thumbnail,
                    rate_func=squish_rate_func(
                        smooth,
                        0, 0.7,
                    )
                )
                for thumbnail in thumbnails
            ], lag_ratio=1),
            run_time=5
        )
        self.play(Write(dots))
        self.wait()

        self.thumbnails = thumbnails

    def zoom_in_to_one_thumbnail(self):
        self.play(
            self.camera_frame.replace,
            self.thumbnails[self.zoomed_thumbnail_index],
            run_time=3,
        )
        self.wait()

    def show_words(self):
        words = VGroup(
            OldTexText("Generalize"),
            OldTexText("Put in context"),
            OldTexText("Modify"),
        )
        # words.arrange(DOWN, aligned_edge=LEFT, buff=LARGE_BUFF)
        words.scale(1.5)
        words.to_corner(UR)
        words.add_to_back(VectorizedPoint(words.get_center()))
        words.add(VectorizedPoint(words.get_center()))

        diffEq = OldTexText("Differential\\\\equations")
        diffEq.scale(1.5)
        diffEq.to_corner(DL, buff=LARGE_BUFF)

        for word1, word2 in zip(words, words[1:]):
            self.play(
                FadeInFromDown(word2),
                FadeOut(word1, UP),
            )
            self.wait()
        self.play(
            ReplacementTransform(
                VGroup(self.thumbnails).copy().fade(1),
                diffEq,
                lag_ratio=0.01,
            )
        )
        self.wait()

    #
    def add_phase_space_preview(self, thumbnail):
        image = ImageMobject("LovePhaseSpace")
        image.replace(thumbnail)
        thumbnail.add(image)

    def add_heat_preview(self, thumbnail):
        image = ImageMobject("HeatSurfaceExample")
        image.replace(thumbnail)
        thumbnail.add(image)

    def add_matrix_exponent(self, thumbnail):
        matrix = IntegerMatrix(
            [[3, 1], [4, 1]],
            v_buff=MED_LARGE_BUFF,
            h_buff=MED_LARGE_BUFF,
            bracket_h_buff=SMALL_BUFF,
            bracket_v_buff=SMALL_BUFF,
        )
        e = OldTex("e")
        t = OldTex("t")
        t.scale(1.5)
        t.next_to(matrix, RIGHT, SMALL_BUFF)
        e.scale(2)
        e.move_to(matrix.get_corner(DL), UR)
        group = VGroup(e, matrix, t)
        group.set_height(0.7 * thumbnail.get_height())
        randy = Randolph(mode="confused", height=0.75)
        randy.next_to(group, LEFT, aligned_edge=DOWN)
        randy.look_at(matrix)
        group.add(randy)
        group.move_to(thumbnail)
        thumbnail.add(group)

    def add_fourier_series(self, thumbnail):
        colors = [BLUE, GREEN, YELLOW, RED, RED_E, PINK]

        waves = VGroup(*[
            self.get_square_wave_approx(N, color)
            for N, color in enumerate(colors)
        ])
        waves.set_stroke(width=1.5)
        waves.replace(thumbnail, stretch=True)
        waves.scale(0.8)
        waves.move_to(thumbnail)
        thumbnail.add(waves)

    def get_square_wave_approx(self, N, color):
        return FunctionGraph(
            lambda x: sum([
                (1 / n) * np.sin(n * PI * x)
                for n in range(1, 2 * N + 3, 2)
            ]),
            x_min=0,
            x_max=2,
            color=color
        )

    def add_laplace_symbol(self, thumbnail):
        mob = OldTex(
            "\\mathcal{L}\\left\\{f(t)\\right\\}"
        )
        mob.set_width(0.8 * thumbnail.get_width())
        mob.move_to(thumbnail)
        thumbnail.add(mob)



# ----- From _2019/diffyq/part2/staging.py -----

class PartTwoOfTour(TourOfDifferentialEquations):
    CONFIG = {
        "zoomed_thumbnail_index": 1,
    }

    def construct(self):
        self.add_title()
        self.show_thumbnails()
        self.zoom_in_to_one_thumbnail()

    def zoom_in_to_one_thumbnail(self):
        frame = self.camera_frame
        thumbnails = self.thumbnails

        ode = OldTexText("Ordinary\\\\", "Differential Equation")
        pde = OldTexText("Partial\\\\", "Differential Equation")
        for word, thumbnail, vect in zip([ode, pde], thumbnails, [DOWN, UP]):
            word.match_width(thumbnail)
            word.next_to(thumbnail, vect)
        ode[0].set_color(BLUE)
        pde[0].set_color(YELLOW)

        self.add(ode)

        frame.save_state()
        self.play(
            frame.replace,
            thumbnails[0],
            run_time=1,
        )
        self.play(
            Restore(frame, run_time=3),
        )
        self.play(
            TransformFromCopy(ode, pde),
        )
        self.play(
            ApplyMethod(
                frame.replace, thumbnails[1],
                path_arc=(-30 * DEGREES),
                run_time=3
            ),
        )
        self.wait()
