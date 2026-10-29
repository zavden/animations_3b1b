# ==============================================================================
# Scene:      FeynmanFame
# Source:     videos/_2018/lost_lecture.py (lines 403-570)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FeynmanFame.py FeynmanFame -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FeynmanFame(Scene):
    def construct(self):
        books = VGroup(
            ImageMobject("Feynman_QED_cover"),
            ImageMobject("Surely_Youre_Joking_cover"),
            ImageMobject("Feynman_Lectures_cover"),
        )
        for book in books:
            book.set_height(6)
            book.move_to(FRAME_WIDTH * LEFT / 4)

        feynman_diagram = self.get_feynman_diagram()
        feynman_diagram.next_to(ORIGIN, RIGHT)
        fd_parts = VGroup(*reversed(feynman_diagram.family_members_with_points()))

        # As a physicist
        self.play(self.get_book_intro(books[0]))
        self.play(LaggedStartMap(
            Write, feynman_diagram,
            run_time=4
        ))
        self.wait()
        self.play(
            self.get_book_intro(books[1]),
            self.get_book_outro(books[0]),
            LaggedStartMap(
                ApplyMethod, fd_parts,
                lambda m: (m.scale, 0),
                run_time=1
            ),
        )
        self.remove(feynman_diagram)
        self.wait()

        # As a public figure
        safe = SVGMobject(file_name="safe", height=2)
        safe_rect = SurroundingRectangle(safe, buff=0)
        safe_rect.set_stroke(width=0)
        safe_rect.set_fill(GREY_D, 1)
        safe.add_to_back(safe_rect)

        bongo = SVGMobject(file_name="bongo")
        bongo.set_height(1)
        bongo.set_color(WHITE)
        bongo.next_to(safe, RIGHT, LARGE_BUFF)

        objects = VGroup(safe, bongo)

        feynman_smile = ImageMobject("Feynman_Los_Alamos")
        feynman_smile.set_height(4)
        feynman_smile.next_to(objects, DOWN)

        VGroup(objects, feynman_smile).next_to(ORIGIN, RIGHT)

        joke = OldTexText(
            "``Science is the belief \\\\ in the ignorance of \\\\ experts.''"
        )
        joke.move_to(objects)

        self.play(LaggedStartMap(
            DrawBorderThenFill, objects,
            lag_ratio=0.75
        ))
        self.play(self.get_book_intro(feynman_smile))
        self.wait()
        self.play(
            objects.shift, 2 * UP,
            VFadeOut(objects)
        )
        self.play(Write(joke))
        self.wait(2)

        self.play(
            self.get_book_intro(books[2]),
            self.get_book_outro(books[1]),
            LaggedStartMap(FadeOut, joke, run_time=1),
            ApplyMethod(
                feynman_smile.shift, FRAME_HEIGHT * DOWN,
                remover=True
            )
        )

        # As a teacher
        feynman_teacher = ImageMobject("Feynman_teaching")
        feynman_teacher.set_width(FRAME_WIDTH / 2 - 1)
        feynman_teacher.next_to(ORIGIN, RIGHT)

        self.play(self.get_book_intro(feynman_teacher))
        self.wait(3)

    def get_book_animation(self, book,
                           initial_shift,
                           animated_shift,
                           opacity_func
                           ):
        rect = BackgroundRectangle(book, fill_opacity=1)
        book.shift(initial_shift)

        return AnimationGroup(
            ApplyMethod(book.shift, animated_shift),
            UpdateFromAlphaFunc(
                rect, lambda r, a: r.move_to(book).set_fill(
                    opacity=opacity_func(a)
                ),
                remover=True
            )
        )

    def get_book_intro(self, book):
        return self.get_book_animation(
            book, 2 * DOWN, 2 * UP, lambda a: 1 - a
        )

    def get_book_outro(self, book):
        return ApplyMethod(book.shift, FRAME_HEIGHT * UP, remover=True)

    def get_feynman_diagram(self):
        x_min = -1.5
        x_max = 1.5
        arrow = Arrow(LEFT, RIGHT, buff=0)
        arrow.tip.move_to(arrow.get_center())
        arrows = VGroup(*[
            arrow.copy().rotate(angle).next_to(point, vect, buff=0)
            for (angle, point, vect) in [
                (-45 * DEGREES, x_min * RIGHT, UL),
                (-135 * DEGREES, x_min * RIGHT, DL),
                (-135 * DEGREES, x_max * RIGHT, UR),
                (-45 * DEGREES, x_max * RIGHT, DR),
            ]
        ])
        labels = VGroup(*[
            OldTex(tex)
            for tex in ["e^-", "e^+", "\\text{\\=q}", "q"]
        ])
        vects = [UR, DR, UL, DL]
        for arrow, label, vect in zip(arrows, labels, vects):
            label.next_to(arrow.get_center(), vect, buff=SMALL_BUFF)

        wave = FunctionGraph(
            lambda x: 0.2 * np.sin(2 * TAU * x),
            x_min=x_min,
            x_max=x_max,
        )
        wave_label = OldTex("\\gamma")
        wave_label.next_to(wave, UP, SMALL_BUFF)
        labels.add(wave_label)

        squiggle = ParametricCurve(
            lambda t: np.array([
                t + 0.5 * np.sin(TAU * t),
                0.5 * np.cos(TAU * t),
                0,
            ]),
            t_min=0,
            t_max=4,
        )
        squiggle.scale(0.25)
        squiggle.set_color(BLUE)
        squiggle.rotate(-30 * DEGREES)
        squiggle.next_to(
            arrows[2].point_from_proportion(0.75),
            DR, buff=0
        )
        squiggle_label = OldTex("g")
        squiggle_label.next_to(squiggle, UR, buff=-MED_SMALL_BUFF)
        labels.add(squiggle_label)

        return VGroup(arrows, wave, squiggle, labels)
