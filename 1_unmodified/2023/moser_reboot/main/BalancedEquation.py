# ==============================================================================
# Scene:      BalancedEquation
# Source:     videos/_2023/moser_reboot/main.py (lines 739-945)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BalancedEquation.py BalancedEquation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BalancedEquation(InteractiveScene):
    def construct(self):
        # Equation
        full_rect = FullScreenRectangle()
        equation = Tex("V - E + F = 2", font_size=60)
        equation.to_edge(UP)
        variables = VGroup(*(
            equation[char][0]
            for char in "VEF"
        ))
        numbers = VGroup(*map(Integer, [1, 0, 1]))
        for number, variable in zip(numbers, variables):
            number.scale(1.25)
            number.next_to(variable, DOWN, MED_SMALL_BUFF)

        self.add(full_rect)
        self.add(equation)

        # Initialize Graph
        original_points = [ORIGIN, RIGHT, UL, DL, UR, 2 * LEFT]
        edges = [
            (0, 1),
            (0, 2),
            (0, 3),
            (1, 4),
            (2, 5),
            (2, 4),
            (5, 0),
            (3, 5),
            (1, 3),
        ]
        faces = [
            (0, 1, 4, 2),
            (0, 2, 5),
            (0, 3, 5),
            (0, 1, 3),
        ]
        dots = VGroup(*(Dot(point) for point in original_points))
        dots.space_out_submobjects(1.5)
        dots.move_to(DOWN)
        points = [dot.get_center() for dot in dots]

        edges = VGroup(*(
            Line(points[i], points[j])
            for i, j in edges
        ))
        edges.set_stroke(BLUE_B, 2)

        colors = [BLUE_E, BLUE_C, TEAL_C, GREY_BROWN]
        faces = VGroup(*(
            Polygon(*[points[i] for i in face]).set_fill(color, 1)
            for face, color in zip(faces, colors)
        ))
        faces.set_stroke(width=0)

        # Trivial graph
        arrow = Vector(DL)
        arrow.next_to(dots[0], UR, SMALL_BUFF)
        word = Text("Trivial graph")
        word.next_to(arrow.get_start(), UP)

        self.add(dots[0])
        self.play(
            Write(word, run_time=1),
            GrowArrow(arrow),
        )
        self.wait()

        self.play(
            FlashAround(equation["V"]),
            FlashAround(dots[0]),
            FadeIn(numbers[0], 0.5 * DOWN),
        )
        self.wait(0.5)
        self.play(
            FlashAround(equation["F"]),
            full_rect.animate.set_fill(BLUE_E, 0.5).set_anim_args(rate_func=there_and_back),
            FadeIn(numbers[2], 0.5 * DOWN)
        )
        self.wait()
        self.play(
            FlashAround(equation["E"]),
            FadeIn(numbers[1], 0.5 * DOWN)
        )
        self.wait()
        self.play(FadeOut(word), FadeOut(arrow))

        # Edges with new vertices
        number_y = numbers.get_y()
        increments = VGroup(
            Integer(1, include_sign=True),
            Integer(-1, include_sign=True),
            Integer(1, include_sign=True),
        )
        for number, incr in zip(numbers, increments):
            incr.next_to(number, DOWN)
            incr.set_color(YELLOW)

        def incr_anim(*ns):
            return LaggedStart(*(
                AnimationGroup(
                    UpdateFromAlphaFunc(
                        increments[n], lambda m, a: m.set_y(number_y - 0.75 * a).set_opacity(there_and_back(a))
                    ),
                    ChangeDecimalToValue(
                        numbers[n], numbers[n].get_value() + 1,
                        run_time=0.25
                    )
                )
                for n in ns
            ), lag_ratio=0.1)

        new_vert_word = TexText(R"New edge $\rightarrow$ New vertex")
        new_vert_word["New vertex"].set_color(YELLOW)
        new_vert_word.next_to(dots[1], UP)
        new_vert_word.set_backstroke(width=2)

        self.play(
            ShowCreation(edges[0]),
            FadeIn(new_vert_word[R"New edge $\rightarrow$"][0])
        )
        self.wait()
        self.play(
            FadeIn(dots[1], scale=0.5),
            FadeIn(new_vert_word["New vertex"][0], lag_ratio=0.1)
        )
        self.play(incr_anim(0, 1))
        for i in [2, 3, 5, 4]:
            self.add(edges[i - 1], new_vert_word)
            self.play(
                ShowCreation(edges[i - 1]),
                new_vert_word.animate.next_to(dots[i], UP),
                FadeIn(dots[i])
            )
            self.play(incr_anim(0, 1))

        # Edges with new faces
        new_face_word = TexText(R"New edge $\rightarrow$ New face")
        new_face_word["New face"].set_color(BLUE)
        new_face_word.next_to(faces[0], UP)

        self.play(
            FadeTransform(new_vert_word, new_face_word),
            ShowCreation(edges[5]),
        )
        self.play(Write(faces[0]))
        self.play(incr_anim(1, 2))
        self.wait()
        for i, vect in zip([1, 2, 3], [UP, DOWN, DOWN]):
            self.add(edges[i + 5], dots)
            self.play(
                ShowCreation(edges[i + 5]),
                new_face_word.animate.next_to(faces[i], vect),
            )
            self.add(faces[i], edges[:i + 5], dots, new_face_word)
            self.play(Write(faces[i]))
            self.play(incr_anim(1, 2))
        self.add(*faces, *edges, *dots)
        self.play(
            FadeOut(new_face_word),
            FadeOut(numbers),
        )

        # Name formula
        rect = SurroundingRectangle(equation)
        rect.set_stroke(YELLOW, 2)
        name = TexText("Euler's Characteristic Formula", font_size=60)
        name.next_to(rect, DOWN, buff=MED_LARGE_BUFF)

        self.play(
            ShowCreation(rect),
            FlashAround(equation),
            Write(name, run_time=2),
        )
        self.wait()
        self.play(FadeOut(rect), FadeOut(name))

        # Rearrange
        new_equation = Tex("F = E - V + 2")
        new_equation.match_height(equation)
        new_equation.move_to(equation)

        face_labels = index_labels(faces, label_height=0.2)
        face_labels.set_backstroke(BLACK, 3)
        face_labels[3].shift(0.3 * UP)
        outer_label = Integer(len(faces) + 1)
        outer_label.match_height(face_labels[0])
        outer_label.match_style(face_labels[0])
        outer_label.next_to(faces, RIGHT, MED_LARGE_BUFF)

        self.remove(faces)
        self.play(
            ShowIncreasingSubsets(faces),
            ShowIncreasingSubsets(face_labels),
            run_time=2,
        )
        self.add(edges, *dots)
        self.wait(0.2)
        self.add(outer_label)
        full_rect.set_fill(BLUE_E, 0.5)
        self.wait(0.5)
        full_rect.set_fill(GREY_E, 1)
        self.wait()
        self.play(TransformMatchingTex(
            equation, new_equation, path_arc=90 * DEGREES
        ))
        self.wait()
