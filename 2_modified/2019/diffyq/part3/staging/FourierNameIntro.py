# ==============================================================================
# Scene:      FourierNameIntro
# Source:     videos/_2019/diffyq/part3/staging.py (lines 6-200)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl FourierNameIntro.py FourierNameIntro -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use CairoImageMobject to keep Cairo's default height and pixel reading, without changing other years.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: keep Cairo's height (2) and the pixel_array reading through a local adapter.
from cairo_compat import CairoImageMobject as ImageMobject

class FourierNameIntro(Scene):
    def construct(self):
        self.show_two_titles()
        self.transition_to_image()
        self.show_paper()

    def show_two_titles(self):
        lt = OldTexText("Fourier", "Series")
        rt = OldTexText("Fourier", "Transform")
        lt_variants = VGroup(
            OldTexText("Complex", "Fourier Series"),
            OldTexText("Discrete", "Fourier Series"),
        )
        rt_variants = VGroup(
            OldTexText("Discrete", "Fourier Transform"),
            OldTexText("Fast", "Fourier Transform"),
            OldTexText("Quantum", "Fourier Transform"),
        )

        titles = VGroup(lt, rt)
        titles.scale(1.5)
        for title, vect in (lt, LEFT), (rt, RIGHT):
            title.move_to(vect * FRAME_WIDTH / 4)
            title.to_edge(UP)

        for title, variants in (lt, lt_variants), (rt, rt_variants):
            title.save_state()
            title.target = title.copy()
            title.target.scale(1 / 1.5, about_edge=RIGHT)
            for variant in variants:
                variant.move_to(title.target, UR)
                variant[0].set_color(YELLOW)

        v_line = Line(UP, DOWN)
        v_line.set_height(FRAME_HEIGHT)
        v_line.set_stroke(WHITE, 2)

        self.play(
            FadeIn(lt, RIGHT),
            ShowCreation(v_line)
        )
        self.play(
            FadeIn(rt, LEFT),
        )
        # Edit in images of circle animations
        # and clips from FT video

        # for title, variants in (rt, rt_variants), (lt, lt_variants):
        for title, variants in [(rt, rt_variants)]:
            # Maybe do it for left variant, maybe not...
            self.play(
                MoveToTarget(title),
                FadeIn(variants[0][0], LEFT)
            )
            for v1, v2 in zip(variants, variants[1:]):
                self.play(
                    FadeOut(v1[0], UP),
                    FadeIn(v2[0], DOWN),
                    run_time=0.5,
                )
                self.wait(0.5)
            self.play(
                Restore(title),
                FadeOut(variants[-1][0])
            )
        self.wait()

        self.titles = titles
        self.v_line = v_line

    def transition_to_image(self):
        titles = self.titles
        v_line = self.v_line

        image = ImageMobject("Joseph Fourier")
        image.set_height(5)
        image.to_edge(LEFT)

        frame = Rectangle()
        frame.replace(image, stretch=True)

        name = OldTexText("Joseph", "Fourier")
        fourier_part = name.get_part_by_tex("Fourier")
        fourier_part.set_color(YELLOW)
        F_sym = fourier_part[0]
        name.match_width(image)
        name.next_to(image, DOWN)

        self.play(
            ReplacementTransform(v_line, frame),
            FadeIn(image),
            FadeIn(name[0]),
            *[
                ReplacementTransform(
                    title[0].deepcopy(),
                    name[1]
                )
                for title in titles
            ],
            titles.scale, 0.65,
            titles.arrange, DOWN,
            titles.next_to, image, UP,
        )
        self.wait()

        big_F = F_sym.copy()
        big_F.set_fill(opacity=0)
        big_F.set_stroke(WHITE, 2)
        big_F.set_height(3)
        big_F.move_to(midpoint(
            image.get_right(),
            RIGHT_SIDE,
        ))
        big_F.shift(DOWN)
        equivalence = VGroup(
            fourier_part.copy().scale(1.25),
            OldTex("\\Leftrightarrow").scale(1.5),
            OldTexText("Break down into\\\\pure frequencies"),
        )
        equivalence.arrange(RIGHT)
        equivalence.move_to(big_F)
        equivalence.to_edge(UP)

        self.play(
            FadeIn(big_F),
            TransformFromCopy(fourier_part, equivalence[0]),
            Write(equivalence[1:]),
        )
        self.wait(3)
        self.play(FadeOut(VGroup(big_F, equivalence)))

        self.image = image
        self.name = name

    def show_paper(self):
        image = self.image
        paper = ImageMobject("Fourier paper")
        paper.match_height(image)
        paper.next_to(image, RIGHT, MED_LARGE_BUFF)

        date = OldTex("1822")
        date.next_to(paper, DOWN)
        date_rect = SurroundingRectangle(date)
        date_rect.scale(0.3)
        date_rect.set_color(RED)
        date_rect.shift(1.37 * UP + 0.08 * LEFT)
        date_arrow = Arrow(
            date_rect.get_bottom(),
            date.get_top(),
            buff=SMALL_BUFF,
            color=date_rect.get_color(),
        )

        heat_rect = SurroundingRectangle(
            OldTexText("CHALEUR")
        )
        heat_rect.set_color(RED)
        heat_rect.scale(0.6)
        heat_rect.move_to(
            paper.get_top() +
            1.22 * DOWN + 0.37 * RIGHT
        )
        heat_word = OldTexText("Heat")
        heat_word.scale(1.5)
        heat_word.next_to(paper, UP)
        heat_word.shift(paper.get_width() * RIGHT)
        heat_arrow = Arrow(
            heat_rect.get_top(),
            heat_word.get_left(),
            buff=0.1,
            path_arc=-60 * DEGREES,
            color=heat_rect.get_color(),
        )

        self.play(FadeIn(paper, LEFT))
        self.play(
            ShowCreation(date_rect),
        )
        self.play(
            GrowFromPoint(date, date_arrow.get_start()),
            ShowCreation(date_arrow),
        )
        self.wait(3)

        # Insert animation of circles/sine waves
        # approximating a square wave

        self.play(
            ShowCreation(heat_rect),
        )
        self.play(
            GrowFromPoint(heat_word, heat_arrow.get_start()),
            ShowCreation(heat_arrow),
        )
        self.wait(3)
